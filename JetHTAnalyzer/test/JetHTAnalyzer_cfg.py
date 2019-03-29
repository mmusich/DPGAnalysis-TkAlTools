'''
cfg to produce alignment validation plots from JetHT sample 
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms
process = cms.Process("JetHTAnalyzer")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/tmp/musich/CMSSW_10_4_0/src/Alignment/JetHTAnalyzer/test/TkAlMinBias.root')
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
                                       minVertexMeanWeight = cms.untracked.double(0.5)
                                       )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("JetHTAnalysis.root"),	
                                   closeFileFast = cms.untracked.bool(False)
                                   )

process.p = cms.Path(process.offlineBeamSpot                        + 
                     process.TrackRefitter                          + 
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.jetHTAnalyzer)


