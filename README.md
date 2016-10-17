# auto-rsync

Auto RSync files by watch filesystem events.

## INSTALLATION

### use pip

```bash
$ [sudo] pip install auto-rsync
```

### use [pipsi](https://github.com/mitsuhiko/pipsi) (recommend)

```bash
$ pipsi install auto-rsync
```


## USAGE

```bash
$ auto-rsync --help

Usage: auto_rsync.py [OPTIONS] LOCAL_PATH REMOTE_PATH

Options:
  --observer-timeout INTEGER  The observer timeout, default 1
  --rsync-options TEXT        rsync command options
  --help                      Show this message and exit.
```

## EXAMPLE

```bash
$ auto-rsync ./test username@host:/home/username/test --rsync-options='--delete --excludes=*.pyc'
```
