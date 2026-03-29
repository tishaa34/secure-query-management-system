from app.core.enums import QueryStatus
from app.core.exceptions import ValidationError

ALLOWED_TRANSITIONS: dict[QueryStatus, set[QueryStatus]] = {
    QueryStatus.NEW: {QueryStatus.ASSIGNED},
    QueryStatus.ASSIGNED: {QueryStatus.IN_PROGRESS},
    QueryStatus.IN_PROGRESS: {QueryStatus.ON_HOLD, QueryStatus.RESOLVED},
    QueryStatus.ON_HOLD: {QueryStatus.IN_PROGRESS},
    QueryStatus.RESOLVED: set(),
}


def ensure_valid_transition(current_status: QueryStatus, next_status: QueryStatus) -> None:
    if next_status == current_status:
        return
    if next_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValidationError(f"Invalid workflow transition: {current_status} -> {next_status}.")
