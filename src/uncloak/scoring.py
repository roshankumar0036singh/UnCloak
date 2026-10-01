import json

from uncloak.models import Candidate, ScoreBreakdown


def score_candidate(candidate: Candidate) -> Candidate:
    breakdown = ScoreBreakdown()
    total = 0.0

    if not candidate.captures:
        return candidate

    cap = candidate.captures[0]

    body = cap.response_body.strip()
    if body.startswith("{") or body.startswith("["):
        breakdown.is_json = 10.0
        total += 10.0

        try:
            data = json.loads(body)
            if isinstance(data, list) or (
                isinstance(data, dict)
                and any(isinstance(v, list) for v in data.values())
            ):
                breakdown.has_data_array = 20.0
                total += 20.0
        except Exception:
            pass

    new_cand = candidate.model_copy(deep=True)
    new_cand.breakdown = breakdown
    new_cand.score = total
    return new_cand
