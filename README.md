# auto-rsync

Auto RSync files by watch filesystem events.

## USAGE

    $ auto-rsync --help
    
    Usage: auto_rsync.py [OPTIONS] CURRENT_PATH REMOTE_PATH
    
    Options:
      --observer-timeout INTEGER  The observer timeout, default 1
      --rsync-options TEXT        rsync command options
      --help                      Show this message and exit.

## EXAMPLE

    $ auto-rsync ./test username@host:/home/username/test --rsync-options='--delete --excludes=*.pyc'
