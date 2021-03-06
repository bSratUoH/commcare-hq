from django.test import TestCase

from corehq.apps.domain.shortcuts import create_domain
from corehq.apps.locations.models import LocationType, make_location


class SiteCodeTest(TestCase):

    domain = 'test-site-code'

    @classmethod
    def setUpClass(cls):
        super(SiteCodeTest, cls).setUpClass()
        cls.project = create_domain(cls.domain)
        LocationType(domain=cls.domain, name='type').save()

    @classmethod
    def tearDownClass(cls):
        cls.project.delete()
        super(SiteCodeTest, cls).tearDownClass()

    def testSimpleName(self):
        location = make_location(
            name="Some Location",
            domain=self.domain,
            location_type="type"
        )

        location.save()

        self.assertEqual(location.site_code, 'some_location')

    def testOtherCharacters(self):
        location = make_location(
            name="Somé$ #Location (Old)",
            domain=self.domain,
            location_type="type"
        )

        location.save()

        self.assertEqual(location.site_code, 'some_location_old')

    def testDoesntDuplicate(self):
        location = make_location(
            name="Location",
            domain=self.domain,
            location_type="type"
        )

        location.save()

        self.assertEqual(location.site_code, 'location')

        location = make_location(
            name="Location",
            domain=self.domain,
            location_type="type"
        )

        location.save()

        self.assertEqual(location.site_code, 'location1')
