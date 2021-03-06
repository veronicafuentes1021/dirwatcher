#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = 'Veronica Fuentes'

import sys
import signal
import time
import datetime
import os
import logging
import argparse


exit_flag = False
filesfound = []
magic_word_position = {}
logger = logging.getLogger(__file__)


def search_for_magic(path, filename, start_line, magic_string):
    global magic_word_position
    with open(path + '/' + filename) as f:
        for i, line in enumerate(f.readlines(), 1):
            if magic_string in line and i > magic_word_position[filename]:
                logger.info('Magic word {} on line {} in file {}'
                            .format(magic_string, i, filename))
            if i > magic_word_position[filename]:
                magic_word_position[filename] += 1


def watch_directory(path, magic_string, extension, interval):
    global filesfound
    global magic_word_position
    logger.info('Watching dir {}, magic string: {}, extension: {},interval: {}'
                .format(path, magic_string, extension, interval))
    directory = os.path.abspath(path)
    file_in_dir = os.listdir(directory)
    for f in file_in_dir:
        if f.endswith(extension) and f not in filesfound:
            logger.info('new file: {} found in {}'.format(f, path))
            filesfound.append(f)
            magic_word_position[f] = 0
    for f in filesfound:
        if f not in file_in_dir:
            logger.info('file {} not found in {}'.format(f, path))
    for f in filesfound:
        search_for_magic(path, f, 0, magic_string)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, help="directory to watch")
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help="file extension to search for")
    parser.add_argument('-i', '--int', type=float, default=1,
                        help='polling interval')
    parser.add_argument('-magic', help='magic text to watch for')
    return parser


def signal_handler(sig_num, frame):
    global exit_flag
    signals = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signals[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True
    return


def main(args):
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s'
        '[%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    start_time = datetime.datetime.now()

    logger.info(
        '\n' +
        '-' * 80 +
        f'\n\tRunning {__file__}\n' +
        f'\nStarted on{start_time.isoformat()}\n' +
        '-' * 80
    )

    parser = create_parser()
    args = parser.parse_args()
    print(args)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not exit_flag:
        try:
            watch_directory(args.dir, args.magic, args.ext, args.int)
        except OSError:
            logger.error('Directory {} does not exist'.format(args.dir))
            # logger.error(e)
            time.sleep(args.int * 2)
        except Exception as e:
            logger.error('Unhandled exception:{}'.format(e))
        time.sleep(args.int)
    total = datetime.datetime.now()-start_time

    logger.info(
        '\n' +
        '-' * 80 +
        f'\n\tRunning {__file__}\n' +
        f'\nStarted on{str(total)}\n' +
        '-' * 80
    )


if __name__ == '__main__':
    main(sys.argv[1:])
