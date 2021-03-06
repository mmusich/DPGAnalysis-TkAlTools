from WMCore.Configuration import Configuration
config = Configuration()

inputList='jetHtFilesForMC2016_first50inEachPtHat.txt'
jobTag='TkAlJetHTAnalysis_MC2016_mp3298_2020-08-11'

config.section_("General")
config.General.requestName = jobTag
config.General.workArea = config.General.requestName
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'JetHTAnalyzer_jsonImplementation.py'
config.JobType.pyCfgParams = ['configurationFile=jethtConfigurationMC2016_mp3298.json']
config.JobType.inputFiles = ['jethtConfigurationMC2016_mp3298.json','alignments_MP3298.db']
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 1200
config.JobType.maxJobRuntimeMin = 1200

config.section_("Data")
config.Data.userInputFiles = open(inputList).readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 3
config.Data.totalUnits = len(config.Data.userInputFiles)
config.Data.outputPrimaryDataset = 'TrackAlignment_jetHTanalysis'
config.Data.outLFNDirBase = '/store/user/jviinika/' + config.General.requestName
config.Data.publication = False

config.section_("Site")
config.Site.whitelist = ['T2_CH_*']
config.Site.storageSite = 'T3_US_FNALLPC'
