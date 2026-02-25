import unittest
from unittest.mock import Mock, patch

import requests

import api


class TestApi(unittest.TestCase):
    def test_fetch_token_stats_retries_and_eventually_succeeds(self):
        success_response = Mock()
        success_response.raise_for_status.return_value = None
        success_response.json.return_value = {"data": {"token_info": {"remain_quota_display": "100"}}}

        with patch(
            "api.requests.get",
            side_effect=[
                requests.Timeout("timeout-1"),
                requests.Timeout("timeout-2"),
                success_response,
            ],
        ) as mock_get:
            data = api.fetch_token_stats("demo-token")

        self.assertEqual(data["data"]["token_info"]["remain_quota_display"], "100")
        self.assertEqual(mock_get.call_count, 3)

    def test_fetch_token_stats_raises_after_max_retries(self):
        with patch(
            "api.requests.get",
            side_effect=[
                requests.Timeout("timeout-1"),
                requests.Timeout("timeout-2"),
                requests.Timeout("timeout-3"),
            ],
        ) as mock_get:
            with self.assertRaises(requests.Timeout):
                api.fetch_token_stats("demo-token")

        self.assertEqual(mock_get.call_count, 3)


if __name__ == "__main__":
    unittest.main()
