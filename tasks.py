from invoke import run, task, env
from invoke.util import cd, contextmanager
import sys
import os

env.directory = './'
env.activate = 'source env/bin/activate && '


@task()
def pip(cmd='list', venv=True):
    venv = env.activate if venv else ''
    run('{venv}pip {cmd}'.format(**locals()))


@task
def mkdir(path):
    if sys.platform == 'win32':
        run('mkdir %s' % path)
    elif sys.platform == 'unix':
        run('mkdir -p %s' % path)


@task
def test_setup():
    pip('install -r tests/requirements.txt')
    pip('install -U .')


@task
def create_test_app():
    """Create a test app structure

    :return:
    """
    mkdir(path='tests')
    with cd('tests'):
        run('django-admin.exe startproject config .')


@task
def docs():
    """Build html docs

    :return:
    """
    with cd('docs'):
        run('make html')


@task
def clean(docs=False, bytecode=False, venv=False, extra=''):
    patterns = ['build', '*.egg-info', 'dist']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if venv:
        patterns.append('env')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        run("rm -rf %s" % pattern)


@task
def build(docs=False):
    run("python setup.py sdist bdist_wheel")
    if docs:
        run("sphinx-build docs docs/_build")


@task
def runserver():
    run("python tests/manage.py runserver",)
