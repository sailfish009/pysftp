'''test pysftp.Connection.timeout - uses py.test'''

from common import SFTP_REBEX
import pysftp


def test_timeout_getter():
    '''test getting the timeout value'''
    with pysftp.Connection(**SFTP_REBEX()) as sftp:
        # always starts at no timeout,
        assert sftp.timeout is None


def test_timeout_setter(rsftp):
    '''test setting the timeout value'''
    rsftp.timeout = 10.5
    assert rsftp.timeout == 10.5
    rsftp.timeout = None
    assert rsftp.timeout is None


def test_timeout_cnopts():
    '''test setting the timeout value via CnOpts'''
    args = SFTP_REBEX()
    args['cnopts'].timeout = 3.7
    with pysftp.Connection(**args) as sftp:
        # always starts at no timeout,
        assert sftp.timeout == 3.7
