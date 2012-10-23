from corehq.apps.reports.standard import CustomProjectReport
from corehq.apps.reports.generic import GenericTabularReport,\
    SummaryTablularReport
import random
from corehq.apps.reports.datatables import DataTablesHeader, DataTablesColumn
from datetime import datetime, timedelta
from copy import copy
from corehq.apps.reports.dispatcher import CustomProjectReportDispatcher
import urllib
from dimagi.utils.html import format_html
from corehq.apps.groups.models import Group

class ConvenientBaseMixIn(object):
    # this is everything that's shared amongst the Bihar supervision reports
    # this class is an amalgamation of random behavior and is just 
    # for convenience
    
    hide_filters = True
    flush_layout = True
    mobile_enabled = True
    
    # for the lazy
    _headers = []  # override
    @property
    def headers(self):
        return DataTablesHeader(*(DataTablesColumn(h) for h in self._headers))

    @property
    def render_next(self):
        return None if self.rendered_as == "async" else self.rendered_as
       
    @classmethod
    def show_in_navigation(cls, request, *args, **kwargs):
        return False
     


class TeamHoldingMixIn(object):
    @property
    def team(self):
        return self.request_params.get('team')
    
class ReportReferenceMixIn(object):
    # allow a report to reference another report
    
    @property
    def next_report_slug(self):
        return self.request_params.get("next_report")
    
    @property
    def next_report_class(self):
        return CustomProjectReportDispatcher().get_report(self.domain, self.next_report_slug)
    

class MockTablularReport(ConvenientBaseMixIn, GenericTabularReport, CustomProjectReport):
    
    row_count = 20 # override if needed
    def _row(self, i):
        # override
        raise NotImplementedError("Override this!")
    
    @property
    def rows(self):
        return [self._row(i) for i in range(self.row_count)]

class MockSummaryReport(ConvenientBaseMixIn, SummaryTablularReport, CustomProjectReport):
    
    def fake_done_due(self, i=20):
        # highly customized for gates
        return "(%(done)s Done / %(due)s Due)" % \
            {"done": random.randint(0, i),
             "due": i}
            
class MockNavReport(MockSummaryReport):
    # this is a bit of a bastardization of the summary report
    # but it is quite DRY
    
    preserve_url_params = False
    
    @property
    def reports(self):
        # override
        raise NotImplementedError("Override this!")
    
    @property
    def _headers(self):
        return [" "] * len(self.reports)
    
    @property
    def data(self):
        def _nav_link(report_cls):
            url = report_cls.get_url(self.domain, 
                                     render_as=self.render_next)
            if self.preserve_url_params:
                url = url_and_params(url, self.request_params)
            return format_html('<a href="{details}">{val}</a>',
                                val=report_cls.name, 
                                details=url)
        return [_nav_link(report_cls) for report_cls in self.reports]
        

class MockEmptyReport(MockSummaryReport):
    """
    A stub empty report
    """
    _headers = ["Whoops, this report isn't done! Sorry this is still a prototype."]
    data = [""]
    
        
class SubCenterSelectionReport(ConvenientBaseMixIn, GenericTabularReport, 
                               CustomProjectReport, ReportReferenceMixIn):
    name = "Select Subcenter"
    slug = "subcenter"
    description = "Subcenter selection report"
    
    _headers = ["Team Name", "Rank"]
    
    def __init__(self, *args, **kwargs):
        super(SubCenterSelectionReport, self).__init__(*args, **kwargs)
    
    def _get_groups(self):
        groups = Group.by_domain(self.domain)
        # temp hack till we figure out how user/group association works
        return filter(lambda g: "Aguwanpur" in g.name, groups)
        
    @property
    def rows(self):
        return [self._row(g) for g in self._get_groups()]
        
    def _row(self, group):
        
        def _link(g):
            params = copy(self.request_params)
            params["team"] = g.get_id
            return format_html('<a href="{details}">{group}</a>',
                group=g.name,
                details=url_and_params(self.next_report_class.get_url(self.domain,
                                                                      render_as=self.render_next),
                                       params))
        denom = random.randint(5, 20)
        num = random.randint(0, denom)
        return [_link(group), 
                "%s / %s" % (num, denom)]
            

class MainNavReport(MockNavReport):
    name = "Main Menu"
    slug = "mainnav"
    description = "Main navigation"
    
    @classmethod
    def show_in_navigation(cls, request, *args, **kwargs):
        return True
    
    @property
    def reports(self):
        from bihar.reports.indicators.reports import IndicatorSelectNav
        return [IndicatorSelectNav, WorkerRankReport, 
                DueListReport, ToolsReport]


# TODO
class WorkerRankReport(MockEmptyReport):
    name = "Worker Rank"
    slug = "workerranks"

class DueListReport(MockEmptyReport):
    name = "Due List"
    slug = "duelist"

class ToolsReport(MockEmptyReport):
    name = "Tools"
    slug = "tools"

class ClientListReport(MockTablularReport):
    _headers = ["Name", "EDD"] 
    
    def _row(self, i):
        def _random_edd():
            return (datetime.now() + timedelta(days=random.randint(0, 9 * 28))).strftime("%Y-%m-%d" )
        return ["Mother %s" % i, _random_edd()]
        
def url_and_params(urlbase, params):
    assert "?" not in urlbase
    return "{url}?{params}".format(url=urlbase, 
                                   params=urllib.urlencode(params))