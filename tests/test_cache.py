from fakts_next import Fakts
from fakts_next.cache.file import FileCache
import os
import tempfile
import shutil

from fakts_next.grants.hard import HardFaktsGrant
from fakts_next.models import ActiveFakts, AuthFakt, Instance, Manifest, SelfFakt, Alias, Requirement


TESTS_FOLDER = str(os.path.dirname(os.path.abspath(__file__)))


def test_cache():
    grant = HardFaktsGrant(
        fakts=ActiveFakts(
            self=SelfFakt(deployment_name="test_deployment"),
            auth=AuthFakt(
                client_id="test_client_id",
                client_secret="test_client",
                client_token="test_client_token",
                token_url="http://localhost:8000/token",
                report_url="http://localhost:8000/report",
            ),
            instances={
                "test": Instance(
                    service="test_service",
                    identifier="test_instance",
                    aliases=[
                        Alias(
                            id="test",
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
            requirements=[Requirement(key="test", service="test_service")],
        ),
    )

    with fakts_next:
        alias = fakts_next.get_alias("test", omit_challenge=True, omit_report=True)
        assert alias is not None


def test_cache_with_invalid_filename_characters():
    """Test that cache files with invalid characters in filenames are properly sanitized."""
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Simulate a cache_file path with Windows-style absolute path in filename
        # This mimics the error: '.arkitekt_next/cache/C:\\Users\\imansaray\\repos\\test\\main-0.0.1_fakts_cache.json'
        cache_dir = os.path.join(temp_dir, ".arkitekt_next", "cache")
        cache_file_with_invalid_chars = os.path.join(cache_dir, "C:\\Users\\user\\test\\main-0.0.1_fakts_cache.json")
        
        grant = HardFaktsGrant(
            fakts=ActiveFakts(
                self=SelfFakt(deployment_name="test_deployment"),
                auth=AuthFakt(
                    client_id="test_client_id",
                    client_secret="test_client",
                    client_token="test_client_token",
                    token_url="http://localhost:8000/token",
                    report_url="http://localhost:8000/report",
                ),
                instances={
                    "test": Instance(
                        service="test_service",
                        identifier="test_instance",
                        aliases=[
                            Alias(
                                id="test",
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
            cache=FileCache(cache_file=cache_file_with_invalid_chars),
            manifest=Manifest(
                version="0.1.0",
                identifier="test_manifest",
                scopes=["openid", "profile", "email"],
                logo="http://localhost:8000/logo.png",
                requirements=[Requirement(key="test", service="test_service")],
            ),
        )
        
        # This should not raise an OSError anymore
        with fakts_next:
            alias = fakts_next.get_alias("test", omit_challenge=True, omit_report=True)
            assert alias is not None
            
        # Verify that the cache file was created with sanitized filename
        # The invalid characters should have been replaced with underscores
        assert os.path.exists(cache_dir)
        cache_files = os.listdir(cache_dir)
        assert len(cache_files) > 0
        # The sanitized filename should not contain colons or backslashes
        for cache_file in cache_files:
            assert ":" not in cache_file
            assert "\\" not in cache_file
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)


def test_cache_sanitize_method():
    """Test the _sanitize_cache_path method directly."""
    cache = FileCache()
    
    # Test various paths with invalid characters
    test_cases = [
        "C:\\Users\\test\\file.json",
        ".arkitekt/cache/C:\\test\\file.json",
        "path/to/file:with:colons.json",
        "normal_file.json",
    ]
    
    for input_path in test_cases:
        sanitized = cache._sanitize_cache_path(input_path)
        # Check that the sanitized filename doesn't contain invalid characters
        filename = os.path.basename(sanitized)
        assert ":" not in filename, f"Colon found in sanitized filename: {filename}"
        assert "\\" not in filename, f"Backslash found in sanitized filename: {filename}"

