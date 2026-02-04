import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_read_test_endpoint():
    """Test the static /test endpoint to ensure the API starts."""
    response = client.get("/test")
    assert response.status_code == 200
    #assert response.json() == {"message": "If you see this, CURL and Mangum are working!"}
    assert response.json() == {"message": "THIS WILL FAIL THE BUILD"}

@patch("main.get_snowflake_connection")
def test_get_snowflake_version_mock(mock_conn):
    """Test /snowflake-version by mocking the Snowflake connector."""
    # Setup mock cursor and return value
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["8.5.1"]
    
    # Setup mock connection to return the mock cursor
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_conn.return_value = mock_connection

    response = client.get("/snowflake-version")
    
    assert response.status_code == 200
    assert response.json() == {"version": "8.5.1"}
    mock_cursor.execute.assert_called_once_with("SELECT CURRENT_VERSION()")
