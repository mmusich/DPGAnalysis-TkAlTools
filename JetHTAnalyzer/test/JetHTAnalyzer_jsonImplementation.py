'''
cfg to produce alignment validation plots from JetHT sample 
here doing refit of tracks and vertices using latest alignment 
'''

import FWCore.ParameterSet.Config as cms
process = cms.Process("JetHTAnalyzer")

# Choose whether to run with Monte Carlo or data settings based on command line argument
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing()
options.register ('configurationFile',
                  "jethtConfiguration.json", # Default file
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "JetHT analysis configuration file in json format.")
options.parseArguments()

jsonConfig = options.configurationFile

#Read the configuration file
import json
with open(jsonConfig, "r") as jsonFile:
    configuration = json.load(jsonFile)

# Read parameters from the configuration file
useMC = configuration["jetht"]["mc"]
printTriggers = configuration["jetht"]["printTriggers"]
iovListList = configuration["jetht"]["iovList"]
globalTag = str(configuration["jetht"]["globalTag"])
pixelTemplate = str(configuration["jetht"]["SiPixelTemplateDBObjectRecord"])
trackerAlignment = str(configuration["jetht"]["TrackerAlignmentRcd"])
trackerAlignmentError = str(configuration["jetht"]["TrackerAlignmentErrorExtendedRcd"])
alignmentErrorFile = str(configuration["jetht"]["TrackerAlignmentErrorFile"])
surfaceDeformation = str(configuration["jetht"]["TrackerSurfaceDeformationRcd"])
trackCollection = configuration["jetht"]["trackCollection"]

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

# Input files. Choose different test input fule for MC and data

if useMC:
  process.source = cms.Source("PoolSource",
                              fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/mc/RunIIWinter19PFCalibDRPremix/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/ALCARECO/TkAlMinBias-2017Conditions_105X_mc2017_realistic_v5-v1/250000/134A5981-A7F5-AF49-9288-A99820BBEEE0.root')
                              )
else:
  process.source = cms.Source("PoolSource",
                              fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/user/jviinika/TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/TrackAlignment_jetHTreconstruction/crab_TkAlJetHTReconstruction_Run2017ABCDEF-v1_10keventPerIov/190305_003651/0000/TkAlJetHT_2.root')

                              )

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")

# The global tag is defined in the configuration file

process.GlobalTag.globaltag = globalTag


# Option to refit the tracks with the latest alignment and APE tags provided in the configuration file
import CalibTracker.Configuration.Common.PoolDBESSource_cfi

# If requested, read pixel template object records
if not (pixelTemplate == "nothing" or pixelTemplate == ""):

  process.conditionsInSiPixelTemplateDBObjectRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('SiPixelTemplateDBObjectRcd'),
                                 tag = cms.string(pixelTemplate)
                                 )
                        )
      )
  process.prefer_conditionsInSiPixelTemplateDBObjectRcd = cms.ESPrefer("PoolDBESSource", "conditionsInSiPixelTemplateDBObjectRcd")

# If requested, read the tracker alignment records
if not (trackerAlignment == "nothing" or trackerAlignment == ""):

  process.conditionsInTrackerAlignmentRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentRcd'),
                                 tag = cms.string(trackerAlignment)
                                 )
                        )
      )
  process.prefer_conditionsInTrackerAlignmentRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentRcd")

# If requested, read the tracker alignment error record
if not (trackerAlignmentError == "nothing" or trackerAlignmentError == ""):
  process.conditionsInTrackerAlignmentErrorExtendedRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                 tag = cms.string(trackerAlignmentError)
                                 )
                        )
      )
  process.prefer_conditionsInTrackerAlignmentErrorExtendedRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentErrorExtendedRcd")

# If the reference to the databese is not provided, check if a database file is provided
elif not (alignmentErrorFile == "nothing" or alignmentErrorFile == ""):
  process.conditionsInTrackerAlignmentErrorExtendedRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string("sqlite_file:" + alignmentErrorFile),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
                                 tag = cms.string('APEs')
                                 )
                        )
      )
  process.prefer_conditionsInTrackerAlignmentErrorExtendedRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerAlignmentErrorExtendedRcd")

# If requested, read the surface deformation record
if not (surfaceDeformation == "nothing" or surfaceDeformation == ""):
  process.conditionsInTrackerSurfaceDeformationRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
       connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
       toGet = cms.VPSet(cms.PSet(record = cms.string('TrackerSurfaceDeformationRcd'),
                                 tag = cms.string(surfaceDeformation)
                                 )
                        )
      )
  process.prefer_conditionsInTrackerSurfaceDeformationRcd = cms.ESPrefer("PoolDBESSource", "conditionsInTrackerSurfaceDeformationRcd")


# Setup track refitter
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
# remove the following lines if you run on RECO files
process.TrackRefitter.src = trackCollection
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
                                       iovList = cms.untracked.vint32(iovListList)
                                       )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("JetHTAnalysis.root"),	
                                   closeFileFast = cms.untracked.bool(False)
                                   )

process.p = cms.Path(process.offlineBeamSpot                        + 
                     process.TrackRefitter                          + 
                     process.offlinePrimaryVerticesFromRefittedTrks +
                     process.jetHTAnalyzer)


