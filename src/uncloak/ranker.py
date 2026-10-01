import urllib.parse

from uncloak.models import Candidate, Capture, ScoreBreakdown


def _get_base_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def group_by_endpoint(captures: list[Capture]) -> list[Candidate]:
    groups: dict[str, list[Capture]] = {}
    for c in captures:
        base = _get_base_url(c.url)
        key = f"{c.method} {base}"
        if key not in groups:
            groups[key] = []
        groups[key].append(c)

    candidates = []
    for caps in groups.values():
        candidates.append(
            Candidate(score=0.0, breakdown=ScoreBreakdown(), captures=caps)
        )
    return candidates


def rank_candidates(candidates: list[Candidate]) -> list[Candidate]:
    from uncloak.scoring import score_candidate

    scored = [score_candidate(c) for c in candidates]
    scored.sort(key=lambda c: c.score, reverse=True)
    return scored
