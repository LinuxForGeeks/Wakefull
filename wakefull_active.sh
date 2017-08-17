#!/usr/bin/env bash

# wakefull_active.sh
# Copyright (C) 2015, John Walsh, all rights reserved.

# called periodically while wakefull.py is turned ON (active)

# it works by:

# simulate a key press
# OR
# find any screen/power saver processes and block/reset them

# ----

# decide on method to use

if [[ $(type -p xdotool) ]]; then
  use_xdotool=1
else
  use_xdotool=0
fi

# override method

#use_xdotool=0

# ----

if (( $use_xdotool )); then

######################################################################
# simulate a key press
######################################################################

# in general, this should work for all cases

xdotool key F20

# if it doesn't, or causes any problems, then try this:

#xdotool search --name Desktop key F20

# otherwise, don't use xdotool

else

######################################################################
# find any screen/power saver processes and block/reset them
######################################################################

# gnome-screensaver

pgrep -f gnome-screensaver && gnome-screensaver-command --deactivate

# ----

# xscreensaver

pgrep -f xscreensaver && xscreensaver-command -deactivate

# ----

# gnome-power-manager

pgrep -f gnome-power-manager && pkill -f gnome-power-manager; gnome-power-manager &

# ----

# xfce4-power-manager

pgrep -f xfce4-power-manager && xfce4-power-manager --restart

fi

######################################################################

