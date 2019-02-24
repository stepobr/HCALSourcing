import FWCore.ParameterSet.Config as cms
                #erwarn['Non-existentent combination Eta/Phi/Layer'] += 1
                #continue
            
            #if heDepths[mapKey] != depth:
                #erwarn['Skipping data not associated with tube'] += 1
                #continue

process = cms.Process("HCALSourceDataMonitor")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load('FWCore.Modules.printContent_cfi')

process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'MCRUN2_74_V8A'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2018_realistic', '')
process.es_ascii = cms.ESSource('HcalTextCalibrations',
    input = cms.VPSet(
        cms.PSet(
            object = cms.string('ElectronicsMap'),
            file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/ngHF2017EMap_20170206_pre05.txt')
            #file = cms.FileInPath('HCALSourcing/HCALSourceDataMonitor/emap_versionG_ngHF20170206_HEP17_CRF.txt')
            ),
	)
    )
process.es_prefer = cms.ESPrefer('HcalTextCalibrations','es_ascii')


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# input files
process.source = cms.Source("HcalTBSource",
    fileNames = cms.untracked.vstring(
 	#'file:///data/sourcing/USC1702/USC_288697.root'
        'root://eoscms//eos/cms/store/group/dpg_hcal/comm_hcal/USC/run289134/USC_289134.root'
        #'file:///data/sourcing/USC1702/USC_288690.root'
    )
)

# TB data unpacker
process.tbunpack = cms.EDProducer("HcalTBObjectUnpacker",
    HcalSlowDataFED = cms.untracked.int32(-1),
    HcalSourcePositionFED = cms.untracked.int32(12),
    HcalTriggerFED = cms.untracked.int32(1),
    fedRawDataCollectionTag = cms.InputTag('source')
)

process.histoUnpack = cms.EDProducer("HcalUTCAhistogramUnpacker",
          fedRawDataCollectionTag = cms.InputTag("source"),
          rawDump = cms.bool(False),
          fedNumbers = cms.vint32(64,61,60))

# Tree-maker
process.hcalSourceDataMon = cms.EDAnalyzer('HCALSourceDataMonitor',
    #RootFileName = cms.untracked.string('/data/sourcing/Ntuples1702/ntuple_da_288924.root'),
    RootFileName = cms.untracked.string('/data/sourcing/Ntuples1702/ntuple_da_289134.root'),
    #PrintRawHistograms = cms.untracked.bool(False),
    #SelectDigiBasedOnTubeName = cms.untracked.bool(True),
    SelectDigiBasedOnTubeName = cms.untracked.bool(True),
    HcalSourcePositionDataTag = cms.InputTag("tbunpack"),
    hcalTBTriggerDataTag = cms.InputTag("tbunpack"),
    HcalUHTRhistogramDigiCollectionTag = cms.InputTag("histoUnpack"),
)

process.p = cms.Path(
		     process.tbunpack
                     *process.histoUnpack
#		     *process.printContent
                     *process.hcalSourceDataMon
                    )

