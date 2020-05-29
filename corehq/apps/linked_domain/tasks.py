from celery.task import task

from django.conf import settings
from django.utils.translation import ugettext as _

from corehq import toggles
from corehq.apps.app_manager.dbaccessors import get_apps_in_domain
from corehq.apps.app_manager.util import is_linked_app
from corehq.apps.app_manager.views.utils import update_linked_app
from corehq.apps.hqwebapp.tasks import send_mail_async
from corehq.apps.linked_domain.const import MODEL_APP
from corehq.apps.linked_domain.dbaccessors import get_linked_domains
from corehq.apps.linked_domain.util import (
    pull_missing_multimedia_for_app_and_notify,
)
from corehq.apps.linked_domain.updates import update_model_type
from corehq.apps.users.models import CouchUser


@task(queue='background_queue')
def pull_missing_multimedia_for_app_and_notify_task(domain, app_id, email=None):
    pull_missing_multimedia_for_app_and_notify(domain, app_id, email)


@task(queue='background_queue')
def push_models(master_domain, models, linked_domains, username):
    domain_links_by_linked_domain = {link.linked_domain: link for link in get_linked_domains(master_domain)}
    user = CouchUser.get_by_username(username)
    errors = []
    for linked_domain in linked_domains:
        if linked_domain not in domain_links_by_linked_domain:
            errors.append(_("Project space {} is no longer linked to this project space").format(linked_domain))
            continue
        domain_link = domain_links_by_linked_domain[linked_domain]
        for model in models:
            try:
                if model['type'] == MODEL_APP:
                    app_id = model['detail']['app_id']
                    for linked_app in get_apps_in_domain(linked_domain, include_remote=False):
                        if is_linked_app(linked_app) and linked_app.family_id == app_id:
                            if toggles.MULTI_MASTER_LINKED_DOMAINS.enabled(linked_domain):
                                msg = _("Cannot update apps for project spaces using multi master")
                                errors.append(_("Updating {} in {}: {}").format(model['name'], linked_domain, msg))
                                continue
                            update_linked_app(linked_app, app_id, user.user_id)
                else:
                    update_model_type(domain_link, model['type'], model_detail=model['detail'])
            except Exception as e:   # intentionally broad
                errors.append(_("Updating {} in {}: {}").format(model['name'], linked_domain, str(e)))
    subject = _("Linked project release complete.")
    if errors:
        subject += _(" Errors occurred.")
    message = _("""
Release complete.{}

The following content was released:
{}

The following linked domains received this content:
{}
    """).format(
        "\nThe following errors occurred:\n" + "\n".join("- " + e for e in errors) if errors else "",
        "\n".join(["- " + m['name'] for m in models]),
        "\n".join(["- " + d for d in linked_domains])
    )
    send_mail_async.delay(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email or user.username])
