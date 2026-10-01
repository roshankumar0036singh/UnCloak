from uncloak.blocklist import is_blocked

def test_is_blocked_exact():
    assert is_blocked("https://analytics.google.com/foo") is True
    assert is_blocked("https://api.example.com/data") is False

def test_is_blocked_subdomain():
    # If blocklist has sentry.io, ingest.sentry.io should be blocked
    assert is_blocked("https://ingest.sentry.io/api/123/store/") is True
    # But a similar string shouldn't be
    assert is_blocked("https://mysentry.io/api") is False

def test_is_blocked_handles_ports():
    assert is_blocked("https://analytics.google.com:8080/foo") is True
