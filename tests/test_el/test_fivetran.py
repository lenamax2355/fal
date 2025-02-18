from mock import patch, Mock, ANY
import requests

from fal.el.fivetran import FivetranClient, ScheduleType


def test_fivetran_get_connector_data():
    api_client = FivetranClient(
        api_key="test_key", api_secret="test_secret", disable_schedule_on_trigger=False
    )
    with patch("requests.request") as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError()
        try:
            api_client.get_connector_data(connector_id="test_id")
        except Exception as e:
            mock_request.assert_called_with(
                method="GET",
                url="https://api.fivetran.com/v1/connectors/test_id",
                headers={"Content-Type": "application/json;version=2"},
                auth=ANY,
                data=None,
                timeout=5,
            )
            assert str(e) == "Exceeded max number of retries."


def test_fivetran_check_connector():
    api_client = FivetranClient(
        api_key="test_key", api_secret="test_secret", disable_schedule_on_trigger=False
    )
    with patch("requests.request") as mock_request:
        try:
            api_client.check_connector("test_id")

        except Exception as e:
            mock_request.assert_called_with(
                method="GET",
                url="https://api.fivetran.com/v1/connectors/test_id",
                headers={"Content-Type": "application/json;version=2"},
                auth=ANY,
                data=None,
                timeout=5,
            )
            assert str(e) == "Cannot sync connector test_id: not set up."


def test_fivetran_update_connector():
    api_client = FivetranClient(
        api_key="test_key", api_secret="test_secret", disable_schedule_on_trigger=False
    )
    with patch("requests.request") as mock_request:
        try:
            api_client.update_connector("test_id", {"test_key": "test_value"})

        except Exception as e:
            mock_request.assert_called_with(
                method="PATCH",
                url="https://api.fivetran.com/v1/connectors/test_id",
                headers={"Content-Type": "application/json;version=2"},
                auth=ANY,
                data='{"test_key": "test_value"}',
                timeout=5,
            )
            assert str(e) == "Exceeded max number of retries."


def test_fivetran_update_schedule_type():
    api_client = FivetranClient(
        api_key="test_key", api_secret="test_secret", disable_schedule_on_trigger=False
    )
    with patch("requests.request") as mock_request:
        try:
            api_client._update_schedule_type("test_id", ScheduleType.MANUAL)

        except Exception as e:
            mock_request.assert_called_with(
                method="PATCH",
                url="https://api.fivetran.com/v1/connectors/test_id",
                headers={"Content-Type": "application/json;version=2"},
                auth=ANY,
                data='{"schedule_type": "manual"}',
                timeout=5,
            )
            assert str(e) == "Exceeded max number of retries."


def test_fivetran_start_sync():
    api_client = FivetranClient(
        api_key="test_key", api_secret="test_secret", disable_schedule_on_trigger=False
    )
    with patch("requests.request") as mock_request:
        try:
            api_client.check_connector = Mock(return_value=None)
            api_client.start_sync("test_id")

        except Exception as e:
            api_client.check_connector.assert_called_once()
            mock_request.assert_called_with(
                method="POST",
                url="https://api.fivetran.com/v1/connectors/test_id/force",
                headers={"Content-Type": "application/json;version=2"},
                auth=ANY,
                data=None,
                timeout=5,
            )
            assert str(e) == "Exceeded max number of retries."

        api_client.check_connector.reset_mock()
