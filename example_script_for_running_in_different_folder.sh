#!/bin/bash
#
# this is a comment document




f1=$1
f2=$2


usage='

This is a showcase script as an example of how to write script that can run at different directory!

Usage:

	In the same folder as the script:
	$ ./script_for_running_in_different_folder.sh [path_to_file/filename]

	In the target data folder:
	$ path_to_script/./script_for_running_in_different_folder.sh filename

	If running using for loop in the script folder, path to the files need to be provided:
	$ for file in `cat listfile`; do ./script_for_running_in_different_folder.sh $file [path_to_file]

This script takes a xxx file as input and xxx as output.

*Noted that if first argument is given full path or partial path 
 to the file that contains slash / (instead of just a filename), 
 second argument will be ignored.

'

# This gets the absolute directory of the script regardless of where it is run
absolute_dir=$(cd `dirname $0` && pwd)
echo "The script's location: "$absolute_dir/
pwd


# If no argument was given at all, show docs and end the script.
if [ -z "$f1" ] && [ -z "$f2" ]
then
	echo "$usage"
	exit 1
fi


# If argument 2 is provided and end is not /, add it; otherwise just use it as path. If argument 2 is not given, path would just be empty
if [ -n "$f2" ] && [ "${f2: -1}" != "/" ]; then
	path=$f2/
else
	path=$f2
fi

# If argument 1 is full path, reset path to empty
len_f1=`echo $f1 | awk '{n=split($1,a,"/"); print n}'`
if (( $len_f1 > 1 )); then
	path=""
fi


# If path/file doesn't exist and path is not given, end the script
if [ ! -e $path$1 ] && [ -z $f2 ] && (( $len_f1 == 1 )); then
	echo -e "File: \t $1 \t can't be found, path argument may be needed, or filename is incorrect. Script end."
        exit 1
# If path/file doesn't exist and path is given, filename or path might be incorrect, end the script
elif [ ! -e $path$1 ]; then
	echo -e "File: \t $path$1 \t can't be found, check the file name or path, Script end."
	exit 1
fi




awk '{print $1}' $path$f1
echo 'all script done'

