#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Script generating a list of files that failed in a crab job"
  echo "Usage of the script:"
  echo "$0 [fileList] [crabStatusTable] [filesPerJob] [outputName]"
  echo "fileList = List of all the jobs that were submitted"
  echo "crabStatusTable = File containing the status table given by the crab status --long command"
  echo "filesPerJob = Number of files per one job"
  echo "outputName = Name of the output file"
  exit
fi

FILELIST=$1
CRABSTATUSTABLE=$2
FILESPERJOB=$3
OUTPUT=$4
SUCCESSLIST="listOfSuccessfullJobsForThisScript.txt"

# Create a list of successfull jobs from the crab status output
./readCrabStatuses.sh $CRABSTATUSTABLE $SUCCESSLIST

# Read the first line of the success list
read -r BEGIN END < $SUCCESSLIST

# Calculate the indices of the first and last line that need to be removed from the file list
LINEMINUSONE=$(( $BEGIN - 1 ))
FIRST=$(( 1 + $LINEMINUSONE * $FILESPERJOB ))
MULTIPLIER=$(( $END - $BEGIN + 1 ))
LAST=$(( $FIRST + $FILESPERJOB * MULTIPLIER - 1 ))

# Prepare the first line to the sed command
COMMAND="$FIRST,${LAST}d"

# Loop over the rest of the success file
while read -r BEGIN END
do

  # Calculate the indices of the first and last line that need to be removed from the file list
  LINEMINUSONE=$(( $BEGIN - 1 ))
  FIRST=$(( 1 + $LINEMINUSONE * $FILESPERJOB ))
  MULTIPLIER=$(( $END - $BEGIN + 1 ))
  LAST=$(( $FIRST + $FILESPERJOB * MULTIPLIER - 1 ))

  # Add the lines to be removed to the sed command
  printf -v COMMAND '%s;%d,%dd' "$COMMAND" "$FIRST" "$LAST"

done < <(tail -n +2 $SUCCESSLIST)

# Delete the successfull jobs from the new file list
sed ''"$COMMAND"'' "$FILELIST" > "$OUTPUT"

# Remove the temporary file containing the list of successful runs
rm $SUCCESSLIST
