"""Module to help to create tests."""
import os
import sys
from functools import wraps
from unittest.mock import MagicMock, Mock

from kytos.core import Controller
from kytos.core.config import KytosConfig
from kytos.core.connection import Connection
from kytos.core.interface import Interface
from kytos.core.switch import Switch


def get_controller_mock():
    """Return a controller mock."""
    options = KytosConfig().options['daemon']
    controller = Controller(options)
    controller.log = Mock()
    return controller


def get_interface_mock(interface_name, port, *args, **kwargs):
    """Return a interface mock."""
    switch = get_switch_mock(0x04)
    switch.connection = Mock()
    iface = Interface(interface_name, port, switch, *args, **kwargs)
    return iface


def get_switch_mock(dpid):
    """Return a switch mock."""
    return Switch(dpid)


def get_connection_mock(of_version, target_switch):
    """Return a connection mock."""
    connection = Connection(Mock(), Mock(), Mock())
    connection.switch = target_switch
    connection.protocol.version = of_version
    return connection


def get_kytos_event_mock(**kwargs):
    """Return a kytos event mock."""
    destination = kwargs.get('destination')
    message = kwargs.get('message')
    source = kwargs.get('source')

    event = MagicMock()
    event.source = source
    event.content = {'destination': destination,
                     'message': message}
    return event

def tags(*args, **kwargs):
    """Handle tokens from requests."""

    test_type = kwargs.get('type') or 'unit'
    test_size = kwargs.get('size') or 'small'
    ENV_TEST_SIZE = os.environ.get("KYTOS_TESTS_SIZE")
    ENV_TEST_TYPE = os.environ.get("KYTOS_TESTS_TYPE")

    def inner_func(func):

        @wraps(func)
        def wrapper(*args, **kwargs):        
            if test_type == ENV_TEST_TYPE and test_size == ENV_TEST_SIZE:
                return func(*args, **kwargs)
            
        return wrapper

    return inner_func
