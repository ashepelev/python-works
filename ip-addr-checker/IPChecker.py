__author__ = 'ash'

import re

class IPChecker:

    def is_valid(self, ip_addr):
        return self.parse_ip(ip_addr)

    def parse_ip(self, ip_addr):
        ip_addr = str(ip_addr).strip()
        if ip_addr == "":
            return False;
        word_pattern = "^.*[^0-9\.].*$"
        if re.match(word_pattern,ip_addr):
            return False
        common_ip_address_pattern = "^((0|[1]?[1-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(0|[1]?[1-9][0-9]?|2[0-4][0-9]|25[0-5])$"
        if not re.match(common_ip_address_pattern,ip_addr):
            return False
        grey_patterns = ["^10.*$",
                        "^172\.(1[6-9]|2[0-9]|3[0-1])(\.0|[1]?[1-9][0-9]?|2[0-4][0-9]|25[0-5]){2}$",
                        "^192\.168(\.0|[1]?[1-9][0-9]?|2[0-4][0-9]|25[0-5]){2}$"]
        for pattern in grey_patterns:
            if re.match(pattern,ip_addr):
                return False
        return True