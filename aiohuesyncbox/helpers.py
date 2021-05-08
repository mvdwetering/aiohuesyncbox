"""Helper functions."""

from typing import List


def generate_attribute_string(self, attributes: List) -> str:
    output = ""
    for attribute in attributes:
        output += f"{attribute}: {getattr(self, attribute)}\n"
    return output
