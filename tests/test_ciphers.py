'''test pysftp.Connection ciphers param and CnOpts.ciphers - uses py.test'''
from __future__ import print_function
# these can not use fixtures as we need to set ciphers prior to the connection
# being made and fixtures are already active connections.
import pytest

from common import SFTP_REBEX
import pysftp


def test_no_ciphers_param():
    '''test the ciphers parameter portion of the Connection is gone.'''
    args = SFTP_REBEX()
    args['ciphers'] = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc',
                       'arcfour256')
    with pytest.raises(TypeError):
        pysftp.Connection(**args)


def test_ciphers_cnopts():
    '''test the ciphers attribute portion of the CnOpts'''
    args = SFTP_REBEX()
    args['cnopts'].ciphers = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc',
                              'arcfour256')
    with pysftp.Connection(**args) as sftp:
        for cipher in sftp.active_ciphers:
            assert cipher in args['cnopts'].ciphers


def test_active_ciphers():
    '''test that method returns a tuple of strings, that show ciphers used'''
    args = SFTP_REBEX()
    args['cnopts'].ciphers = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc',
                              'arcfour256')
    with pysftp.Connection(**args) as sftp:
        local_cipher, remote_cipher = sftp.active_ciphers
    assert local_cipher in args['cnopts'].ciphers
    assert remote_cipher in args['cnopts'].ciphers
