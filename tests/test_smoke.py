import re
import pytest

def test_import_uncloak():
    import uncloak
    assert uncloak is not None

def test_uncloak_version():
    import uncloak
    assert hasattr(uncloak, "__version__"), "uncloak should have a __version__ attribute"
    
    # Matches simple semver like 0.1.0 or 0.1.0.dev0
    version_pattern = re.compile(r"^\d+\.\d+\.\d+(?:\.dev\d+)?$")
    assert version_pattern.match(uncloak.__version__), f"Invalid version format: {uncloak.__version__}"

def test_uncloak_generate_callable():
    import uncloak
    assert hasattr(uncloak, "generate"), "uncloak should expose 'generate'"
    assert callable(uncloak.generate), "'generate' should be a callable function"
    
    with pytest.raises(NotImplementedError):
        uncloak.generate("https://example.com")

def test_uncloak_check_callable():
    import uncloak
    assert hasattr(uncloak, "check"), "uncloak should expose 'check'"
    assert callable(uncloak.check), "'check' should be a callable function"
    
    with pytest.raises(NotImplementedError):
        uncloak.check("contract.json")
