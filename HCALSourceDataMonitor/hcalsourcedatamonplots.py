import FWCore.ParameterSet.Config as cms

process = cms.PSet()


process.HCALSourceDataMonPlots = cms.PSet(
    RootInputFileName = cms.string('264742.root'),
    RootOutputFileName = cms.string('264742_plots.root'),
    NewRowEvery = cms.int32(2),
    ThumbnailSize = cms.int32(350),
    OutputRawHistograms = cms.bool(False),
    SelectDigiBasedOnTubeName = cms.bool(True),
    MaxEvents = cms.int32(2000000),
    HtmlFileName = cms.string('index.html'),
    HtmlDirName = cms.string('html'),
    PlotsDirName = cms.string('plots')

)
