from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB
config = Configuration()

inputList = 'failedMClist.txt'
ape = 'ultralegacyMC_v2'
jobTag = 'TkAlJetHTAnalysis_2017Conditions_105X_mc2017_realistic_v5_' + ape + '_2019-06-26_reallyFailed'
#errorFile = ape + '.db'

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = config.General.requestName
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'JetHTAnalyzer_cfg.py'
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 1500
config.JobType.maxJobRuntimeMin = 500
#config.JobType.pyCfgParams = ['mc=1','errorFile='+errorFile]
config.JobType.pyCfgParams = ['mc=1']
#config.JobType.inputFiles = ['alignments_MC2017_MP.db',errorFile]

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'TrackAlignment_jetHTanalysis'
config.Data.outLFNDirBase = ('/store/user/%s/' % (getUsernameFromSiteDB())) + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_US_Florida','T2_US_Nebraska','T2_US_Wisconsin','T2_US_MIT']
config.Site.storageSite = 'T3_US_FNALLPC'
