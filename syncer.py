#!/usr/bin/env python

from __future__ import print_function
import click
import datetime
import os
import sys
import time
import sh
try:
     from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse


def sync_repo(dest, branch):

    # fetch branches
    output = sh.execute('git fetch --all', workdir=dest)

    # pull branches
    output = sh.execute('git pull --all', workdir=dest)

    # reset working copy
    output = sh.execute('git reset --hard origin/%s' % (branch), workdir=dest)

    # clean untracked files
    sh.execute('git clean -dfq', workdir=dest)

    # repo_name = urlparse(repo).path
    # click.echo(
        # 'Finished syncing {repo_name}:{branch} at {t:%Y-%m-%d %H:%M:%S}'.format(
        #     **locals(), t=datetime.datetime.now()))

@click.command()
@click.option('--dest', '-d', envvar='GIT_SYNC_DEST', default=os.getcwd(), help='The destination path. Defaults to the current working directory; can also be set with envvar GIT_SYNC_DEST.')
@click.option('--branch', '-b', envvar='GIT_SYNC_BRANCH', default='master', help='The branch to sync. Defaults to inferring from `repo` (if already cloned), otherwise defaults to master; can also be set with envvar GIT_SYNC_BRANCH.')
@click.option('--wait', '-w', envvar='GIT_SYNC_WAIT', default=60, help='The number of seconds to pause after each sync. Defaults to 60; can also be set with envvar GIT_SYNC_WAIT.')
@click.option('--run-once', '-1', envvar='GIT_SYNC_RUN_ONCE', is_flag=True, help="Run only once (don't loop). Defaults to off; can also be set with envvar GIT_SYNC_RUN_ONCE=true.")
def git_sync(dest, branch, wait, run_once):
    """
    Periodically syncs a remote git repository to a local directory. The sync
    is one-way; any local changes will be lost.
    """
    while True:
        sync_repo(dest, branch)
        if run_once:
            break
        time.sleep(wait)

if __name__ == '__main__':
    git_sync()