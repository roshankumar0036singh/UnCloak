import urllib.parse
from pathlib import Path

BLOCKLIST_PATH = Path(__file__).parent / "data" / "blocklist.txt"


def _load_blocklist() -> set[str]:
    blocked: set[str] = set()
    if not BLOCKLIST_PATH.exists():
        return blocked
    with open(BLOCKLIST_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                blocked.add(line.lower())
    return blocked


_BLOCKED_DOMAINS = _load_blocklist()


def is_blocked(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        if not host:
            return False
        host = host.lower()

        parts = host.split(".")
        for i in range(len(parts)):
            domain_suffix = ".".join(parts[i:])
            if domain_suffix in _BLOCKED_DOMAINS:
                return True
        return False
    except ValueError:
        return False
