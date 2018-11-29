import os

dirs = ['Hcc', 'Hbb', "qcd"]
dirs = ['Z']
for d in dirs:
	tests = os.listdir(d+"/test")
	f = open("list_test_{}.txt".format(d), "w")
	for line in tests:
		f.write(d+"/test/"+line+"\n")
	f.close()
	
	trains = os.listdir(d)
	f = open("list_{}.txt".format(d), "w")
	for line in trains:
		if not line.endswith(".root"): continue
		f.write(d+"/"+line+"\n")
	f.close()
	
