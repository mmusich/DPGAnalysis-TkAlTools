# DPGAnalysis-TkAlTools

## Introduction

This code is indended for doing track alignment checks for JetHT datasets. The JetHT datasets are used so that tracks with very high pT are included and we can study the performance of the alignment also on that region. The code fills the following histograms:
  * Mean dxy and dz error as a function of pT, eta and phi
  * Distributions of dxy, dz and their errors
  * pT, eta and phi for the probe tracks

The histograms are filled for all tracks in the given input files, for central tracks (|eta| < 1) and for each IOV in the IOV list defined in the configuration file.

## Instructions

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

The CRAB configuration files crabJetHT\_MC.py and crabJetHtManualApe.py show examples on how to run with MC configuration or with manual database file for alignment. For these different configurations, see more explanation below.

### Configuration for JetHTAnalyzer\_cfg.py

Variables that you will most likely need to change in JetHTAnalyzer\_cfg.py
  * fileNames = Defines in input files used in the analysis
  * globaltag = Global tag used in the input files
  * alignment tags = Overwrite specific parts of the alignments defined in the global tag
  * iovList = List of run boundaries that define the studied IOV:s

The configuration file can take three parameters. These are
  * mc: 0 = Run analysis with real dada. 1 = Run MC analysis.
  * printTriggers: 0 = Run analysis regularly. 1 = Print trigger table to console.
  * errorFile: Name of the .db file from which ExtendedErrorRecord is read. If not specified, the tag in the code is used.
