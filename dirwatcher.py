#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = 'Veronica Fuentes'

import sys
from datetime import time
import os
import logging
import argparse
import signal


exit_flag = False
filesfound = []
magic_word_pos = {}
logger = logging.getLogger(__file__)


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def watch_directory(path, magic_string, extension, interval):
    file_holder = {}
    global exit_flag
    while not exit_flag:
        time.sleep(interval)
        if os.path.isdir(path):
            file_list = os.listdir(path)
            for files in file_list:
                if files.endswith(extension) and files not in file_holder:
                    file_holder[files] = 0
                    logging.info(f'file added {files}')
            key = list(file_holder.keys())
            for char in key:
                if char not in file_list:
                    print(f'This file has been removed {char}')
                    file_holder.pop(char)
            for key, value in file_holder.items():
                file_holder[key] = search_for_magic(
                    f'{path}/{key}', value, magic_string)
            print(file_holder)
        else:
            logging.error(f'{path} directory not found.')
            file_holder = {}


def create_parser():
    parser = argparse.ArgumentParser(
        description='Watches specified directory for a specific input.')
    parser.add_argument(
        'directory',
        help='directory to watch')
    parser.add_argument(
        'input',
        help='input to scan directory for')
    parser.add_arguemnt(
        '-e', '--extension',
        help='file extention to search', default='.txt')
    parser.add_arguemnt(
        '-i', '--interval',
        help='poll int, defaults to 1 sec', type=float, default=1.0)
    return parser


def signal_handler(sig_num, frame):
    logger.warn('Received ' + signal.Signals(sig_num).name)


def main(args):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    global exit_flag
    while not exit_flag:
        return


if __name__ == '__main__':
    main(sys.argv[1:])
