#!/usr/bin/python3

import os
import signal
import json
import gi
import gettext

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
from gi.repository import Gio as gio
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

gettext.bindtextdomain('suseprimeindicator', '/usr/share/locale')
gettext.textdomain('suseprimeindicator')
_ = gettext.gettext

APPINDICATOR_ID = 'suseprimeindicator'

intel_notif = _('Switching to Intel staged')
nvidia_notif = _('Switching to Nvidia staged')
reboot_notif = _('Please reboot or relog for changed to take effect')
error_head = _('Error occured')

def check_current():
    if (glib.file_test('/etc/prime/current_type', glib.FileTest.EXISTS)):
        return glib.file_get_contents('/etc/prime/current_type')[1].decode("utf-8").strip()
    else:
        return ''

def main():
    if (check_current() == 'nvidia'):
        icon = 'suseprime-nvidia-symbolic'
    elif (check_current() == 'intel'):
        icon = 'suseprime-intel-symbolic'
    else:
        icon = 'suseprime-symbolic'
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    if (check_current() != 'nvidia'):
        item_nvidia = gtk.MenuItem.new_with_label(_('Switch to Nvidia'))
        item_nvidia.connect('activate', nvidia)
        menu.append(item_nvidia)
    if (check_current() != 'intel'):
        item_intel = gtk.MenuItem.new_with_label(_('Switch to Intel'))
        item_intel.connect('activate', intel)
        menu.append(item_intel)
    menu.show_all()
    return menu

def nvidia(_):
    result, output, error, status = glib.spawn_command_line_sync('/usr/share/suseprime-appindicator/scripts/pkexec_nvidia')
    if (error):
        notify.Notification.new(error_head, error.decode("utf-8"), 'dialog-warning').show()
    elif (result):
        notify.Notification.new(nvidia_notif, reboot_notif, 'suseprime-nvidia-symbolic').show()
    else:
        notify.Notification.new(error_head, output.decode("utf-8"), 'dialog-warning').show()

def intel(_):
    result, output, error, status = glib.spawn_command_line_sync('/usr/share/suseprime-appindicator/scripts/pkexec_intel')
    if (error):
        notify.Notification.new(error_head, error.decode("utf-8"), 'dialog-warning').show()
    elif (result):
        notify.Notification.new(intel_notif, reboot_notif, 'suseprime-intel-symbolic').show()
    else:
        notify.Notification.new(error_head, output.decode("utf-8"), 'dialog-warning').show()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
