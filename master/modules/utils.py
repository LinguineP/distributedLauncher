import re
from typing import Callable, List, Tuple


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


def extractIpfromString(inString: str) -> str:
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

    ip_addresses = re.findall(ip_pattern, inString)
    return ip_addresses


def replace_mip(inString: str, mip: str) -> str:
    result = re.sub(r"\bmip\b", str(mip), inString)
    return result


def replace_node_id(inString: str, node_id: str) -> str:
    result = re.sub(r"\bid\b", str(node_id), inString)
    return result


def remove_double_space(inString: str, substring: str):
    while "  " in inString:
        inString = inString.replace("  ", " ")
    return inString


def string_transformer(inString: str, transformations: List[Tuple[Callable, str]]):
    "does all specified transformations on the string"

    for function, param in transformations:
        inString = function(inString, param)
    return inString
