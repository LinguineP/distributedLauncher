def escape_chars(s):
    """deals with escapable chars useful for paths on windows"""
    escape_dict = {
        "\\": "\\\\",
        "'": "\\'",
        '"': '\\"',
        "\a": "\\a",
        "\b": "\\b",
        "\f": "\\f",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\v": "\\v",
    }
    return "".join([escape_dict.get(char, char) for char in s])
