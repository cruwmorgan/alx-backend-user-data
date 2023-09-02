#!/usr/bin/env python3
"""
    Regex-ing
"""
import logging
import re
from typing import List, Tuple


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """
        Filter and obfuscated the string

        Args:
            fields: a list of strings representing all fields to obfuscate
            redaction: a string representing by what the field will
                be obfuscated
            message: a string representing the log line
            separator: a string representing by which character is
                    separating all fields in the log line (message)
        Return:
            String with string obfuscated
    """
    pattern = f'({separator.join(fields)})=[^{separator}]+'
    return re.sub(pattern, f'\\1={redaction}', message)
