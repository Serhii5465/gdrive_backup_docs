import sys
import argparse
import datetime
import os
import subprocess
from pathlib import Path
from typing import Dict 
from src import constants

def create_dir(dir: str) -> None:
    Path(dir).mkdir(parents=True, exist_ok=True)

def mode_label_op(message: str, path_log_file: str) -> None:
    message = message + '\n'
    print(message)

    f = open(path_log_file, 'a')
    f.write(message)
    f.close()

def parse_args() -> Dict[str, bool]:
    """
    Handles command-line options to select the script's mode.
    Returns:
        Dictionary with active mode
    """
    parser = argparse.ArgumentParser(description='Selecting the operating mode of the rclone utility')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--upload', action='store_true', help='Uploads files')
    group.add_argument('-d', '--download', action='store_true', help='Downloads files')

    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])
    
    return args

def upload_to_gdrive() -> None:
    """
    Checking all paths for validity and uploading files from local folder to Google Drive.
    Under normal conditions the process finishes work and has an exit code of 0.
    Otherwise, the process has an exit code different from 0 and the script terminates.
    """
    args = parse_args()
    
    log_file = os.path.join(constants.RCLONE_LOGS_DIR, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log')

    command = ['rclone', 'sync', '--dry-run', '--progress', '--verbose', f'--config={constants.RCLONE_CONF_FILE}', f'--log-file={log_file}']
    
    if args['upload']:
        #: Checking for the presence of the local root folder with documents
        try:
            dirs = os.listdir(constants.PATH_SYNC_DIR)
        except FileNotFoundError:
            sys.exit(f'Directory {constants.PATH_SYNC_DIR} is missing')
        else:
            if len(dirs) == 0:
                raise IndexError(f'Directory {constants.PATH_SYNC_DIR} is empty')

        command.insert(4, constants.PATH_SYNC_DIR)
        command.insert(5, constants.ROOT_REMOTE_DIR)

    if args['download']:
        #: Checking for the presence of the remote root folder with documents on Google Drive
        is_rem_dir_empty = subprocess.run(['rclone', f'--config={constants.RCLONE_CONF_FILE}', 'lsf', constants.ROOT_REMOTE_DIR], capture_output=True, text=True)
        if not is_rem_dir_empty.stdout:
            raise FileNotFoundError('Source directory on Google Drive is empty')

        if not os.path.exists(constants.PATH_SYNC_DIR):
            create_dir(constants.PATH_SYNC_DIR)
            print(f'Creating directory {constants.PATH_SYNC_DIR}')

        command.insert(4, constants.ROOT_REMOTE_DIR)
        command.insert(5, constants.PATH_SYNC_DIR)

    create_dir(constants.RCLONE_LOGS_DIR)

    mode_label_op('Running Rclone in dry run mode', log_file)

    if subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout).returncode != 0:
        raise RuntimeError('Error\nCheck logs')

    command.remove('--dry-run')

    mode_label_op('\nUploading mode', log_file)

    if subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout).returncode != 0:
        raise RuntimeError('Error\nCheck logs')
    else:
        print('\nSuccess')


def main() -> None:
    if not os.path.exists(constants.RCLONE_CONF_FILE):
        raise FileNotFoundError('Rclone\'s config file is missing')
    
    upload_to_gdrive()

if __name__ == "__main__":
    main()