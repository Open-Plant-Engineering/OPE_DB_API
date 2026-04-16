from sqlalchemy import and_, or_, not_, cast, String
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.dialects.postgresql import JSONB

from OPE_DB_API.registry import SEARCHABLE_COLUMN_REGISTRY


def compile_search(
    model,
    domain: str,
    node,
):
    """
    Compile a SearchNode into a SQLAlchemy expression.
    """

    if hasattr(node, "and_"):
        return and_(
            *[compile_search(model, domain, n) for n in node.and_]
        )

    if hasattr(node, "or_"):
        return or_(
            *[compile_search(model, domain, n) for n in node.or_]
        )

    if hasattr(node, "not_"):
        return not_(
            compile_search(model, domain, node.not_)
        )

    # Atomic condition
    field = node.field
    op = node.op
    value = node.value

    # Validate column access
    base_field = field.split(".")[0]
    if base_field not in SEARCHABLE_COLUMN_REGISTRY[domain]:
        raise ValueError(f"Field '{base_field}' not searchable")

    column = getattr(model, base_field)

    # -------------------------------------------------
    # JSON path handling (value.key)
    # -------------------------------------------------
    if "." in field:
        _, json_key = field.split(".", 1)
        column = column[json_key].astext

    # -------------------------------------------------
    # Operators
    # -------------------------------------------------
    if op == "=":
        return column == value

    if op == "!=":
        return column != value

    if op == ">":
        return column > value

    if op == "<":
        return column < value

    if op == ">=":
        return column >= value

    if op == "<=":
        return column <= value

    if op == "in":
        return column.in_(value)

    if op == "contains":
        return cast(column, String).ilike(f"%{value}%")

    if op == "json_contains":
        return cast(column, JSONB).contains(value)

    if op == "json_key_exists":
        return cast(column, JSONB).has_key(value)  # noqa: E711

    raise ValueError(f"Unsupported operator: {op}")