from gtm_agent import data_service


def test_update_prospect_info_persists_technology_and_clears_profile_cache():
    prospect_id = "LEAD-71001"
    record = data_service.get_prospect_record(prospect_id)
    original_tech_stack = record["tech_stack"]
    original_profile = data_service.get_profile_from_db(prospect_id)["prospect_profile"]
    record["tech_stack"] = [technology for technology in original_tech_stack if technology != "Kafka"]
    data_service.save_profile_to_db(prospect_id, {"prospect_id": prospect_id})

    try:
        result = data_service.update_prospect_info(prospect_id, "Kafka")

        assert result == {
            "updated": True,
            "found": True,
            "tech_stack": record["tech_stack"],
        }
        assert "Kafka" in data_service.fetch_tech_stack(prospect_id)
        assert data_service.get_profile_from_db(prospect_id)["prospect_profile"] is None
    finally:
        record["tech_stack"] = original_tech_stack
        if original_profile is None:
            data_service._PROFILES.pop(prospect_id, None)
        else:
            data_service.save_profile_to_db(prospect_id, original_profile)
