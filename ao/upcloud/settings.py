from ao import settings

def get_setting(name, default):
    name = 'UPCLOUD_' + name
    return getattr(settings, name, default)


AUTHENTICATION_LEVEL = get_setting('AUTHENTICATION_LEVEL', 0)
CREATION_LEVEL = get_setting('AUTHENTICATION_LEVEL', 0)

SERVER_ACCESS_LEVEL = get_setting('SERVER_ACCESS_LEVEL', 0)
SERVER_ACTION_LEVEL = get_setting('SERVER_ACTION_LEVEL', 0)
SERVER_STOP_DELAY = get_setting('SERVER_STOP_DELAY', 1)
SERVER_START_DELAY = get_setting('SERVER_RESTART_DELAY', 1)
SERVER_RESTART_DELAY = get_setting('SERVER_RESTART_DELAY', 1)

IP_ADDRESS_ACCESS_LEVEL = get_setting('IP_ADDRESS_ACCESS_LEVEL', 0)
IP_ADDRESS_ACTION_LEVEL = get_setting('IP_ADDRESS_ACTION_LEVEL', 0)
