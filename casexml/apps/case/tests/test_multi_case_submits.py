from django.test import TestCase
import os
from casexml.apps.case.models import CommCareCase
from couchforms.models import XFormInstance
from couchforms.util import post_xform_to_couch
from casexml.apps.case.signals import process_cases


class MultiCaseTest(TestCase):
    
    def setUp(self):
        for case in self._get_cases():
            case.delete()
        for form in self._get_forms():
            form.delete()

        
    def testParallel(self):
        self.assertEqual(0, len(CommCareCase.view("case/by_user", reduce=False).all()))
        file_path = os.path.join(os.path.dirname(__file__), "data", "multicase", "parallel_cases.xml")
        with open(file_path, "rb") as f:
            xml_data = f.read()
        form = post_xform_to_couch(xml_data)
        process_cases(sender="testharness", xform=form)
        cases = self._get_cases()
        self.assertEqual(4, len(cases))
        self._check_ids(form, cases)

    def testMixed(self):
        self.assertEqual(0, len(CommCareCase.view("case/by_user", reduce=False).all()))
        file_path = os.path.join(os.path.dirname(__file__), "data", "multicase", "mixed_cases.xml")
        with open(file_path, "rb") as f:
            xml_data = f.read()
        form = post_xform_to_couch(xml_data)
        process_cases(sender="testharness", xform=form)
        cases = self._get_cases()
        self.assertEqual(4, len(cases))
        self._check_ids(form, cases)



    def testCasesInRepeats(self):
        self.assertEqual(0, len(CommCareCase.view("case/by_user", reduce=False).all()))
        file_path = os.path.join(os.path.dirname(__file__), "data", "multicase", "case_in_repeats.xml")
        with open(file_path, "rb") as f:
            xml_data = f.read()
        form = post_xform_to_couch(xml_data)
        process_cases(sender="testharness", xform=form)
        cases = self._get_cases()
        for case in cases:
            print case._id
        self.assertEqual(3, len(cases))
        self._check_ids(form, cases)

    def _get_cases(self):
        return CommCareCase.view("case/get_lite", reduce=False, include_docs=True).all()

    def _get_forms(self):
        return XFormInstance.view("couchforms/by_xmlns", reduce=False, include_docs=True).all()

    def _check_ids(self, form, cases):
        for case in cases:
            ids = case.get_xform_ids_from_couch()
            self.assertEqual(1, len(ids))
            self.assertEqual(form._id, ids[0])
