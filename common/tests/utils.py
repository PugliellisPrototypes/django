import math


def generate_identifier(n: int) -> str:
    """
    Generate a unique identifier string.

    Creates a tree of identifiers. Each node has 3 children.
    """
    exp = 1

    identifier = ""
    position = n

    while position > (lvl_width := 3**exp):
        exp += 1
        position -= lvl_width

    for _ in range(exp):
        remainder = position % 3
        curr_val = "3" if remainder == 0 else str(remainder)

        position = math.ceil(position / 3)

        if not identifier:
            identifier = curr_val
            continue

        identifier = curr_val + "|" + identifier

    return identifier
