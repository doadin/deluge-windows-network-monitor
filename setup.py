#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="deluge-windows-network-monitor",
    version="1.0.0",
    description="Windows Network Monitor - Deluge plugin that shuts down when network interface is disconnected",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/doadin/deluge-windows-network-monitor",
    license="GPL-3.0",
    packages=find_packages(),
    package_data={
        'delugenm': ['gtk/plugins.ui', 'data/pixmaps/*']
    },
    entry_points={
        'deluge.plugin': 'delugenm = delugenm:plugin_base',
    },
    install_requires=[
        'deluge',
        'pywin32',  # Required for WMI access on Windows
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking',
    ],
)
