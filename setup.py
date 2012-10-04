# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: setup.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os

from setuptools import setup, find_packages, Extension


def make_extensions(include_dir, lib_path):
    lib_file = os.path.basename(lib_path)
    lib_name = os.path.splitext(lib_file)[0]
    if lib_name.startswith('lib'):
        lib_name = lib_name[3:]
    lib_dir = os.path.dirname(lib_path)
    extensions = [
        Extension(
            'pikos._internal._lsprof_rt',
            sources=[
                'pikos/_internal/_lsprof_rt.c',
                'pikos/_internal/rotatingtree.c',
                # 'pikos/_internal/nanopb/pb_encode.c',
                ],
            include_dirs=[include_dir],
            library_dirs=[lib_dir],
            libraries=[lib_name],
            ),
        ]
    return extensions


def run_setup(extensions=None):
    kwargs = dict(
        name='pikos',
        version='0.1a',
        author='Enthought, Inc',
        author_email='info@enthought.com',
        description='Enthought monitoring and profiling tools',
        requires=['psutil'],
        install_requires=['distribute'],
        packages=find_packages(),
        entry_points=dict(
            console_scripts=[
                'pikos-run = pikos.runner:main',
                ],
            ),
        )
    if extensions is not None:
        kwargs['ext_modules'] = extensions
    setup(**kwargs)


class ArgumentParseError(RuntimeError):
    pass


def _parse_argv_item(argv, name):
    if name not in sys.argv:
        raise ArgumentParseError('Missing {} option'.format(name))
    index = sys.argv.index(name) + 1
    if index == len(sys.argv):
        raise ArgumentParseError('Missing argument for {}'.format(name))
    opt, value = sys.argv[index - 1: index + 1]
    sys.argv = sys.argv[:index - 1] + sys.argv[index + 1:]
    return value


def _parse_argv(argv):
    # FIXME: stupid

    INCLUDE = '--include'
    ZMQ_PATH = '--zmq-path'

    include_dir = _parse_argv_item(argv, INCLUDE)
    lib_path = _parse_argv_item(argv, ZMQ_PATH)

    if not os.path.isdir(include_dir) or \
            not 'zmq.h' in os.listdir(include_dir):
        raise ArgumentParseError(('{} option should be a directory containing '
                                  'zmq.h').format(INCLUDE))
    if not os.path.isfile(lib_path):
        raise ArgumentParseError(('{} option should be the compiled zeromq '
                                  'binary').format(ZMQ_PATH))

    return include_dir, lib_path


if __name__ == '__main__':
    import sys

    include_dir, lib_path = _parse_argv(sys.argv)

    extensions = make_extensions(include_dir, lib_path)
    run_setup(extensions)
