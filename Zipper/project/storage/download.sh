#!/bin/bash -x

location=$(pwd)

format='7z'


while getopts f:u:l:c:s:a: param; do
	case $param in
		f) filename=$OPTARG
			;;
		u) url=$OPTARG
			;;
		l) location=$OPTARG
			;;
		c) level=$OPTARG
			;;
		s) split=$OPTARG
			;;
		a) format=$OPTARG
			;;
	esac
done

#downloading file
aria2c -x2 -o "$filename" -d "$location" "$url" 1> /dev/null 2>&1

if [[ $? -ne 0 ]]
then
	exit 1
fi

clamscan "$location/$filename" 1> /dev/null 2>&1

if [[ $? -ne 0 ]]
then
	echo "Virus detected"
	exit 2
fi

name=${filename%.*}

if [ $split ]
then
	7z a -t7z -m0=lzma2 -mx=${level} -aoa -mfb=64 -md=32m -ms=on -mhe -V${split}m "$location/zip/$filename/$filename.$format" "$location/$filename" | tail -n 2 | head -n 1 | cut -d ' ' -f 3
	echo "$location/zip/$filename"
	ls -l "$location/zip/$filename" | sed 1d | awk '{for(i=9;i<=NF;++i)printf $i""FS ; print":"$5}'
else
	7z a -t7z -m0=lzma2 -mx=${level} -aoa -mfb=64 -md=32m -ms=on -mhe  "$location/zip/$filename.$format" "$location/$filename" | tail -n 2 | head -n 1 | cut -d ' ' -f 3
	echo "$location/zip/$filename.$format"
fi


if [[ $? -ne 0 ]]
then
	exit 1
fi
