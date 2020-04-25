
=============
pysftp.CnOpts
=============
The goal of pysftp is to make using Secure File Transfer Protocol as simple as
possible for the vast majority of cases.  However, due to the underlying
complexity there are times when you might need to get a little more technical
to achieve your goals.

There are a myriad of options that can be modified and over time, users have
requested the ability to modify certain options to overcome a specific problem
that may be unusual to most, but was preventing them from achieving their goal
of solving a particular problem.  In answering those requests, pysftp ended up
adding more and more parameters to the .Connection method.  This resulted in
an ever growing list of options that most would never use and in the process
complicating the .Connection method parameter list.

As a solution to simplifying the .Connection method and keeping it relatively
clean but yet allowing for previously exposed options to remain available, and
allow for future option additions, I decided that the main parameters used by
the .Connection method would be specifying the host and the requisite
authentication information.  Everything else would move out to a compound data
structure -- a/k/a pysftp.CnOpts.


The following two code blocks are equivalent:

.. code-block:: python

    import pysftp
    cnopts = pysftp.CnOpts()
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        # do something
       pass

    with pysftp.Connection(host, username, password=password) as sftp:
        # do something
       pass


If no cnopts is passed to the .Connection method, then it creates and uses a
default CnOpts object.


CnOpts.hostkeys
---------------
HostKey checking is probably the most likely option that you will use.  As of
pysftp 0.2.9 HostKey checking is enabled by default.  

By default, pysftp will
look for and load hostkeys from your `~/.ssh/known_hosts` file.  If it fails
to find a known_hosts file at the normal location it will raise a warning. You
will either need to load a specific known_hosts file from a different location
or (not recommended) disable hostkey checking.

To silence the warning because you already know that your file holding known
host keys is located some place else, you can specify that file when you
instantiate CnOpts by:

.. code-block:: python

    import pysftp
    cnopts = pysftp.CnOpts(knownhosts='/path/to/your/known_hosts')

If the known_hosts file is found, but no hostkeys are in it, an SSHException
is raised because you will not be able to connect to any host because no
hostkeys are available.

If you wish to disable hostkey checking, then this is the recipe: (Please do
not use this, read a bit further and a better solution will be presented.)

.. code-block:: python

    import pysftp
    cnopts = CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        # HostKey checking is now disabled.
       pass

CnOpts.hostkeys is a paramiko.hostkeys.HostKeys object and all methods are
available.

If you are not in control of the known_hosts file on the target machine, you
can create your own known_hosts file and distribute with your code.  This
known_hosts file can be named anything but must be in the standard known_hosts
format.  You could make a copy of your local known_hosts file then remove all
the other hostkeys in the copy, leaving only the hostkey you want to
distribute.   You could also create a file programmaticaly, i.e.

.. code-block:: python

    import pysftp
    cnopts = CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        # HostKey checking is now disabled.
       myhostkeys = pysftp.HostKeys()  # an empty hostkeys object
       myhostkeys.add(host, sftp.remote_server_key.get_name(), sftp.remote_server_key) # add key
       myhostkeys.save('myhost.pub')   # save single hostkey to a file


You know have a seperate known_host format file, 'myhost.pub' that you can
distribute with your code.  It would be used like this:


.. code-block:: python

    import pysftp
    cnopts = CnOpts(knownhosts='myhost.pub')
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        # HostKey checked using information in myhost.pub
       pass


You could wish to augment any existing knownhost information by loading your
knownhost file after the default `~/.ssh/known_hosts` file is processed by:


.. code-block:: python

    import pysftp
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('myhost.pub')  # key merged into .hostkeys

.load works the same as .add, in that if the key doesn't exist it is added, if
it does exist, then it is overwritten with the new information.


CnOpts.log
----------
type: bool|str(path)

By default, is False and no log file is created.  If set to True, then a temp
file is created and used for logging.  You can get the name of the temp log
file with .Connection().logfile .  Logging is often helpful if you are
encountering issues connecting to or transferring files.

