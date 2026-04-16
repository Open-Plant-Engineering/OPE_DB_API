from typing import Any


def resolve_field(row, field: str):
    """
    Resolve a field or JSON path from a SQLAlchemy row.
    Supports:
      - field
      - value.key
    """
    if "." not in field:
        return getattr(row, field, None)

    base, json_key = field.split(".", 1)
    json_obj = getattr(row, base, None)
    if json_obj is None:
        return None

    return json_obj.get(json_key)


def eval_condition(row, condition) -> bool:
    """
    Evaluate a SearchCondition against a row.
    """
    field = condition.field
    op = condition.op
    value = condition.value

    row_value = resolve_field(row, field)

    if op == "=":
        return row_value == value

    if op == "!=":
        return row_value != value

    if op == ">":
        return row_value is not None and row_value > value

    if op == "<":
        return row_value is not None and row_value < value

    if op == ">=":
        return row_value is not None and row_value >= value

    if op == "<=":
        return row_value is not None and row_value <= value

    if op == "in":
        return row_value in value

    if op == "contains":
        return row_value is not None and str(value) in str(row_value)

    if op == "json_contains":
        return isinstance(row_value, dict) and value.items() <= row_value.items()

    if op == "json_key_exists":
        return isinstance(row_value, dict) and value in row_value

    raise ValueError(f"Unsupported operator: {op}")


def eval_search_node(row, node) -> bool:
    """
    Recursively evaluate a SearchNode against a row.
    """

    # AND
    if hasattr(node, "and_"):
        return all(eval_search_node(row, n) for n in node.and_)

    # OR
    if hasattr(node, "or_"):
        return any(eval_search_node(row, n) for n in node.or_)

    # NOT
    if hasattr(node, "not_"):
        return not eval_search_node(row, node.not_)

    # Atomic condition
    return eval_condition(row, node)