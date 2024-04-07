import ipaddress
import json

from root import PROJECT_ROOT


class BlacklistManager:
    def __init__(self, blacklist):
        self._blacklist = blacklist

    @classmethod
    def from_file(cls):
        return BlacklistManager(cls._read_blacklist())

    def ip_is_blacklisted(self, ip: str) -> bool:
        return any(self._ip_belongs_to_network(ip, network) for network in self._blacklist)

    def _ip_belongs_to_network(self, ip: str, network: str):
        return ipaddress.ip_address(ip) in ipaddress.ip_network(network)

    @staticmethod
    def _read_blacklist():
        blacklist_path = PROJECT_ROOT / 'resources' / 'blacklist.json'
        return json.loads(blacklist_path.read_text())
