from test.helper import (
    execute_add,
    command_factory,
)


def test_switch(daemon_setup):
    """Switch the position of two commands in the queue."""
    command_factory('pause')()
    execute_add('ls')
    execute_add('ls -l')
    command_factory('switch')({'first': 0, 'second': 1})
    status = command_factory('status')()
    assert status['data'][0]['command'] == 'ls -l'
    assert status['data'][1]['command'] == 'ls'


def test_switch_fails(daemon_setup):
    """Switching the position of a not existing command fails."""
    response = command_factory('switch')({'first': 0, 'second': 1})
    assert response['status'] == 'error'


def test_switch_running(daemon_setup):
    """Switching the position of running command fails."""
    execute_add('sleep 60')
    execute_add('ls -l')
    response = command_factory('switch')({'first': 0, 'second': 1})
    assert response['status'] == 'error'
