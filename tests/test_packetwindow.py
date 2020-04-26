'''test the default_window_size and default_max_packet_size'''

from paramiko.common import DEFAULT_WINDOW_SIZE, DEFAULT_MAX_PACKET_SIZE

from common import SFTP_REBEX
import pysftp


def test_defaults(rsftp):
    '''test the default window and packet size values'''
    channel = rsftp.sftp_client.get_channel()
    assert channel.in_window_size == DEFAULT_WINDOW_SIZE
    assert channel.in_max_packet_size == DEFAULT_MAX_PACKET_SIZE


def test_windowpacket_cnopts():
    '''test setting the window/packet values via CnOpts'''
    args = SFTP_REBEX()
    args['cnopts'].default_max_packet_size = 4096
    args['cnopts'].default_window_size = 8 * 4096
    with pysftp.Connection(**args) as sftp:
        channel = sftp.sftp_client.get_channel()
        assert channel.in_max_packet_size == 4096
        assert channel.in_window_size == 8 * 4096
