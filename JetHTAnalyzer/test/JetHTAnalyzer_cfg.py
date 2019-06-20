'''
cfg to produce alignment validation plots from JetHT sample 
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms
process = cms.Process("JetHTAnalyzer")

# Choose whether to run with Monte Carlo or data settings based on command line argument
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register ('mc',
                  0, # False
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "1 = Run MC analysis. 0 = Run data analysis.")
options.register ('printTriggers',
                  0, # False
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "0 = Run analysis regularly. 1 = Print trigger table to console.")
options.register ('errorFile',
                  "nothing", # No default file
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "Name of the .db file from which ExtendedErrorRecord is read.")
options.parseArguments()

useMC = options.mc
printTriggers = options.printTriggers
errorFile = options.errorFile

###################################################################
# Messages
###################################################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')

if useMC:
  process.source = cms.Source("PoolSource",
                              #fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/RunIIWinter19PFCalibDRPremix/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/ALCARECO/TkAlMinBias-2017Conditions_105X_mc2017_realistic_v5-v1/10000/EBF8B22E-50A1-F247-920A-23F1BF46F0AF.root')
                              fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIIWinter19PFCalibDRPremix/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/ALCARECO/TkAlMinBias-2017Conditions_105X_mc2017_realistic_v5-v1/250000/134A5981-A7F5-AF49-9288-A99820BBEEE0.root')
                              )
else:
  process.source = cms.Source("PoolSource",
                              fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/user/jviinika/TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/TrackAlignment_jetHTreconstruction/crab_TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/190305_003651/0000/TkAlJetHT_2.root')

                              )

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")

if useMC:
  process.GlobalTag.globaltag = '105X_mc2017_realistic_v5'
else:  
  process.GlobalTag.globaltag = '104X_dataRun2_v1'

# Append alignment condition to the global tag
# Note: This is equivalent with the uncommented conditionsInXXX syntax
# Only one of these must the uncommented at the same time.
#process.GlobalTag.toGet.append(
#cms.PSet(
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#  record = cms.string("SiPixelTemplateDBObjectRcd"),
#  tag = cms.string("SiPixelTemplateDBObject_38T_v15_offline")),
#)
#
#process.GlobalTag.toGet.append(
#cms.PSet(
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#  record = cms.string("TrackerAlignmentRcd"),
#  tag = cms.string("TrackerAlignment_2017_ultralegacy_v1")),
#)
#
#process.GlobalTag.toGet.append(
#cms.PSet(
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#  record = cms.string("TrackerAlignmentErrorExtendedRcd"),
#  tag = cms.string("TrackerAlignmentExtendedErrors_2017_ultralegacy_v2")),
#)
#
#process.GlobalTag.toGet.append(
#cms.PSet(
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
#  record = cms.string("TrackerSurfaceDeformationRcd"),
#  tag = cms.string("TrackerSurfaceDeformations_2017_ultralegacy_v1")),
#)

# Refit the tracks with the latest alignment and APE tags from the UL2017 campaign
import CalibTracker.Configuration.Common.PoolDBESSource_cfi
if not useMC:

  process.conditionsInSiPixelTemplateDBObjectRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('SiPixelTemplateDBObjectRcd'),
                                 tag = cms.string('SiPixelTemplateDBObject_38T_v15_offline')
                                 )
                        )
      )
  process.prefer_conditionsInSiPixelTemplateDBObjectRcd = cms.ESPrefer("PoolDBESSource", "conditionsInSiPixelTemplateDBObjectRcd")

  process.conditionsInTrackerAlignmentRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentRcd'),
                                 tag = cms.string('TrackerAlignment_2017_ultralegacy_v1')
                                 )
                        )
      )
  process.prefer_conditionsInTrackerAlignmentRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentRcd")

  # Load TrackerAlignmentErrorExtendedRcd from a tag
  if errorFile == "nothing":
    process.conditionsInTrackerAlignmentErrorExtendedRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
         connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
         toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                   tag = cms.string('TrackerAlignmentExtendedErrors_2017_ultralegacy_v2')
                                   )
                          )
        )

  # Load TrackerAlignmentErrorExtendedRcd from a database file instead of tag
  else:
    process.conditionsInTrackerAlignmentErrorExtendedRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
         connect = cms.string("sqlite_file:" + errorFile),
         toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                   tag = cms.string('APEs')
                                   )
                          )
        )

  # The prefer statement in common for the two above TrackerAlignmentErrorExtendedRcd blocks
  process.prefer_conditionsInTrackerAlignmentErrorExtendedRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentErrorExtendedRcd")

  # Block for the surface deformations

  process.conditionsInTrackerSurfaceDeformationRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerSurfaceDeformationRcd'),
                                 tag = cms.string('TrackerSurfaceDeformations_2017_ultralegacy_v1')
                                 )
                        )
      )
  process.prefer_conditionsInTrackerSurfaceDeformationRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerSurfaceDeformationRcd")

# Configuration for Monte Carlo running
else:

  # Load TrackerAlignmentRcd from a database file
  process.conditionsInTrackerAlignmentRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('sqlite_file:alignments_MC2017_MP.db'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentRcd'),
                                 tag = cms.string('Alignments')
                                 )
                        )
      )
  process.prefer_conditionsInTrackerAlignmentRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentRcd")

  # If a file is provided, load TrackerAlignmentErrorExtendedRcd from a database file
  if errorFile != "nothing":
    process.conditionsInTrackerAlignmentErrorExtendedRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
         connect = cms.string("sqlite_file:" + errorFile),
         toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                   tag = cms.string('APEs')
                                   )
                          )
        )
    process.prefer_conditionsInTrackerAlignmentErrorExtendedRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentErrorExtendedRcd")


# Setup track refitter
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
                                       vtxCollection       = cms.InputTag("offlinePrimaryVerticesFromRefittedTrks"),
                                       trackCollection	   = cms.InputTag("TrackRefitter"),		
                                       triggerResults      = cms.InputTag("TriggerResults","","HLT"),
                                       printTriggerTable   = cms.untracked.int32(printTriggers),
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


