import json
import pytest
import requests_mock
from unittest.mock import patch
from pifunc.cli import main, parse_args

@pytest.fixture(autouse=True)
def _requests_mock():
    """Automatically use requests mock for all tests"""
    with requests_mock.Mocker() as m:
        yield m

def test_cli_help():
    """Test CLI help command"""
    with patch('sys.argv', ['cli', '--help']):
        with pytest.raises(SystemExit) as e:
            parse_args()
        assert e.value.code == 0

def test_call_command_help():
    """Test call command help"""
    with patch('sys.argv', ['cli', 'call', '--help']):
        with patch('sys.stdout') as mock_stdout:
            with pytest.raises(SystemExit) as e:
                parse_args()
            assert e.value.code == 0

def test_call_with_http_protocol(_requests_mock):
    """Test calling a service with HTTP protocol"""
    mock_response = {'result': 8}
    _requests_mock.post(
        'http://localhost:8080/api/add',
        json=mock_response
    )
    
    with patch('sys.argv', [
        'cli',
        'call',
        'add',
        '--protocol', 'http',
        '--args', '{"a": 5, "b": 3}'
    ]):
        with patch('sys.stdout') as mock_stdout:
            assert main() == 0

def test_call_with_invalid_json():
    """Test calling with invalid JSON arguments"""
    with patch('sys.argv', [
        'cli',
        'call',
        'add',
        '--args', 'invalid json'
    ]):
        with patch('sys.stderr') as mock_stderr:
            assert main() != 0

def test_call_with_unsupported_protocol():
    """Test calling with unsupported protocol"""
    with patch('sys.argv', [
        'cli',
        'call',
        'add',
        '--protocol', 'unsupported',
        '--args', '{}'
    ]):
        with patch('sys.stderr') as mock_stderr:
            assert main() == 1

def test_call_http_service_failure(_requests_mock):
    """Test handling HTTP service failure"""
    _requests_mock.post(
        'http://localhost:8080/api/add',
        status_code=500
    )
    
    with patch('sys.argv', [
        'cli',
        'call',
        'add',
        '--protocol', 'http',
        '--args', '{"a": 5, "b": 3}'
    ]):
        with patch('sys.stderr') as mock_stderr:
            assert main() == 1
