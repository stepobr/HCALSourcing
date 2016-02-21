# HCALSourcing

# set up a CMSSW release area
cmsrel CMSSW_7_6_0_pre2
cd CMSSW_7_6_0_pre2/src/
cmsenv
# merge in private Unpacker code by Andrew Evans
git cms-merge-topic UMN-CMS:QIE1011Unpacker
# get the HCALSourcing analyzers
git clone git@github.com:sethcooper/HCALSourcing
# build
scram b -j 4
cd HCALSourcing/HCALSourceDataMonitor
# To run the unpacker and ntuple maker
cmsRun hcalsourcedatamonitor_cfg.py
# To obtain plots for express monitoring
hcalSourceDataMonPlots hcalsourcedatamonplots.py
