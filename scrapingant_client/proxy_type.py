from enum import Enum


class ProxyType(str, Enum):
    datacenter = 'datacenter'
    residential = 'residential'
