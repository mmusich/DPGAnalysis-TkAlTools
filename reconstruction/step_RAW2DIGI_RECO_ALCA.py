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
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/FACD59F6-9851-E711-A157-02163E01A671.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/0218D1FA-9851-E711-8248-02163E01399E.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/FEBD6DFD-9851-E711-944B-02163E013406.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/466F54FF-9851-E711-B7EF-02163E01416A.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C48FDD09-9951-E711-B936-02163E014408.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/04724205-9951-E711-9D43-02163E012748.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/CC0F690F-9951-E711-B736-02163E01381C.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7ECFF51A-9951-E711-934F-02163E01237E.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C0218FFC-9851-E711-BB42-02163E011953.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/82B5C4F8-9851-E711-A254-02163E01A32D.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/A267C90D-9951-E711-AA2E-02163E0135C8.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/986D5D05-9951-E711-8582-02163E013877.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7860C100-9951-E711-86B4-02163E0143E9.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7CEACBF9-9851-E711-A47A-02163E0146E2.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/D6A87E01-9951-E711-9504-02163E013865.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/8E00C208-9951-E711-BB2D-02163E013630.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/4E14B217-9951-E711-B9E1-02163E01381C.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/88A16902-9951-E711-B1D6-02163E01253C.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/9E8E92C5-9A51-E711-AD86-02163E0143C5.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C8C7EFF7-9851-E711-82AE-02163E019CC3.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7A205203-9951-E711-9C64-02163E011A70.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7CA216FC-9851-E711-A047-02163E011D9F.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/28EC23F9-9851-E711-919C-02163E013673.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/86647C10-9951-E711-9F25-02163E011CFE.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/8A29830E-9951-E711-A063-02163E013502.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/52CB0301-9951-E711-A0BA-02163E01341E.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/24A7560A-9951-E711-A156-02163E0146CA.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/589B1FE7-9D51-E711-8CA6-02163E014484.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/38B3D303-9951-E711-B954-02163E0134D1.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/ECE6B444-9951-E711-A74B-02163E0142FA.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/DC281116-9951-E711-956A-02163E01237E.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/B6C823FD-9851-E711-8AE0-02163E011953.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C02B52FD-9851-E711-8DE8-02163E01416A.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C65F470A-9951-E711-994D-02163E013630.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/FC232EFC-9851-E711-811B-02163E0134D8.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/9E3706FB-9851-E711-AEB0-02163E014755.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/2A534802-9951-E711-A58F-02163E0135C8.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/987655FF-9851-E711-BB18-02163E012268.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/BEEC65FD-9851-E711-A424-02163E014219.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/E607AEFE-9851-E711-B356-02163E014219.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/0ADEDC97-9A51-E711-9774-02163E019C40.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/DCEF4D08-9951-E711-B139-02163E011951.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/862168FE-9851-E711-8DDE-02163E013420.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/70B45B01-9951-E711-86AF-02163E01341E.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/08E84D0C-9951-E711-9E55-02163E013492.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/D090ADDE-A051-E711-BAAB-02163E011E0A.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/AC55FAFD-9851-E711-A132-02163E013420.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/C4D614FF-9851-E711-9494-02163E011A03.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/709A77FF-9851-E711-82DA-02163E012748.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/B6503CA0-9B51-E711-8918-02163E0126F1.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/987266FC-9851-E711-894D-02163E013406.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/BA613346-9951-E711-A0A9-02163E0142FA.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/729CF702-9951-E711-BDE9-02163E011A70.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/F6817C00-9951-E711-8B00-02163E011801.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/CE7DC100-9951-E711-96D3-02163E0143E9.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/9C0C2202-9951-E711-AA8E-02163E014222.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/E08A18FE-9851-E711-B6CF-02163E013492.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/7CD03EC3-9951-E711-BD1F-02163E01392C.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/CE922301-9A51-E711-AE58-02163E0144A0.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/828C6DF6-9851-E711-AD91-02163E01A671.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/947E2AFE-9851-E711-8B11-02163E0141FC.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/669E6D00-9951-E711-96CB-02163E011801.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/B86F5AFA-9851-E711-A34C-02163E011A03.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/52C37E01-9951-E711-AF9E-02163E013865.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/BCE0B204-9951-E711-8084-02163E013502.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/DE387608-9951-E711-8078-02163E013877.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/9A9E4625-9951-E711-91A3-02163E0126FE.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/CE28C8F9-9851-E711-83BB-02163E0134D1.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/2CE25314-9A51-E711-B462-02163E012A01.root', 
        '/store/data/Run2017A/JetHT/RAW/v1/000/296/887/00000/3CBE8966-9951-E711-9CF6-02163E012389.root'
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
    fileName = cms.untracked.string('TkAlJetHT.root'),
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
