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