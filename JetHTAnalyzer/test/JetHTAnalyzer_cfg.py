'''
cfg to produce alignment validation plots from JetHT sample 
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms
process = cms.Process("JetHTAnalyzer")

###################################################################
# Messages
###################################################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.source = cms.Source("PoolSource",
                            #fileNames = cms.untracked.vstring('file:/tmp/musich/CMSSW_10_4_0/src/Alignment/JetHTAnalyzer/test/TkAlMinBias.root')
                            fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/user/jviinika/TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/TrackAlignment_jetHTreconstruction/crab_TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/190305_003651/0000/TkAlJetHT_1.root')
                            )

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.GlobalTag.globaltag = '104X_dataRun2_v1'

# process.GlobalTag.toGet.append(
# cms.PSet(
#   connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#   record = cms.string("TrackerAlignmentRcd"),
#   tag = cms.string("TrackerAlignment_v24_offline")),
# )
# process.GlobalTag.toGet.append(
# cms.PSet(
#   connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#   record = cms.string("TrackerAlignmentErrorExtendedRcd"),
#   tag = cms.string("TrackerAlignmentExtendedErrors_v10_offline_IOVs")),
# )


process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
# remove the following lines if you run on RECO files
process.TrackRefitter.src = 'ALCARECOTkAlMinBias'
process.TrackRefitter.NavigationSchool = ''

## PV refit
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import offlinePrimaryVertices 
process.offlinePrimaryVerticesFromRefittedTrks  = offlinePrimaryVertices.clone()
process.offlinePrimaryVerticesFromRefittedTrks.TrackLabel                                       = cms.InputTag("TrackRefitter") 
process.offlinePrimaryVerticesFromRefittedTrks.vertexCollections.maxDistanceToBeam              = 1
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxNormalizedChi2             = 20
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minSiliconLayersWithHits      = 5
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.maxD0Significance             = 5.0 
process.offlinePrimaryVerticesFromRefittedTrks.TkFilterParameters.minPixelLayersWithHits        = 2   

process.jetHTAnalyzer = cms.EDAnalyzer('JetHTAnalyzer',
                                       vtxCollection    	= cms.InputTag("offlinePrimaryVerticesFromRefittedTrks"),
                                       trackCollection		= cms.InputTag("TrackRefitter"),		
                                       minVertexNdf        = cms.untracked.double(10.),
                                       minVertexMeanWeight = cms.untracked.double(0.5),
                                       iovList = cms.untracked.vint32(296702,296966,297224,297281,297429,297467,297484,297494,297503,297557,297598,297620,297660,297670,298653,298678,298996,299062,299096,299184,299327,299368,299381,299443,299480,299592,299594,299649,300087,300155,300233,300237,300280,300364,300389,300399,300459,300497,300515,300538,300551,300574,300636,300673,300780,300806,300812,301046,301417,302131,302573,302635,303719,303790,303825,303998,304170,304505,304672,304911,305040,305113,305178,305188,305204,305809,305842,305967,305898,306029,306042,306126,306169,306417,306459,306460,306705,306826)
                                       )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("JetHTAnalysis.root"),	
                                   closeFileFast = cms.untracked.bool(False)
                                   )

process.p = cms.Path(process.offlineBeamSpot                        + 
                     process.TrackRefitter                          + 
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.jetHTAnalyzer)


