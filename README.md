# DNNTuplesAK8

## Setup
```bash
cmsrel CMSSW_8_0_28
cd CMSSW_8_0_28/src/
cmsenv
git clone https://github.com/anovak10/DNNTuplesAK8 DeepNTuples
scram b -j4
```

## Submit jobs via CRAB

```bash
# Set up CRAB env; run it after cmsenv
#source /cvmfs/cms.cern.ch/crab3/crab.sh
source crab.sh
voms-proxy-init -rfc -voms cms --valid 168:00
# German grid
#voms-proxy-init --voms cms:/cms/dcms --valid 168:00"

# Create the CRAB config files
cd DeepNTuples/NtupleAK8/run
# -o path goes by default to /store/user/$USERNAME/+[-o input]
python makeCrabJobs.py -i samples/[name].conf -o 80x #--site [T2_CH_CERN|T3_US_FNALLPC|...]
# Check if config is correct in crab_projects/crab_*
# Submit jobs
bash submit_[name].conf
```

To check all the options of the submission script, run
```
./makeCrabJobs.py -h
```

Currently disabled: You can set arguments to be passed to the cmsRun job in the beginning of the sample.conf file, e.g.,
~~fjKeepFlavors=2,3,4   # only keep fatjets whose labels match to the given number. 0:Light, 1:Top, 2:W, 3:Z, 4:Higgs~~
 
## Merge outputs (with random mixing of different samples)

1. First create the file list.

N.B. **Files reserved for testing should be placed in a `test_sample` directory by hand before proceeding**!

```bash
cd DeepNTuples/NtupleAK8/run
./createFileList.py [/eos/cms/store/user/$USER/DeepNtuples/output_dir/ttbar]
```
Note that you need to run this for every sample you produced, e.g., ttbar, qcd, etc.

2. Merge the samples (with random mixing)

```bash
# Make lists of files to merge, e.g. Mix all qcd statistics to uniform per file distribution.
python Utilities/scripts/makeRemoteSampleLists.py  # Might need modifications to your specifics storage space
# python Utilities/scripts/mergeSamples.py [events per output file] [output dir] [paths to file lists]
python Utilities/scripts/mergeSamples.py 200000 qcd lists/QCD_Pt_*txt
# Make lists of files for training and testing.
python Utilities/scripts/makeLocalSampleLists.py  # Might need modifications to your specifics storage space


