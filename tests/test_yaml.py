from fakts_next import Fakts
from fakts_next.grants.io.yaml import YamlGrant
import os

TESTS_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


def test_yaml_grant():
    fakts_next = Fakts(grant=YamlGrant(filepath=f"{TESTS_FOLDER}/test.yaml"))
    with fakts_next:
        assert fakts_next.get("test")["hello"]["world"] == "Hello world"
