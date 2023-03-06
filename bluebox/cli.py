"""cli.py

This file can be used to interactively generate tone sequences.
"""

from pathlib import Path
import argparse
import logging
import sys
from .box import Sequencer
from . import get_mf, list_mf


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        The parsed arguments.
    """

    parser = argparse.ArgumentParser(
            description='Generate tone sequences.')
    parser.add_argument(
            '-l', '--length',
            type=float,
            default=22.0,
            help='The length of each tone in milliseconds.')
    parser.add_argument(
            '-p', '--pause',
            type=float,
            default=40.0,
            help='The length of the pause between tones in milliseconds.')
    parser.add_argument(
            '-a', '--amplitude',
            type=float,
            default=1.0,
            help='The combined amplitude of the waveforms.')
    parser.add_argument(
            '-s', '--sample-rate',
            type=float,
            default=44100.0,
            help='The sample rate of the waveforms.')
    parser.add_argument(
            '-m', '--mf',
            type=str,
            default='dtmf',
            help='The MF to use e.g. dtmf, mf.')
    parser.add_argument(
            '-d', '--debug',
            action='store_true',
            help='Enable debug logging.')
    # we can have sequence or file,pipe,stdin OR interactive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
            '-f', '--file',
            type=Path,
            help='The file to read the sequence from.')
    group.add_argument(
            '-P', '--pipe',
            type=Path,
            help='Read the sequence from a pipe.')
    group.add_argument(
            '-S', '--stdin',
            action='store_true',
            help='Read the sequence from stdin.')
    group.add_argument(
            '-i', '--interactive',
            action='store_true',
            help='Enter interactive mode.')
    group.add_argument(
            'sequence',
            type=str,
            nargs='?',
            help='The sequence of tones to generate.')

    return parser.parse_args()


def bluebox_interactive(seq: Sequencer) -> None:
    """Enter interactive mode."""

    print('Entering interactive mode. Type "exit" to quit.')
    while True:
        try:
            seq(input('Sequence: '))
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception as e:
            logging.error(e)
            if seq._stop_on_error:
                break


def bluebox() -> None:
    """Generate a tone sequence.

    This function can be used to generate a tone sequence from the
    command line.
    """

    args = parse_args()

    if args.debug:
        stop_on_error = True
        logging.basicConfig(level=logging.DEBUG)
    else:
        stop_on_error = False
        logging.basicConfig(level=logging.INFO)

    if args.mf in list_mf():
        mf = get_mf(args.mf)()
    else:
        logging.error('Invalid MF: %s', args.mf)
        logging.error('Valid MFs: %s', ', '.join(list_mf()))
        sys.exit(1)

    seq = Sequencer(
            mf=mf,
            amplitude=args.amplitude,
            length=args.length,
            pause=args.pause,
            sample_rate=args.sample_rate,
            channels=1,
            stop_on_error=stop_on_error)
    if args.interactive:
        bluebox_interactive(seq)
        return
    try:
        seq(args.sequence)
    except Exception as e:
        logging.error(e)
        sys.exit(1)


if __name__ == '__main__':
    bluebox()
