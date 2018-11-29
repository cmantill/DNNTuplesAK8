import os
from argparse import ArgumentParser
import ROOT 

#parser = ArgumentParser()
#arser.add_argument("--include", help="Path to training sample", default=)
#args=parser.parse_args()
#print(args.include)


#names = ["QCD", "Glu", "Bul", "GluGluH"]
#names = ["GluGluH"]
names = ["Bulk", "qcd"]

dcap = "dcap://grid-dcap-extern.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/user/anovak"
srm = "srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/anovak"
fnal = True
if fnal:dirs = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/").read().split("\n")
else:	dirs = os.popen("gfal-ls "+srm).read().split("\n")

print "Processsing directories starting with: ", names
print "======================================="
all_files = []
for i, d in enumerate(dirs):
	#print i, d
	dir_files = []
	go = False
	for name in names:
		if d.startswith(name): go = True
	if not go: continue
	print d
	if fnal:
		sds = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/"+d).read().split("\n")
		for sd in sds:
			if not sd.endswith(tuple(["madgraph", "pythia8"])):continue 
			sd2 = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/"+d+"/"+sd).read().split("\n")[0]
			sd3 = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/"+d+"/"+sd+"/"+sd2).read().split("\n")[0]
			sd4 = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/"+d+"/"+sd+"/"+sd2+"/"+sd3).read().split("\n")[0]
			files = os.popen("eos root://cmseos.fnal.gov ls /store/group/lpchbb/20180524_ak8_94x/"+d+"/"+sd+"/"+sd2+"/"+sd3+"/"+sd4).read().split("\n")
			path = "root://cmseos.fnal.gov//store/group/lpchbb/20180524_ak8_94x/"+d+"/"+sd+"/"+sd2+"/"+sd3+"/"+sd4+"/"
			files = [path+f for f in files if f.endswith("root")]
	
			with open("2017lists/"+sd+".txt", 'w') as f:
				        f.write('\n'.join(files))
	
	else:
		sd = os.popen("gfal-ls "+srm+"/"+d).read().replace("\n", "")
		sd2 = os.popen("gfal-ls "+srm+"/"+d+"/"+sd).read().replace("\n", "")
		sd3 = os.popen("gfal-ls "+srm+"/"+d+"/"+sd+"/"+sd2).read().replace("\n", "")
		files = os.popen("gfal-ls "+srm+"/"+d+"/"+sd+"/"+sd2+"/"+sd3).read().split("\n")

	if not fnal:
		path = dcap+"/"+d+"/"+sd+"/"+sd2+"/"+sd3
		for f in files:
			if not f.endswith("root"): continue
			all_files.append(path+"/"+f)
			dir_files.append(path+"/"+f)


		with open("lists/"+d+".txt", 'w') as f:
		        f.write('\n'.join(dir_files))
        #print 'Write training/validation files to %s' % os.path.join(inputdir, 'train_val_samples.txt')
