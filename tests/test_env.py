from fakts_next import Fakts, EnvGrant
import os

TESTS_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


def test_env_grant():
    os.environ["FAKTS_TEST__HELLO__WORLD"] = "KARL"

    fakts_next = Fakts(grant=EnvGrant())
    with fakts_next:
        assert (
            fakts_next.get("test.hello.world")== "KARL"
        ), "Incorrectly loaded the fakts_next"


def test_env_grant_with_prepend():
    os.environ["TEST_FAKTS_NEXT_TEST__HELLO__WORLD"] = "Hello World"

    fakts_next = Fakts(grant=EnvGrant(prepend="TEST_FAKTS_NEXT_"))
    with fakts_next:
        assert (
            fakts_next.get("test.hello.world") == "Hello World"
        ), "Incorrectly loaded the fakts_next"


def test_env_grant_with_delimiter():
    os.environ["FAKTS_TEST-HELLO-WORLD"] = "Hello World"

    fakts_next = Fakts(grant=EnvGrant(delimiter="-"))
    with fakts_next:
        assert (
            fakts_next.get("test.hello.world") == "Hello World"
        ), "Incorrectly loaded the fakts_next"
