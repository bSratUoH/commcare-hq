from django.test import TestCase

from corehq.apps.fixtures.dbaccessors import (
    get_fixture_data_types,
    count_fixture_data_types,
)
from corehq.apps.fixtures.models import FixtureDataType


class DBAccessorTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DBAccessorTest, cls).setUpClass()
        cls.domain = 'fixture-dbaccessors'
        cls.data_types = [
            FixtureDataType(domain=cls.domain, tag='a'),
            FixtureDataType(domain=cls.domain, tag='b'),
            FixtureDataType(domain=cls.domain, tag='c'),
            FixtureDataType(domain='other-domain', tag='x'),
        ]
        FixtureDataType.get_db().bulk_save(cls.data_types)
        get_fixture_data_types.clear(cls.domain)

    @classmethod
    def tearDownClass(cls):
        FixtureDataType.get_db().bulk_delete(cls.data_types)
        get_fixture_data_types.clear(cls.domain)
        super(DBAccessorTest, cls).tearDownClass()

    def test_count_fixture_data_types(self):
        self.assertEqual(
            count_fixture_data_types(self.domain),
            len([data_type for data_type in self.data_types
                 if data_type.domain == self.domain])
        )

    def test_get_fixture_data_types(self):
        expected = [data_type.to_json() for data_type in self.data_types if data_type.domain == self.domain]
        actual = [o.to_json() for o in get_fixture_data_types(self.domain)]
        self.assertItemsEqual(actual, expected)
