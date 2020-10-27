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
import signal


exit_flag = False
filesfound = []
magic_word_position = {}
logger = logging.getLogger(__file__)


def search_for_magic(path, filename, start_line, magic_string):
    global magic_word_pos
    with open(path + '/' + filename) as f:
        for i, line in enumerate(f.readlines(), 1):
            if magic_string in line and i > magic_word_pos[filename]:
                logger.info('Woohoo! Magic word {} on line {} in file {}'
                            .format(magic_string, i, filename))
            if i > magic_word_pos[filename]:
                magic_word_pos[filename] += 1


def watch_directory(path, magic_string, extension, interval):
    global filesfound
    global magic_word_pos
    logger.info('Watching dir {}, magic string: {}, extension: {},interval: {}'
                .format(path, magic_string, extension, interval))
    directory = os.path.abspath(path)
    file_in_dir = os.listdir(directory)
    for f in file_in_dir:
        if f.endswith(extension) and f not in filesfound:
            logger.info('new file: {} found in {}'.format(f, path))
            filesfound.append(f)
            magic_word_pos[f] = 0
    for f in filesfound:
        if f not in file_in_dir:
            logger.info('file {} not found in {}'.format(f, path))
    for f in filesfound:
        search_for_magic(path, f, 0, magic_string)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Watches specified directory for a specific input.')
    parser.add_argument(
        '-d', '--dir', type=str
        help='directory to watch')
    parser.add_argument(
        'input',
        help='input to watch directory for')
    parser.add_arguemnt(
        '-e', '--ext', type=str
        help='file extention to search', default='.txt')
    parser.add_arguemnt(
        '-i', '--interval',
        help='poll interval, defaults to 1 sec', type=float, default=1.0)
    return parser


def signal_handler(sig_num, frame):
    global exit_flag
    signals = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warn('Received ' + signals[sig_num]
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
        '\n'
        '-------------------------------------------------------------------\n'
        '    Running {0}\n'
        '    Started on {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, start_time.isoformat())
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
        '\n'
        '-------------------------------------------------------------------\n'
        '    Stopped {0}\n'
        '    Total time was {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(Total))
    )


if __name__ == '__main__':
    main(sys.argv[1:])
