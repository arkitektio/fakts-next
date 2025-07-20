from fakts_next import Fakts
from fakts_next.cache.file import FileCache
import os

from fakts_next.grants.hard import HardFaktsGrant
from fakts_next.models import ActiveFakts, AuthFakt, Instance, Manifest, SelfFakt, Alias


TESTS_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


def test_cache():
    grant = HardFaktsGrant(
        fakts=ActiveFakts(
            self=SelfFakt(deployment_name="test_deployment"),
            auth=AuthFakt(
                client_id="test_client_id",
                client_secret="test_client",
                token_url="http://localhost:8000/token",
            ),
            instances={
                "test": Instance(
                    service="test_service",
                    identifier="test_instance",
                    aliases=[
                        Alias(
                            host="localhost",
                            port=8000,
                            path="/test",
                        )
                    ],
                )
            },
        )
    )

    fakts_next = Fakts(
        grant=grant,
        cache=FileCache(),
        manifest=Manifest(
            version="0.1.0",
            identifier="test_manifest",
            scopes=["openid", "profile", "email"],
            logo="http://localhost:8000/logo.png",
        ),
    )

    with fakts_next:
        alias = fakts_next.get_alias("test", omit_challenge=True)
        assert alias is not None
