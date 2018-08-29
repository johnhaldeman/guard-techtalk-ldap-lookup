#!/bin/sh
## (C) Copyright IBM Corp. 2018
# The source code for this program is not published or
# otherwise divested of its trade secrets, irrespective of
## what has been deposited with the US Copyright Office.

## IMPORTANT: If you change this script, also change install.sh; 
# a "replica" of this script is created in install.sh, 
# in $INSTALL_PATH/bin/install_guardium_dependencies. 
##
if [ ! -z "$1" ]; then
    cd "$1"
fi

# install rpms
if [ -f src_deps/rpms/ordering.txt ] ; then
    echo "Found src_deps/rpms/ordering.txt file, installing listed RPMs if available under src_deps/rpms/..."
    for line in $(cat src_deps/rpms/ordering.txt)
    do
      rpm -Uvh src_deps/rpms/$line
    done
else
  if ls src_deps/rpms/*.rpm 1> /dev/null 2>&1; then
    echo "Found src_deps/rpms/*rpm file, installing..."
    rpm -Uvh src_deps/rpms/*.rpm
  fi
fi

echo "Attempting to install APP pip requirements as listed under src_deps/pip/APP_CUSTOM_REQUIREMENTS.txt."
echo "The necessary installation files for the listed requirements must be located under src_deps/pip"
pip install --no-index --find-links=src_deps/pip -r src_deps/pip/APP_CUSTOM_REQUIREMENTS.txt
# install python pip packages
#if [ -f src_deps/pip/ordering.txt ] ; then
#    echo "Found src_deps/pip/ordering.txt file, you will need to install these pip packages manually ..."
#    for line in $(cat src_deps/pip/ordering.txt)
#    do
#      pip install src_deps/pip/$line
#    done
#else
#  if ls src_deps/pip/*.whl 1> /dev/null 2>&1; then
#        echo "Found src_deps/pip/*whl file, you will need to install these pip packages manually ..."
#        pip install src_deps/pip/*.whl
#  fi
#  if ls src_deps/pip/*.tar.gz 1> /dev/null 2>&1; then
#    echo "Found src_deps/pip/*tar.gz file, you will need to install these pip packages manually ..."
#    pip install src_deps/pip/*.tar.gz
#  fi
#fi

# install other stuff, if app does not run locally (through SDK).
if [ -f src_deps/init/ordering.txt ] ; then
    echo "=====  Running commands from src_deps/init.ordering.txt  ====="
      while read line || [[ -n "$line" ]];
        do
          $line;
        done < src_deps/init/ordering.txt
fi
