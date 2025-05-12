from fakts_next import Fakts
from fakts_next.grants.io.yaml import YamlGrant
from fakts_next.cache.file import FileCache
import os


TESTS_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


def test_cache():
    grant = YamlGrant(filepath=f"{TESTS_FOLDER}/test.yaml")

    fakts_next = Fakts(grant=grant, cache=FileCache())

    with fakts_next:
        
        values = fakts_next.get("test")
        assert isinstance(values, dict), "Fakts: test is not a dict"
        hello = values.get("hello")
        assert isinstance(hello, dict), "Fakts: test.hello is not a dict"
        assert hello["world"] == "Hello world"
        assert fakts_next.get("test.hello.world") == "Hello world"
