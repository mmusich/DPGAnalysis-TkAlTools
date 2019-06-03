from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

config = Configuration()

inputList='JetHT_Run2017ABCDEF-v1_RAW_10k/JetHT_Run2017ABCDEF-v1_RAW_sorted.txt'
jobTag='TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov_2019-06-03' 

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = config.General.requestName
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step_RAW2DIGI_RECO_ALCA.py'
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 4500

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 4
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'TrackAlignment_jetHTreconstruction'
config.Data.outLFNDirBase = ('/store/user/%s/' % (getUsernameFromSiteDB())) + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_CH_CERN']
config.Site.storageSite = 'T3_US_FNALLPC'
