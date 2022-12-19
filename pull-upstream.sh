#!/bin/bash
#
# By default, this script will pull from upstream master in all watched subdirectories.
# The user may optionally pass a comma-separated subset of watched subdirectories from 
# which to pull.
#
# Usage: ./pull-upstream.sh [subdirectory1,subdirectory2,subdirectory3,...]
# 

# DEBUG="echo -e"

# Error out if not in deploy-dev root
root_dir=$(pwd)
if [[ "$root_dir" != *deploy-dev ]]; then
	echo "ERROR: This script should be run from the deploy-dev repository root."
	exit 1
fi

# Default parameter to all subdirs
if [ "$1" == "" ]; then
	subdirs="ngx-dashboard,virtual_resources,girderfs,wholetale,gwvolman,wt_versioning,wt_data_manager,wt_home_dir,globus_handler"
else
	subdirs="$1"
fi

# Loop over supplied subdirectories and pull from upstream
for subdir in $(echo "$subdirs" | sed "s/,/ /g")
do
	($DEBUG cd $root_dir/src/$subdir && $DEBUG git status && $DEBUG git pull origin master) || exit 1
done
