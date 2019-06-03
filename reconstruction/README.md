# Reconstruction

Reconstructing RAW data to a format that can be more easily analyzed

1. Edit the following lines in file crabReconstruct.py
  - inputList = Give here a list of files you want to analyse
  - jobTag = Give a unique name for your job
  - config.Site.storageSite = Give a site name where you have write rights

2. Run the analysis on CRAB:

  ```
  source /cvmfs/cms.cern.ch/crab3/crab.sh
  voms-proxy-init --voms cms
  crab submit -c crabReconstruct.py
  ```

## Troubleshooting

In case some of the crab jobs fail and cannot be recovered with `crab resubmit` command, you can generate a file list for only the failed jobs using `./makeFailList.sh` script. This script required you to copy a status table printed by `crab status --long` command to a text file. Then you can easily send a recovery job excluding all the files that were previously reconstructed successfully.
