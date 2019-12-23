# Pigrizia

## What this is

Pigrizia is a library to make it easy to do things like automation,
monitoring and reporting. It is currently in very early development
but I am working quite intensively on it.

I am writing this because I need it and my poor old brain can figure out
how to make big, serious tools like Ansible or Fabric to work for me. So
I began working on my own.

At the same time as I'm developing this for work, I am also having a lot
of fun with it. And I decided to learn things about Python that I've never
really thought about before, such as documentation, testing and deployment.
In other words, my first attempt at a "serious" Python project.

Just bear in mind that I'm prioritizing things that I need for work. And
I will only fix things when they become a problem to me, unless somebody
reports a bug. Pull requests are more than welcome.

## Why the name?

Pigrizia means "laziness" in my native language and I develop with the
mind of being able to be lazy in the future. I basically want to write
tools that do most of the hard work for me.

## Installation

The following should work, though things may be broken at times (read:
most of the time):

    (.venv) % pip install pip+https://github.com/lcabrini/pigrizia

## Using it

As I said, there is not much here at the moment. There is some initial
API documentation, but for now, you are probably better off just reading
the code. Anyways, here is some stuff you can do, assuming you have an
account on a 192.168.0.184, sudo access and the same username as your
local user.

    >>> from getpass import getpass
    >>> from pigrizia.host import get_host
    >>> passwd = getpass()
    >>> host = get_host(addr='192.168.0.100')
    >>> type(host)
    <class 'pigrizia.host.linux.Issabel'>
    >>> host.distro()
    '"centos"'
    >>> host.user_exists('lorenzo')
    True
    >>> host.user_exists('salvatore')
    False
    >>> new_passwd = getpass()
    >>> host.useradd('salvatore', new_passwd)
    >>> host.user_exists('salvatore')
    True

By not passing in an addr, you would be working locally.

    >>> host = get_host(passwd=passwd)
    >>> host.distro()
    'fedora'
    >>> host.whoami()
    'lorenzo'

If you wanted to add a user to multiple hosts, that would be (assuming
the same password on all hosts):

    >>> for addr in ('192.168.0.10', '192.168.0.11', '192.168.0.12'):
    ...     linux = Linux(addr=addr, passwd=passwd)
    ...     linux.useradd('salvatore', new_passwd)

The library really doesn't do that much more, but it is (mostly) easy to
use, at least. But I am working on this daily, so expect more functions
to be added over time.

Finally, beware that the API is going to change a lot at this early stage.
Eventually, when I get far enough to make a release, it will stabilize, 
but for now, I get an idea and implement it. Over time, I may realize that
some things annoy me, don't work like I expected, or that there is a 
simpler way to do it. When that happens, I will change things around.

## Contributing

If you would like to help a young, but ambitious project out, welcome!

I have a lot of things I need to implement because of work. Then there
are a bunch of ideas I have, that I'd like to implement. On top of that,
there are so many things that could be done that I haven't even thought 
of.

I'm currently using the issue tracker on GitHub as a sort of todo list
for myself. (At my age, I need all the memory help I can get.) If you
want to work on something, just signal me on the issue you are intersted
in.

If you peek at the code, you will see most of it is very naive. There
are a whole bunch of tests that need to be added. Parts of the code are
really clumsy and can be improved. Most of the code is not crash-proof
at all at this point.

I'm sure that much of it is not "pythonic" either. That is not really
one of my personal goals, unless "being pythonic" also happens to 
coincide with "making sense". But if you feel that the being pythonic
gives the code some intrinsic value, feel free to fix and send me pull
requests.
