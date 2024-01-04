from pathlib import Path

def RCLONE_CONF_FILE() -> str:
    return str(Path.home()) + '/.config/rclone/rclone.conf'

def DOCS_DIR() -> str:
    return '/cygdrive/e/documents'

def ROOT_REMOTE_DIR() -> str:
    return 'google-drive:'

def LOGS_DIR() -> str:
    return '/cygdrive/e/logs/rclone/'
