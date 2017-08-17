#!/usr/bin/env bash

# install.sh

# install wakeful to system
# run as root

# ----

# check system is OK for installation

sys_ok=1

# ----

py_version=$(type -p python)
if [[ $py_version ]]; then
  py_version=$(python --version 2>&1 | awk '{print $2}')
  temp=( ${py_version//./ } )
  py_version_major=${temp[0]}
else
  echo missing: python
  sys_ok=0
fi

# ----

# check file system structure

if [[ ! -d "/usr/share/icons" ]]; then
  echo missing: /usr/share/icons
  sys_ok=0
fi

if [[ ! -d "/usr/local/bin" ]]; then
  echo missing: /usr/local/bin
  sys_ok=0
fi

if [[ ! -d "/etc/xdg/autostart" ]]; then
  echo missing: /etc/xdg/autostart
  sys_ok=0
fi

if [[ ! -d "/usr/share/applications" ]]; then
  echo missing: /usr/share/applications
  sys_ok=0
fi

if (( $sys_ok )); then
  echo system check: passed
else
  echo system check: failed
  echo please check your system and modify this script to siut...
  exit
fi

# ----

# all OK, force root owner

if (( $EUID )); then
  echo "Please, type root's password..."
  su -c "$0 $@"
  exit
fi

# ----

mkdir -p /usr/share/icons/user

# if (( $py_version_major >= 3 )); then
#   cp ./wakefull_py3.py /usr/local/bin/wakefull.py
# else         
#   cp ./wakefull_py2.py /usr/local/bin/wakefull.py
# fi

cp ./wakefull.py /usr/local/bin/wakefull.py

cp ./wakefull_icon_* /usr/share/icons/user/.
cp ./wakefull*.sh /usr/local/bin/.

cp ./wakefull_auto.desktop /etc/xdg/autostart/wakefull.desktop

cp ./wakefull_app.desktop /usr/share/applications/wakefull.desktop

# ----

echo Done.
