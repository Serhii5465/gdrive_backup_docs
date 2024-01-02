import os
import sys
import argparse
import datetime
from pathlib import Path
from py_exec_cmd import exec_cmd
from typing import List, Dict


def check_files(*list_files: List[str]) -> None:
    """
    Verifies if the path to a folder or file is valid. If at least one path is broken,
    the script terminates.
    Args:
        *list_files: List of full paths to folders and files.
    """
    for i in list_files:
        if not os.path.exists(i):
            msg = i + " doesn't exists"
            sys.exit(msg)


def parse_args() -> Dict[str, bool]:
    """
    Handles command-line options to select the script's modeю.
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


def upload_to_gdrive(sync_dir: str, logs_dir: str) -> None:
    """
    Uploads files from local folder to Google Drive.
    Under normal conditions the process finishes work and has an exit code of 0.
    Otherwise, the process has an exit code different from 0 and the script terminates.
    Args:
        sync_dir: Path to the synchronized folder.
        logs_dir: Path to the logs folder.
    """
    args = parse_args()
    
    #: Converting Unix-like path to Windows form by using Cygpath.exe utility.
    win_style_path_sync_dir = exec_cmd.get_cmd_out(['cygpath', '--windows', sync_dir])
    win_style_path_logs_dir = exec_cmd.get_cmd_out(['cygpath', '--windows', logs_dir])

    command = ['rclone', 'sync', '--progress', '--verbose',
                '--log-file=' + win_style_path_logs_dir.stdout.strip('\n') + '/' + datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S") + '.log']

    if args['upload']:
        command.insert(4, win_style_path_sync_dir.stdout.strip('\n'))
        command.insert(5, 'google-drive:')

    elif args['download']:
        command.insert(4, 'google-drive:')
        command.insert(5, win_style_path_sync_dir.stdout.strip('\n'))

    out = exec_cmd.run_cmd(command)

    if out.returncode != 0:
        sys.exit('Error\nCheck logs')
    else:
        print('\nGood')


def main() -> None:
    rclone_conf = str(Path.home()) + '/.config/rclone/rclone.conf'
    sync_dir = '/cygdrive/e/documents'

    check_files(rclone_conf, sync_dir)

    logs_dir = '/cygdrive/e/logs/rclone/'
    Path(logs_dir).mkdir(parents=True, exist_ok=True)

    upload_to_gdrive(sync_dir, logs_dir)


main()