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


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


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
    # Your code here
    return


def main(args):
    # Your code here
    return


if __name__ == '__main__':
    main(sys.argv[1:])
