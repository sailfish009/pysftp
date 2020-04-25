'''test that exceptions return what is expected'''

from pysftp.exceptions import ConnectionException


def test_connectionexception_msg():
    '''test that the connection exception message is intended.'''
    exc = ConnectionException('host', 'port')
    assert exc.message == "Could not connect to host:port"
