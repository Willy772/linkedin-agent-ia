from typing import Dict, List


ALLOWED_FILTERS = {'school', 'title', 'company', 'location'}


def _normalize(value):
    if value is None:
        return None
    return str(value).strip().lower()


def apply_filters(filters: Dict[str, str], candidates: List[Dict]) -> List[Dict]:
    normalized_filters = {k: _normalize(v) for k, v in filters.items() if k in ALLOWED_FILTERS and v}
    if not normalized_filters:
        return candidates

    filtered_candidates = []
    for candidate in candidates:
        matches = True
        for field, value in normalized_filters.items():
            candidate_value = _normalize(candidate.get(field))
            if candidate_value != value:
                matches = False
                break
        if matches:
            filtered_candidates.append(candidate)
    return filtered_candidates
