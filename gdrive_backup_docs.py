import sys
import argparse
import datetime
import os
import subprocess
import rclone_const
from pathlib import Path
from typing import Dict 

def create_dir(dir: str) -> None:
    Path(dir).mkdir(parents=True, exist_ok=True)

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


def upload_to_gdrive(logs_dir: str, docs_dir: str) -> None:
    """
    Checking all paths for validity and uploading files from local folder to Google Drive.
    Under normal conditions the process finishes work and has an exit code of 0.
    Otherwise, the process has an exit code different from 0 and the script terminates.
    Args:
        logs_dir (str): The path to the directory where log files will be saved.
        docs_dir (str): The path to the local folder containing documents.
    """
    args = parse_args()
    
    command = ['rclone', 'sync', '--progress', '--verbose', '--config=' + rclone_const.RCLONE_CONF_FILE(),
                '--log-file=' + logs_dir + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log']
    
    if args['upload']:
        #: Checking for the presence of the local root folder with documents
        try:
            dirs = os.listdir(docs_dir)
        except FileNotFoundError:
            sys.exit('Directory ' + docs_dir + ' is missing')
        else:
            if len(dirs) == 0:
                raise IndexError('Directory ' + docs_dir + ' is empty')

        command.insert(4, docs_dir)
        command.insert(5, rclone_const.ROOT_REMOTE_DIR())

    if args['download']:
        #: Checking for the presence of the remote root folder with documents on Google Drive
        is_rem_dir_empty = subprocess.run(['rclone', 'lsf', rclone_const.ROOT_REMOTE_DIR()], capture_output=True, text=True)
        if not is_rem_dir_empty.stdout:
            raise FileNotFoundError('Source directory on Google Drive is empty')

        if not os.path.exists(docs_dir):
            create_dir(docs_dir)
            print('Creating directory ' + docs_dir)

        command.insert(4, rclone_const.ROOT_REMOTE_DIR())
        command.insert(5, docs_dir.stdout.strip('\n'))

    create_dir(logs_dir)

    out = subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)
    if out.returncode != 0:
        raise RuntimeError('Error\nCheck logs')
    else:
        print('\nSuccess')


def main() -> None:
    if not os.path.exists(rclone_const.RCLONE_CONF_FILE()):
        raise FileNotFoundError('Rclone\'s config file is missing')
    
    mnt = rclone_const.MOUNT_POINTS()

    if mnt:
        upload_to_gdrive(mnt + 'logs\\rclone_gdrive_documents\\', mnt + rclone_const.ROOT_LOCAL_DIR())

main()