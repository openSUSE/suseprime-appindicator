#!/usr/bin/python3

import os
from distutils.core import setup

setup(name="suseprimeindicator",
      version="0.1.0",
      description="SUSE Prime Application Indicator",
      url='https://github.com/openSUSE/suseprime-appindicator',
      author='Stasiek Michalski',
      author_email='hellcp@opensuse.org',
      license='GPLv2',
      packages=["suseprimeindicator"],
      data_files=[
          ('/usr/share/icons/hicolor/symbolic/apps/', ['icons/suseprime-symbolic.svg', 'icons/suseprime-intel-symbolic.svg', 'icons/suseprime-nvidia-symbolic.svg']),
          ('/usr/share/suseprime-appindicator/scripts', ['scripts/pkexec_nvidia', 'scripts/pkexec_intel']),
          ('/etc/xdg/autostart', ['autostart/suseprime-appindicator.desktop'])],
      scripts=["bin/suseprime-appindicator"]
)
