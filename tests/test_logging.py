'''test pysftp.Connection logging param and CnOpts.log - uses py.test'''
from __future__ import print_function
import os

import pytest

from common import VFS, conn, SFTP_REBEX
import pysftp


def test_removed_log_param():
    '''test Connection log parameter removed'''
    args = SFTP_REBEX()
    args['log'] = True
    with pytest.raises(TypeError):  # pylint:disable=e1101
        pysftp.Connection(**args)


def test_log_cnopt_user_file():
    '''test .logfile returns temp filename when CnOpts.log is set to a
    user file.'''
    args = SFTP_REBEX()
    args['cnopts'].log = os.path.expanduser('my-logfile1.txt')
    with pysftp.Connection(**args) as sftp:
        sftp.listdir()
        assert sftp.logfile == args['cnopts'].log
        assert os.path.exists(sftp.logfile)
        logfile = sftp.logfile
    # cleanup
    os.unlink(logfile)


def test_log_cnopts_explicit_false(rsftp):
    '''test .logfile returns false when CnOpts.log is set to false'''
    assert rsftp.logfile is False


def test_log_cnopts_true(sftpserver):
    '''test .logfile returns temp filename when CnOpts.log is set to True'''
    args = conn(sftpserver)
    args['cnopts'].log = True
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**args) as sftp:
            sftp.listdir()
            assert os.path.exists(sftp.logfile)
            # and we are not writing to a file named 'True'
            assert sftp.logfile == args['cnopts'].log
            assert not isinstance(sftp.logfile, bool)
            logfile = sftp.logfile
        # cleanup
        os.unlink(logfile)