.. code-block:: python

    from __future__ import print_function
    import pysftp
    cnopts = CnOpts()
    cnopts.log = True
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        print(sftp.logfile)  # prints the path and name of the temp logfile


If you wish to log to a specific file, you can do that by setting .log to that
filepath.


.. code-block:: python

    from __future__ import print_function
    import pysftp
    cnopts = CnOpts()
    cnopts.log = '/path/to/my/logfile'
    with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
        print(sftp.logfile)  # prints '/path/to/my/logfile'


CnOpts.compression
------------------
type: bool

Defaults to `False`.  Set to `True` to enable.  A little code to demonstrate:

.. code-block:: pycon

    >>> from __future__ import print_function
    >>> import pysftp
    >>> with pysftp.Connection(host, username, password=password) as sftp:
    ...   print(sftp.active_compression) # prints a tuple of local,remote compression in use
    ... 
    ('none', 'none')
    >>> cnopts = pysftp.CnOpts()
    >>> cnopts.compression = True
    >>> with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
    ...   print(sftp.active_compression)
    ... 
    ('zlib@openssh.com', 'zlib@openssh.com')


CnOpts.ciphers
--------------
type: tuple(str)

It is important to note that you can not add ciphers with this option.  You
can affect the order that ciphers are attempted or to remove specific ciphers
from being used.


.. code-block:: pycon

    >>> from __future__ import print_function
    >>> import pysftp
    >>> with pysftp.Connection(host, username, password=password) as sftp:
    ...     sec_opts = sftp.security_options
    ...     print(sec_opts.ciphers)
    ...
    ('aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'aes128-cbc', 'blowfish-cbc',
    'aes192-cbc', 'aes256-cbc', '3des-cbc', 'arcfour128', 'arcfour256')


Ok, as an example and not a recommendation, lets limit the ciphers to just the
aes variety.


.. code-block:: pycon

    >>> from __future__ import print_function
    >>> import pysftp
    >>> desired = ('aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'aes128-cbc',
    ... 'aes192-cbc', 'aes256-cbc')
    >>> cnopts = pysftp.CnOpts()
    >>> cnopts.ciphers = desired
    >>> with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
    ...     sec_opts = sftp.security_options
    ...     print(sec_opts.ciphers)
    ...
    ('aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'aes128-cbc', 'aes192-cbc', 'aes256-cbc')


So your client now advertises a subset of ciphers available and then the
server and client negotiate based on those ciphers.  If you limit your ciphers
and the server can't match atleast one, you will encounter problems. An
SSHException will be raised, `paramiko.ssh_exception.SSHException: Incompatible
ssh server (no acceptable ciphers)`


CnOpts.timeout
--------------
type: float

Although you could set or retrieve the timeout via pysftp.Connection.timeout
property since v0.2.7 there was request to allow setting the timeout via the
CnOpts parameter.  Now you can use either or both methods.

.. code-block:: pycon

    >>> from __future__ import print_function
    >>> import pysftp
    >>> cnopts = pysftp.CnOpts()
    >>> cnopts.timeout = 60.0  # by default, timeout is None, no timeout.
    >>> with pysftp.Connection(host, username, password=password, cnopts=cnopts) as sftp:
    ...     print(sftp.timeout)
    ...
    60.0

CnOpts.default_window_size
--------------------------
type: int

The default value is `paramiko.common.DEFAULT_WINDOW_SIZE` (2097152)

**Modify at your own risk**

.. danger::
    From the Paramiko documentation: 
        Modifying the the window and packet sizes might have adverse effects on your
        channels created from this transport. The default values are the same as in the
        OpenSSH code base and have been battle tested.

CnOpts.default_max_packet_size
------------------------------
type: int

The default value is `paramiko.common.DEFAULT_MAX_PACKET_SIZE` (32768)

**Modify at your own risk**

.. danger::
    From the Paramiko documentation: 
        Modifying the the window and packet sizes might have adverse effects on your
        channels created from this transport. The default values are the same as in the
        OpenSSH code base and have been battle tested.



