import socket
import sys
import os
import netifaces
import ctypes
from typing import List, Optional, Dict
from shellInteract import *


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


def find_file(root_directory, target_file):
    """
    Finds path to a given file in a subtree of a given dir
    (NOTE:doesn't consider two identical file names)
    """
    for root, dirs, files in os.walk(root_directory):
        if target_file in files:
            return os.path.join(root, target_file)


class InterfaceInfo:
    """ "Interface info data class used for convinience"""

    def __init__(self, interface_ip: str, interface_name: str, interface_index: int):
        self.interface_ip = interface_ip
        self.interface_name = interface_name
        self.interface_index = interface_index


def get_interface_info(interface_ip: str) -> InterfaceInfo:
    """returns filled interface info object for the given interface ip"""

    interface_name = Interface_ip_to_name(interface_ip)
    return InterfaceInfo(
        interface_ip, interface_name, interface_name_to_index(interface_name)
    )


def Interface_ip_to_name(interface_ip: str) -> str:
    """gets interface name from its ip"""

    # Go from IP to interface name using netifaces.  To do that, we have to iterate through
    # all of the machine's interfaces
    interface_name: Optional[str] = None
    for interface in netifaces.interfaces():
        addresses_at_each_level: Dict[int, List[Dict[str, str]]] = (
            netifaces.ifaddresses(interface)
        )
        for address_family in [netifaces.AF_INET, netifaces.AF_INET6]:
            if address_family in addresses_at_each_level:
                for address in addresses_at_each_level[address_family]:
                    if address["addr"] == interface_ip:
                        interface_name = interface

    if interface_name is None:
        raise KeyError("Could not find network address with local IP " + interface_ip)

    return interface_name


if sys.platform == "win32":
    iphlpapi = ctypes.WinDLL("iphlpapi")
    win32_GetAdapterIndex = iphlpapi.GetAdapterIndex
    win32_GetAdapterIndex.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong)]


def interface_name_to_index(interface_name: str) -> int:
    """
    Convert a network interface's name into its interface index.
    """

    if sys.platform == "win32":

        # To get the if index on Windows we have to use the GetAdapterIndex() function.
        # docs here: https://docs.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getadapterindex

        if_idx = ctypes.c_ulong()  # value is returned here

        # Has to be prepended to the names returned by netifaces
        # in order for the win32 API to recognize them.
        interface_name_string = ctypes.c_wchar_p("\\DEVICE\\TCPIP_" + interface_name)

        ret = win32_GetAdapterIndex(interface_name_string, ctypes.byref(if_idx))
        if ret != 0:
            raise ctypes.WinError(ret, "GetAdapterIndex() failed")

        return if_idx.value
    else:
        # Unix based
        return socket.if_nametoindex(interface_name)


def get_interface_ips(include_ipv4: bool = True) -> List[str]:
    """get ips of all interfaces"""
    ip_list = []
    for interface in netifaces.interfaces():

        all_addresses: List[Dict[str, str]] = []
        addresses_at_each_level = netifaces.ifaddresses(interface)

        if include_ipv4:
            # Note: Check needed because some interfaces do not have an ipv4 or ipv6 address
            if netifaces.AF_INET in addresses_at_each_level:
                all_addresses.extend(addresses_at_each_level[netifaces.AF_INET])

        for address_dict in all_addresses:
            ip_list.append(address_dict["addr"])

    return ip_list


_cached_python_cmd = None


def get_python_cmd():
    """gets the python command for the current platform"""
    global _cached_python_cmd
    if _cached_python_cmd is None:
        if sys.platform == "win32":
            _cached_python_cmd = "python"
        else:
            _cached_python_cmd = (
                f"python{sys.version_info.major}.{sys.version_info.minor}"
            )
    return _cached_python_cmd
