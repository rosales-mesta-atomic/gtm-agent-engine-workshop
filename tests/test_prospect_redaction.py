import unittest

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


SENSITIVE_FIELDS = {
    "billing_qualification",
    "tax_id",
    "card_on_file",
    "date_of_birth",
    "credit_check_ref",
}


def collect_keys(value):
    if isinstance(value, dict):
        return set(value) | set().union(*(collect_keys(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(collect_keys(item) for item in value))
    return set()


class ProspectRedactionTest(unittest.TestCase):
    def setUp(self):
        data_service._PROFILES.clear()

    def test_prospect_tools_exclude_sensitive_fields(self):
        contact = get_prospect.invoke({"prospect_id": "LEAD-90001"})
        profile = build_prospect_profile.invoke({"prospect_id": "LEAD-90001"})

        self.assertTrue(SENSITIVE_FIELDS.isdisjoint(collect_keys(contact)))
        self.assertTrue(SENSITIVE_FIELDS.isdisjoint(collect_keys(profile)))
        cached = data_service.get_profile_from_db("LEAD-90001")["prospect_profile"]
        self.assertTrue(SENSITIVE_FIELDS.isdisjoint(collect_keys(cached)))


if __name__ == "__main__":
    unittest.main()
