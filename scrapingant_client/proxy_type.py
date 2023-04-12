from enum import Enum


class ProxyType(str, Enum):
    datacenter = 'datacenter'
    residential = 'residential'

    def __str__(self):
        return self.value
