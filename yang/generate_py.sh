#!/bin/bash
SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP=${SDIR%*/yang}
PYBINDPLUGIN=`/usr/bin/env python3 -c 'import pyangbind; import os; print("%s/plugin" % os.path.dirname(pyangbind.__file__))'`
for files in ${SDIR}/*
do
  temp_file=$(basename $files)
  if [ "${temp_file##*.}" == "yang" ]
  then
    yangname=${temp_file%*.yang}
    yangnewname=${yangname//-/_}
    pyang --plugindir $PYBINDPLUGIN -f pybind -o $SDIR/$yangnewname.py $yangname.yang
  fi
done

