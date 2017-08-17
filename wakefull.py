#!/usr/bin/env python

"""
Filename: wakefull.py
Description: A simple/python version of caffeine, the screensaver blocker.

Author: John Walsh
Maintainer: John Walsh

Copyright (C) 2015, John Walsh, all rights reserved.
Created: Sep 23 2015

https://sourceforge.net/projects/wakefull/

Versions:

1.3.0 - 01/03/16
1.2.0 - 30/12/15
1.1.0 - 21/11/15
1.0.0 - 25/09/15

----------------------------------------------------------------------

Usage: 

wakefull.py [--debug --display :0.0 --help --on]

See README for user instructions.

----------------------------------------------------------------------

This file is part of Wakefull.

Wakefull is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Wakefull is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""


######################################################################
# user options                                                       #
######################################################################

# print simple debug messages (when run crom CLI)

debug = False

# --

# are we in wakefull mode

wakefull_active = False

# --

wakefull_interval_sec = 45


######################################################################
# python support                                                     #
######################################################################

# library support for python versions 2 and 3

import sys

if sys.version_info[0] == 2:
    import gtk
    my_gtk = gtk
    my_gtk_pygtk_version = my_gtk.pygtk_version
    import glib
    my_glib = glib


if sys.version_info[0] == 3:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    my_gtk = Gtk
    my_gtk_pygtk_version = (my_gtk.MAJOR_VERSION, my_gtk.MINOR_VERSION, my_gtk.MICRO_VERSION)
    from gi.repository import GLib
    my_glib = GLib


# common libraries

import getopt
import os
import subprocess
import shlex
import socket


######################################################################
# functions                                                          #
######################################################################

def my_exec(my_cmd, my_wait=True):
    my_cmd_list = shlex.split(my_cmd)

    if my_wait:
        bash_call = subprocess.Popen(my_cmd_list, shell=False, stdin = None, stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
        output_bin, status = bash_call.communicate()[0], bash_call.returncode
        output = output_bin.decode("utf-8").strip()
    else:
        bash_call = subprocess.Popen(my_cmd_list, shell=False, stdin = None, stdout = None, stderr = None, close_fds=True)
        status = 0
        output = ""

    return status, output


######################################################################

def get_lock(process_name):
    # Without this our lock gets garbage collected
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        #print("I got the lock")
    except socket.error:
        #print("lock exists")
        exit()


######################################################################

# debug output

def wakefull_say(message):
    if debug:
        print(message)



######################################################################

def wakefull_usage():
    print("Usage: " + sys.argv[0] + " [--display :0.0 --help --debug]")

    exit(1)


######################################################################

def wakefull_change_state():
    global wakefull_active

    wakefull_active = not wakefull_active

    wakefull_say("set active state to: %s" % wakefull_active)

    tray.set_from_file(wakefull_config['icon_' + str(wakefull_active)])
    tray.set_tooltip_text(wakefull_config['tooltip_' + str(wakefull_active)])

    if wakefull_active:
        status, output = my_exec(wakefull_config['start'], False)
    else:
        status, output = my_exec(wakefull_config['stop'], False)


######################################################################

# Event handler for the tray icon being clicked

def wakefull_onClick(widget):
    my_glib.timeout_add(100, wakefull_change_state)


######################################################################

def wakefull_loop():
    if wakefull_active:
        wakefull_say("wakeup")
        status, output = my_exec(wakefull_config['active'], False)

    return True


######################################################################
# system config                                                      #
######################################################################

wakefull_config = \
dict(
    # The title to be shown on the pop-up.
    title = "Wakefull",

    # The title to be shown on the icon tooltip.
    tooltip_True = "Click to turn OFF",
    tooltip_False = "Click to turn ON",

    # Icons to use in the system tray and pop-up.
    icon_True = "/usr/share/icons/user/wakefull_icon_brown.svg",
    icon_False = "/usr/share/icons/user/wakefull_icon_white.svg",

    # Frequency for active state.
    active_interval_s = wakefull_interval_sec,
)


######################################################################
# Command-line options                                               #
######################################################################

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'hdt', [
        'debug',
        'display=',
        'help',
        'on',
    ])
except:
    print("Unrecognized options given, try " + sys.argv[0] + " --help")
    exit(1)

# Parse the options
for opt in options:
    if opt[0] == '--debug':
        debug = True
        wakefull_say("Debug mode activated")
    elif opt[0] == '--display' or opt[0] == '-d':
        os.environ["DISPLAY"] = opt[1]
        wakefull_say("Set environment $DISPLAY to: %s" % opt[1])
    elif opt[0] == '--help' or opt[0] == '-h':
        wakefull_usage()
    elif opt[0] == '--on':
        wakefull_active = True


######################################################################
# instance check                                                     #
######################################################################

# ensure a single instance only

get_lock(wakefull_config['title'])


######################################################################
# auto detection                                                     #
######################################################################

# detect which script files to use? users or system

wakefull_config['script_dir'] = os.path.expanduser("~/.config/wakefull/")

if not os.path.isdir(wakefull_config['script_dir']):
    wakefull_config['script_dir'] = "/usr/local/bin/"

wakefull_config['start'] = wakefull_config['script_dir'] + 'wakefull_start.sh'
wakefull_config['active'] = wakefull_config['script_dir'] + 'wakefull_active.sh'
wakefull_config['stop'] = wakefull_config['script_dir'] + 'wakefull_stop.sh'


######################################################################
# main                                                               #
######################################################################

tray = my_gtk.StatusIcon()

if my_gtk_pygtk_version >= (2,22,0):
    tray.set_title(wakefull_config['title'])

tray.connect('activate', wakefull_onClick)


# show icon

tray.set_from_file(wakefull_config['icon_' + str(wakefull_active)])
tray.set_tooltip_text(wakefull_config['tooltip_' + str(wakefull_active)])
tray.set_visible(True)


# http://www.pygtk.org:
# The first call to the function will be at the end of the first interval.

my_glib.timeout_add_seconds(wakefull_config['active_interval_s'], wakefull_loop)

my_gtk.main()

# vim:expandtab


######################################################################
