import os
import time
import logging
import subprocess

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers.api import DEFAULT_OBSERVER_TIMEOUT


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class COLORS(object):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class RSyncEventHandler(FileSystemEventHandler):
    """RSync when the events captured."""

    def __init__(self, current_path, remote_path, rsync_options=''):
        self.current_path = current_path
        self.remote_path = remote_path
        self.rsync_options = rsync_options.split()
        self.rsync()

    @staticmethod
    def log(log, color):
        logging.info('{}{}{}'.format(color, log, COLORS.END))

    def on_moved(self, event):
        super(RSyncEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        self.log('Moved {}: from {} to {}'.format(what,
                                                  event.src_path,
                                                  event.dest_path),
                 COLORS.BLUE)

        self.rsync()

    def on_created(self, event):
        super(RSyncEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        self.log('Created {}: {}'.format(what, event.src_path),
                 COLORS.GREEN)

        self.rsync()

    def on_deleted(self, event):
        super(RSyncEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        self.log('Deleted {}: {}'.format(what, event.src_path),
                 COLORS.RED)

        self.rsync()

    def on_modified(self, event):
        super(RSyncEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        self.log('Modified {}: {}'.format(what, event.src_path),
                 COLORS.YELLOW)

        self.rsync()

    def rsync(self):
        self.log('RSyncing', COLORS.PURPLE)
        cmd = 'rsync -avzP {} {} {}'.format(
            ' '.join(self.rsync_options), self.current_path, self.remote_path
        )
        self.log(cmd, COLORS.BOLD)
        with open(os.devnull, 'w') as DEVNULL:
            subprocess.call(['rsync', '-avzP'] + self.rsync_options
                            + [self.current_path, self.remote_path],
                            stdout=DEVNULL,
                            stderr=subprocess.STDOUT)


@click.command()
@click.argument('current-path')
@click.argument('remote-path')
@click.option('--observer-timeout',
              default=DEFAULT_OBSERVER_TIMEOUT,
              help='The observer timeout, default {}'.format(
                  DEFAULT_OBSERVER_TIMEOUT
              ))
@click.option('--rsync-options', default='', help='rsync command options')
def main(current_path, remote_path,
         observer_timeout, rsync_options):
    event_handler = RSyncEventHandler(current_path, remote_path, rsync_options)
    observer = Observer(timeout=observer_timeout)
    observer.schedule(event_handler, current_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
