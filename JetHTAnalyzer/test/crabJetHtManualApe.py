from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB
config = Configuration()

inputList='crabFilesJetHT10keventsPerIovNewAlignment.txt'
jobTag='TkAlJetHTAnalysis_Run2017ABCDEF-v1_10keventPerIov_manualApe_2019-06-07'

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
config.JobType.maxJobRuntimeMin = 360
config.JobType.inputFiles = ['ul2017_comparison_merged.db']

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'TrackAlignment_jetHTanalysis'
config.Data.outLFNDirBase = ('/store/user/%s/' % (getUsernameFromSiteDB())) + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_US_*']
config.Site.storageSite = 'T3_US_FNALLPC'
