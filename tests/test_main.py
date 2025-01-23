import os
import pytest
from click.testing import CliRunner

from desk import main, auth
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")

@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main.main)
    assert result.exit_code == 0

def test_generate_jwt_succeeds() -> None:
    authorization = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, sub_account_id="2")
    assert authorization.jwt is not None

def test_generate_jwt_succeeds_with_jwt() -> None:
    authorization = auth.Auth(jwt="some jwt")
    assert authorization.jwt == "some jwt"