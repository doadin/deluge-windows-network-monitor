#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="deluge-windows-network-monitor",
    version="1.0.0",
    description="Windows Network Monitor - Deluge plugin that shuts down when network interface is disconnected",
    author="Doadin",
    author_email="",
    url="https://github.com/doadin/deluge-windows-network-monitor",
    license="GPL-3.0",
    packages=find_packages(),
    package_data={
        'deluge_windows_network_monitor': ['gtk/plugins.ui', 'data/pixmaps/*']
    },
    entry_points={
        'deluge.plugin': 'deluge_windows_network_monitor = deluge_windows_network_monitor:plugin_base',
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
