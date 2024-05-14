

import sys
import select
import socket
import struct
from typing import List ,Tuple, cast
from utils import  get_interface_ips,get_interface_info,InterfaceInfo

LOCALHOST_IPV4="127.0.0.1"

class MulticastSocket:
    """
    Class to wrap a socket that receives from one or more multicast groups.
    """

    

    def __init__(self, multicast_ip : str, multicast_port: int):
        
        self.addr_family = socket.AF_INET #for ipv4 ipv6 not supported
        self.multicast_ip = multicast_ip  #multicast groups ip address
        self.port = multicast_port #port on which multicast is published

        self.is_opened = False

        
        self.timeout=None #controls the timeout if its none its blocking

        
        self.iface_ips = get_interface_ips(self.addr_family == socket.AF_INET)

        # We shouldnt include localhost Ip addrs when listening on all interfaces, as then we would
        # receive all mcasts sent by the current machine.
        if self.addr_family == socket.AF_INET and LOCALHOST_IPV4 in self.iface_ips:
                self.iface_ips.remove(LOCALHOST_IPV4)

        #getting info for all interfaces
        self.iface_infos = {}
        for iface_ip in self.iface_ips:
            try:
                self.iface_infos[iface_ip] = get_interface_info(iface_ip)
            except KeyError:
                raise RuntimeError(
                    f"Interface with ip {iface_ip} does not match any valid interfaces.  Valid interfaces:are {', '.join(self.get_interface_ips())} " 
                    )
        
        self.sockets = []

        # On Windows, we have to create a socket and bind it for each interface address, then subscribe
        # to all multicast addresses on each of those sockets
        # On Unix, we need one socket bound to each multicast address.
        if sys.platform == 'win32':
            for iface_ip in self.iface_ips:
                new_socket = socket.socket(family=self.addr_family, type=socket.SOCK_DGRAM)
                new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                new_socket.bind((iface_ip, self.port))

                
                self.add_memberships(new_socket, self.multicast_ips, self.iface_infos[iface_ip], self.addr_family)

                # On Windows, by default, sent packets are looped back to local sockets on the same interface, even for interfaces
                # that are not loopback.Change this by disabling IP_MULTICAST_LOOP unless the loopback interface is used or
               
               
                self.sockets.append(new_socket)
        else:
                # For IPv4, on the systems I tested at least, you can get away with subscribing to multiple
                # interfaces on one socket.
                
            iface_ip_groups = [self.iface_ips]

            for iface_ips_this_group in iface_ip_groups:

                new_socket = socket.socket(family=self.addr_family, type=socket.SOCK_DGRAM)
                new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                    
                new_socket.bind((multicast_ip, self.port))

                for iface_ip in iface_ips_this_group:    
                    self.add_memberships(new_socket, [multicast_ip], self.iface_infos[iface_ip])

                self.sockets.append(new_socket)

        self.is_opened = True

        

        
    def __del__(self):
        if self.is_opened:
            self.free_sockets()

    def free_sockets(self):
        for socket in self.sockets:
            socket.close()
        self.is_opened = False

    def recvfrom(self, bufsize: int = 4096, flags: int = 0)->Tuple[bytes, Tuple[str,int]]:
        """
        Receive a UDP packet from the socket, returning the bytes and the sender address.
        This respects the current blocking and timeout settings.

        The "bufsize" and "flags" arguments have the same meaning as the arguments to socket.recv(), see the
        manual for that function for details.
        ret -> (received bytes, ipaddr, port)
       
        """

        # Select finds the socket that is ready for reading
        # Description says: Waits until one or more file descriptors are ready for some kind of I/O.
        #On windows it only works for sockets which is what we need

        print("receiving")
        
        read_list, write_list, exception_list = select.select(self.sockets, [], [], self.timeout) 

        if len(read_list) == 0:
            # No data to read
            return None

        # Since we only want to return one packet at a time, just pick the first readable socket.
        return cast(Tuple[bytes, Tuple[str,int]], read_list[0].recvfrom(bufsize, flags))

    


    def add_memberships(self,multicast_socket: socket.socket, multicast_ips: List[str], interface_info: InterfaceInfo) -> None:
        """
        Add a non-source-specific membership for the given multicast IPs on the given socket.
        """

        for multicast_addr in multicast_ips:
            if sys.platform == 'win32':
                #as per: https://docs.microsoft.com/en-us/windows/win32/winsock/ipproto-ip-socket-options
                #struct packin for windows 

                packed_mreq = struct.pack("!4sI", 
                                         socket.inet_aton(multicast_addr), 
                                         interface_info.interface_index)
                
                multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, packed_mreq)
                
            else:
                #ip_mreqn structure for joining the multicast group, might not work on older kernels(before 2.2)
                # as per: https://linux.die.net/man/7/ip
                #struct packin for unix pased
                
                packed_mreq = struct.pack('@4s4si',
                                         socket.inet_aton(multicast_addr), #  multicast group  address
                                         socket.inet_aton(interface_info.interface_ip), # local interface address
                                         interface_info.interface_index) 
                
                multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, packed_mreq)
                

    


  
