#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Script generating a list of ID:s jobs that succeeded from crab status --long output"
  echo "Usage of the script:"
  echo "$0 [inputFile] [outputFile]"
  echo "inputFile = File containing the job table printed out by crab status command"
  echo "outputFile = File to which the list of succeeded job ID:s is printed"
  exit
fi

INPUTFILE=$1
OUTPUTFILE=$2

# Loop over the crab jobs and create a file of the format
# FirstSuccessiveNotFailedJob0 LastSuccessiveNotFailedJob0
# FirstSuccessiveNotFailedJob1 LastSuccessiveNotFailedJob1
# FirstSuccessiveNotFailedJob2 LastSuccessiveNotFailedJob2
# ...
PREVIOUSFAILED=true
while read -r JOBID STATUS THEREST
do
  # If the status is not failed and the previous job failed, start new line for
  # successive jobs that are not failures
  if [ "$STATUS" != "failed" ]; then
    if [ "$PREVIOUSFAILED" = true ]; then
      FIRSTNUMBER=$JOBID
      PREVIOUSFAILED=false
    fi
  # If the status of the job is failed but the previous job was not failed,
  # end the line for successive jobs that are not failures
  else
    if [ "$PREVIOUSFAILED" = false ]; then
      LASTNUMBER=$(( $JOBID-1 ))
      PREVIOUSFAILED=true
      echo "$FIRSTNUMBER $LASTNUMBER" >> $OUTPUTFILE
    fi
  fi
  LATESTNUMBER=$JOBID
done < $INPUTFILE

# If we end the file with non-failed jobs, add the last jobs to successfull jobs list
if [ "$PREVIOUSFAILED" = false ]; then
      echo "$FIRSTNUMBER $LATESTNUMBER" >> $OUTPUTFILE
fi
