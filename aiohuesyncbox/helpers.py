"""Helper functions."""

def generate_attribute_string(self, attributes):
    output = ""
    for attribute in attributes:
        output += f"{attribute}: {getattr(self, attribute)}\n"
    return output
