#!/usr/bin/env python3
"""
    Regex-ing
"""
import logging
import mysql.connector
import os
import re
from typing import List, Tuple


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get a point of connection toward the database

        Return:
            a connector to the database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passw = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    hosting = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    medb = mysql.connector.connect(
        host=hosting,
        username=username,
        password=passw,
        database=db
    )

    return medb


def get_logger() -> logging.Logger:
    """
        Return:
            returns a logging.Logger object
    """
    log: logging.Logger = logging.getLogger('user_data')
    log.propagate = False

    stream_handler: logging.StreamHandler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter((RedactingFormatter(fields=PII_FIELDS)))
    stream_handler.formatter(formatter)

    log.addHandler(stream_handler)

    return log


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
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            Set the format of the record

            Args:
                record: Log record of a event

            Return:
                The function overloaded to make a new log with all items
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)

        return (super(RedactingFormatter, self).format(record))


if __name__ == '__main__':
    main()
