#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage of the script:"
  echo "$0 <iovList> <fileList>"
  echo "iovList = List containing run numbers that are boundaries of intervals of validity"
  echo "fileList = List of files to be arranged per interval of validity"
  exit
fi

IOVLIST=$1
FILELIST=$2

# Read the run number from the file list and save it to a list for a specific interval of validity
while read line
do

  # The values for thousands and ones of run number are in the same position for each string
  THOUSANDS="$(cut -c39-41 <<<${line})"
  ONES="$(cut -c43-45 <<<${line})"
  RUNNUMBER="${THOUSANDS}${ONES}"

  # Find out the integral of validity to which this run number belongs
  IOVCOUNTER=0
  while read iov
  do
    IOVCOUNTER=$(( IOVCOUNTER+1 ))
    if [ $RUNNUMBER -lt $iov ]; then
      break
    fi
  done < $IOVLIST

  # Read the interval of validity boundaries for this file
  IOVHIGH=`sed "${IOVCOUNTER}q;d" $IOVLIST`
  IOVHIGH=$(( IOVHIGH-1 ))
  IOVCOUNTER=$(( IOVCOUNTER-1 )) 
  IOVLOW=`sed "${IOVCOUNTER}q;d" $IOVLIST`
  
  # Create a new file name based on the boundaries for interval of validity
  OLDFILENAME=${FILELIST::${#FILELIST}-4} # Remove extension from input file list
  NEWFILENAME="${OLDFILENAME}_${IOVLOW}-${IOVHIGH}.txt"

  # Write the current data file name to the new file
  echo "$line" >> $NEWFILENAME

done < $FILELIST
