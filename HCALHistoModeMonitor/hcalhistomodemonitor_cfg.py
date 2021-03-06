import FWCore.ParameterSet.Config as cms

process = cms.Process("HCALHistoModeMonitor")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load('FWCore.Modules.printContent_cfi')

process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.es_ascii = cms.ESSource('HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(
            object = cms.string('ElectronicsMap'),
            #file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/version_G_emap_HBHEuHTR.txt'),
            file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/ngHF2017EMap_20170206_pre05.txt')
            #file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/emap_versionG_ngHF20170206_HEP17_CRF.txt')            
            ),
	)
    )
process.es_prefer = cms.ESPrefer('HcalTextCalibrations','es_ascii')


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

# input files
process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(
        'root://eoscms//eos/cms/store/group/dpg_hcal/comm_hcal/USC/run289928/USC_289928.root'
        #'file:///data/sourcing/USC1702/USC_289928.root'
    )
)

# TB data unpacker
process.tbunpack = cms.EDProducer("HcalTBObjectUnpacker",
    HcalSlowDataFED = cms.untracked.int32(-1),
    #HcalSourcePositionFED = cms.untracked.int32(12),
    HcalTriggerFED = cms.untracked.int32(1),
    fedRawDataCollectionTag = cms.InputTag('source')
)

process.histoUnpack = cms.EDProducer("HcalUTCAhistogramUnpacker",
          fedRawDataCollectionTag = cms.InputTag("source"),
          rawDump = cms.bool(False),
	  fedNumbers = cms.vint32(62,60))

# Tree-maker
process.hcalHistoModeMonitor = cms.EDAnalyzer('HCALHistoModeMonitor',
    #RootFileName = cms.untracked.string('/wwwlocal/p5sourcing/grandr/Ana/Tests/scratch/HCALHistoModeMonitor.289928.root'),
    RootFileName = cms.untracked.string('HCALHistoModeMonitor.289928.root'),
    PrintRawHistograms = cms.untracked.bool(False),
    SelectDigiBasedOnTubeName = cms.untracked.bool(False),
    #HcalSourcePositionDataTag = cms.InputTag("tbunpack"),
    hcalTBTriggerDataTag = cms.InputTag("tbunpack"),
    HcalUHTRhistogramDigiCollectionTag = cms.InputTag("histoUnpack"),
)

process.p = cms.Path(
		     process.tbunpack
                     *process.histoUnpack
#		     *process.printContent
                     *process.hcalHistoModeMonitor
                    )

