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
    group.add_argument('-u', '--upload', action='store_true', help='Uploads files from the local directory "documents" to Google Drive')
    group.add_argument('-d', '--download', action='store_true', help='Downloads files from Google Drive (directory "docs") to the local directory "documents"')

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
    
    #: Converting Unix-like path to Windows form by using Cygpath.exe utility.
    win_style_path_sync_dir = subprocess.run(['cygpath', '--windows', docs_dir], capture_output=True, text=True)
    win_style_path_logs_dir = subprocess.run(['cygpath', '--windows', logs_dir], capture_output=True, text=True)

    command = ['rclone', 'sync', '--progress', '--verbose',
                '--log-file=' + win_style_path_logs_dir.stdout.strip('\n') + datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S") + '.log']
    
    if args['upload']:
        #: Checking for the presence of the local root folder with documents
        try:
            dirs = os.listdir(docs_dir)
        except FileNotFoundError:
            sys.exit('Directory ' + docs_dir + ' is missing')
        else:
            if len(dirs) == 0:
                raise IndexError('Directory ' + docs_dir + ' is empty')

        command.insert(4, win_style_path_sync_dir.stdout.strip('\n'))
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
        command.insert(5, win_style_path_sync_dir.stdout.strip('\n'))

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

    upload_to_gdrive(mnt + 'logs/rclone_gdrive_documents/', mnt + 'documents/')

main()