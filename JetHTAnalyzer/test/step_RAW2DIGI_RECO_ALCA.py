# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: stepReALCA --conditions 104X_dataRun2_v1 --nThreads 8 --scenario pp --process RECO --data -n 10 --era Run2_2017 --eventcontent ALCARECO --runUnscheduled -s RAW2DIGI,RECO:reconstruction_trackingOnly,ALCA:TkAlMinBias --datatier ALCARECO --dasquery=file dataset=/JetHT/Run2017A-v1/RAW run=296887 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

def customise_TkAlMinBias(process):
    if hasattr(process,'ALCARECOStreamTkAlMinBias'):
        process=customise_removeDQM(process)
    return process   

def customise_removeDQM(process):
    print "customising remove ALCA DQM"
    process.pathALCARECOTkAlMinBias.remove(process.ALCARECOTkAlMinBiasTkAlDQM)
    return process

process = cms.Process('RECO',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.AlCaRecoStreams_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/487AC8B6-7BB8-E711-93B9-02163E019BFA.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/AE193E93-79B8-E711-A17D-02163E01A4D8.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/9E4887E4-55B9-E711-8030-02163E0146C1.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/F84A78BA-55B9-E711-BAA8-02163E0144DD.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/B239D0E6-55B9-E711-9925-02163E01A650.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/7E58B84F-56B9-E711-8AFF-02163E011F41.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/C8F39CA8-56B9-E711-81D0-02163E019B35.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/6C946E24-56B9-E711-83E3-02163E019CC4.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/6AD4D0FB-56B9-E711-BBD5-02163E0140E4.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/A05360AC-71B8-E711-9CF4-02163E012A29.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/C8A205B8-71B8-E711-9D99-02163E013733.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/DE3FD97C-7BB8-E711-B296-02163E0128D7.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/26161C03-71B8-E711-8FEF-02163E01A2F5.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/525A62BF-71B8-E711-B6F2-02163E0139D0.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/90397D86-7CB8-E711-8A8A-02163E014549.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/EEF6D5EF-7BB8-E711-A84E-02163E01A424.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/62AFE82C-8CB8-E711-884F-02163E01A580.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/7AAB9BB4-55B9-E711-8C0E-02163E0137BC.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/5AE1A4D1-55B9-E711-BE4F-02163E0119EE.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/BE05D342-56B9-E711-A9CD-02163E01A20E.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/D632A484-77B8-E711-BB76-02163E011CDE.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/18BB24C9-55B9-E711-864D-02163E011A12.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/286D47DA-55B9-E711-BAB2-02163E0142F3.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/92A2DBE7-55B9-E711-B30F-02163E01A3F4.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/66DF5EF8-70B8-E711-8C8E-02163E013942.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/CEF1B890-77B8-E711-825E-02163E011F23.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/601B894A-78B8-E711-8B8F-02163E0145EE.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/BCA23C12-46B9-E711-9FDD-02163E014376.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/9E37FCC6-55B9-E711-8136-02163E011AD9.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/4E9028BF-55B9-E711-A650-02163E01369C.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/F27AA837-56B9-E711-98B6-02163E019CD0.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/44048435-56B9-E711-8109-02163E014758.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/6E342C01-56B9-E711-B529-02163E019CE1.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/1EAC3D8E-77B8-E711-8231-02163E01360C.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/0E00CCC6-7BB8-E711-AF55-02163E011A8F.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/5CC24DC3-46B9-E711-98DF-02163E01212C.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/F6D8F2C2-55B9-E711-99B9-02163E011ACF.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/7010D3DB-55B9-E711-BD9B-02163E01A69B.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/9E42EEC9-55B9-E711-9C75-02163E01A76D.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/E0079DE1-55B9-E711-9725-02163E019C70.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/AA1DD684-77B8-E711-B713-02163E011CBC.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/761F0C4D-79B8-E711-8BAC-02163E01A51D.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/20879D8E-7BB8-E711-987D-02163E014771.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/961B6387-7BB8-E711-A091-02163E012506.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/5AC11051-7CB8-E711-9675-02163E01A4FD.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/905B7469-3EB9-E711-956A-02163E014750.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/22CF182E-43B9-E711-BB96-02163E019BEE.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/D81858B9-55B9-E711-BEA3-02163E0142DA.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/74ED09D3-55B9-E711-B93D-02163E019DEF.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/8EFB9505-56B9-E711-8AB2-02163E01A6D1.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/3EC944ED-55B9-E711-8843-02163E019E85.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/9C9F41AC-56B9-E711-8DFF-02163E01A6EE.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/A6CDE27B-77B8-E711-847C-02163E01192C.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/828E36DE-55B9-E711-A3DE-02163E013512.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/30C3B2DE-55B9-E711-9378-02163E014579.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/DC7A6F0E-56B9-E711-A9F2-02163E019B1E.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/6CCABC0E-56B9-E711-A8FC-02163E019BC1.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/DA2821C5-55B9-E711-9BF3-02163E01A72E.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/A4A3699A-7BB8-E711-A1C4-02163E01A3B3.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/00262672-7CB8-E711-8560-02163E0142AF.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/F88FAAB6-55B9-E711-9579-02163E01344A.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/9E0EE600-56B9-E711-B32C-02163E01A5F3.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/C0E228CD-55B9-E711-990D-02163E019E18.root',
        '/store/data/Run2017F/JetHT/RAW/v1/000/305/517/00000/4AE515FE-55B9-E711-8777-02163E01A1F9.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('stepReALCA nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition
process.ALCARECOStreamTkAlMinBias = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOTkAlMinBias')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('TkAlMinBias')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('TkAlMinBias.root'),
    outputCommands = cms.untracked.vstring(
        'drop *', 
        'keep *_ALCARECOTkAlMinBias_*_*', 
        'keep L1AcceptBunchCrossings_*_*_*', 
        'keep L1GlobalTriggerReadoutRecord_gtDigis_*_*', 
        'keep *_TriggerResults_*_*', 
        'keep DcsStatuss_scalersRawToDigi_*_*', 
        'keep *_offlinePrimaryVertices_*_*', 
        'keep *_offlineBeamSpot_*_*'
    )
)

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOTkAlMinBias_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '104X_dataRun2_v1', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction_trackingOnly)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.ALCARECOStreamTkAlMinBiasOutPath = cms.EndPath(process.ALCARECOStreamTkAlMinBias)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.pathALCARECOTkAlMinBias,process.endjob_step,process.ALCARECOStreamTkAlMinBiasOutPath)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(8)
process.options.numberOfStreams=cms.untracked.uint32(0)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
process = customise_TkAlMinBias(process)
