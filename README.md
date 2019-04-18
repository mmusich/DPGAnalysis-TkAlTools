# DPGAnalysis-TkAlTools

Recipe to run the analysis:

```
cmsrel CMSSW_10_4_0
cd CMSSW_10_4_0/src/
cmsenv
git clone git@github.com:mmusich/DPGAnalysis-TkAlTools.git TkAlTools
scramv1 b -j 8
cd TkAlTools/JetHTAnalyzer/test/
cmsRun JetHTAnalyzer_cfg.py

```

For running the analysis on CRAB, do the following instead of the cmsRun command in the above instructions:

1. Edit the following lines in file crabJetHT.py
  - inputList = Give here a list of files you want to analyse
  - jobTag = Give a unique name for your job
  - config.Site.storageSite = Give a site name where you have write rights

2. Run the analysis on CRAB:
  ```
  source /cvmfs/cms.cern.ch/crab3/crab.sh
  voms-proxy-init --voms cms
  crab submit -c crabJetHT.py
  ```
