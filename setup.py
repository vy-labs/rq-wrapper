import os

from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'rq_wrapper/version.py')) as f:
            locals = {}
            exec(f.read(), locals)
            return locals['VERSION']
    except FileNotFoundError:
        raise RuntimeError('No version info found.')


def get_requirements():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'requirements.txt')) as f:
            return f.readlines()
    except FileNotFoundError:
        raise RuntimeError('No requirements info found.')


setup(
    name='rq_wrapper',
    version=get_version(),
    author='',
    author_email='',
    description='RQ-Wrapper is a wrapper for RQ to introduce environment variables.',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=get_requirements(),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': [
            'rq_wrapper = rq.cli:main',
            'dashboard = rq_wrapper.dashboard.cli:main'
        ],
    },
)
