from WMCore.Configuration import Configuration
config = Configuration()

inputList='jetHtFilesForRun2016B_part2.txt'
jobTag='TkAlJetHTAnalysis_Run2016B_part2_ReReco_2020-08-25'

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = config.General.requestName
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'JetHTAnalyzer_jsonImplementation.py'
config.JobType.pyCfgParams = ['configurationFile=jethtConfigurationReReco.json']
config.JobType.inputFiles = ['jethtConfigurationReReco.json']
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 1800
config.JobType.maxJobRuntimeMin = 1440

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'TrackAlignment_jetHTanalysis'
config.Data.outLFNDirBase = '/store/user/jviinika/' + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_CH_*','T2_DE_*']
config.Site.storageSite = 'T3_US_FNALLPC'
