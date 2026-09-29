import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent import data_service
from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTests(unittest.TestCase):
    def test_disqualified_prospect_is_blocked_without_dispatching(self):
        prospect = {
            "prospect_id": "LEAD-50001",
            "email": "prospect@example.com",
            "name": "Prospect Example",
        }

        with patch.object(
            data_service,
            "get_prospect_record",
            return_value={"disqualified": True},
        ), patch("gtm_agent.gtm_agent.uuid.uuid4") as uuid4:
            result = send_prospect_email.func(
                prospect,
                "A subject",
                "A body",
                runtime=Mock(),
                from_rep={"email": "rep@example.com", "name": "Rep Example"},
            )

        self.assertEqual(
            result,
            {
                "status": "blocked",
                "reason": "prospect is disqualified",
                "requires_confirmation": True,
                "to": "prospect@example.com",
            },
        )
        uuid4.assert_not_called()

    def test_qualified_prospect_is_sent(self):
        prospect = {
            "prospect_id": "LEAD-10001",
            "email": "prospect@example.com",
            "name": "Prospect Example",
        }
        uuid_value = Mock()
        uuid_value.hex = "1234567890abcdef"

        with patch.object(
            data_service,
            "get_prospect_record",
            return_value={"disqualified": False},
        ), patch("gtm_agent.gtm_agent.uuid.uuid4", return_value=uuid_value):
            result = send_prospect_email.func(
                prospect,
                "A subject",
                "A body",
                runtime=Mock(),
                from_rep={"email": "rep@example.com", "name": "Rep Example"},
            )

        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["message_id"], "msg-1234567890ab")
        self.assertEqual(result["to"], "prospect@example.com")


if __name__ == "__main__":
    unittest.main()
