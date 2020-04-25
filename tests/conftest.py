'''session level fixtures'''
import pytest

from common import SFTP_LOCAL, SFTP_REBEX
import pysftp


@pytest.fixture(scope="session")
def lsftp(request):
    '''setup a session long connection to the local sftp server'''
    sftp = pysftp.Connection(**SFTP_LOCAL)
    request.addfinalizer(sftp.close)
    return sftp  # provide the fixture value


@pytest.fixture(scope="session")
def rsftp(request):
    '''setup a session long connection to the test.rebex.net sftp server'''
    sftp = pysftp.Connection(**SFTP_REBEX())
    request.addfinalizer(sftp.close)
    return sftp  # provide the fixture value
