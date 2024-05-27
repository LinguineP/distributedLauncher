import re


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


def extractIpfromString(inString):
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

    ip_addresses = re.findall(ip_pattern, inString)
    return ip_addresses


def replace_node_id(inString, node_num):
    result = re.sub(r"\bid\b", str(node_num), inString)
    return result
