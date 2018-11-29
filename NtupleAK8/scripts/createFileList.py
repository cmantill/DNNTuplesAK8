#!/usr/bin/env python
import os
import sys
import re
import argparse
import logging

dcap = "dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/anovak/"
srm = "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/anovak"
#test = os.system("gfal-ls "+dcap)
print("X")

def create(inputdir):
    train_files = []
    test_files = []

    for dp, dn, filenames in os.walk(inputdir):
        if 'failed' in dp or 'ignore' in dp:
            continue
        for f in filenames:
            print f
            if not f.endswith('.root'):
               continue
            realdir =  "dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/anovak/"+ dp[len("/afs/cern.ch/user/a/anovak/eos/"):]
            
            fullpath = os.path.join(realdir, f)
            print(fullpath)
            try:
                filesize = 10001 #os.path.getsize(fullpath)
                if filesize > 1000:
                    relpath = os.path.relpath(fullpath, start=inputdir)
                    #print relpath.endswith('7.root', '8.root', '9.root')
                    #if 'test_sample' in dp:
                    if fullpath.endswith(('7.root', '8.root', '9.root')):
                       # print "TESTFILE"
                        test_files.append(fullpath)
                    else:
                        #print "TRAINFILE"
                        train_files.append(fullpath)
                else:
                    logging.warning('Ignore file %s: size=%d' % (fullpath, filesize))
            except OSError:
                logging.warning('Ignore file %s: IO Error' % fullpath)

    print(os.path.join(inputdir, 'train_samples.txt'))
    with open('testing_dcap.txt', 'w') as f:
        f.write('\n'.join(train_files))
        print 'Write training/validation files to %s' % os.path.join(inputdir, 'train_samples.txt')
    #with open(os.path.join(inputdir, 'train_samples.txt'), 'w') as f:
    #    f.write('\n'.join(train_files))
       # print 'Write training/validation files to %s' % os.path.join(inputdir, 'train_samples.txt')

    #with open(os.path.join(inputdir, 'test_samples.txt'), 'w') as f:
    #    f.write('\n'.join(test_files))
       # print 'Write testing files to %s' % os.path.join(inputdir, 'test_samples.txt')

def main():
    parser = argparse.ArgumentParser(description='Create filelist for merging.\nFiles reserved for testing should be placed in *test_sample* directory!')
    parser.add_argument("inputdir", help="Input (parent) directory for a specific sample.")
    args = parser.parse_args()

    subdirs = os.listdir(args.inputdir)
    for s in subdirs:
        p = os.path.join(args.inputdir, s)
        if os.path.isdir(p):
            print(p)
            create(p)

if __name__ == '__main__':
    #import os
    #dcap = "dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/anovak/"
    #test = os.system("gfal-ls "+dcap)
    #print test

    main()
