from typing import Any

from sqlalchemy.orm import Session

from backend.app.models.audit import AuditLog


def record_audit(
    db: Session,
    *,
    actor_id: str | None,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    ip_address: str | None = None,
    before_data: dict[str, Any] | None = None,
    after_data: dict[str, Any] | None = None,
) -> AuditLog:

    entry = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip_address,
        before_data=before_data,
        after_data=after_data,
    )

    db.add(entry)
    db.flush()

    return entry