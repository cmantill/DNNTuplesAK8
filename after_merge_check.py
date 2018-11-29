import ROOT
import numpy as np
import os
ROOT.gROOT.SetBatch()
#from histogrammar import *

path = "/eos/user/a/anovak/merged_QCD_Hcc/train/"
contents = os.listdir(path)
files = []
for f in contents:
	if f.endswith("root"): files.append(f)

for f in files:
	pt_qcd = ROOT.TH1F(f[:-5]+"qcd", "Pt [GeV]",50, 0, 2000)
	pt_H = ROOT.TH1F(f[:-5]+"H","Pt [GeV]",50, 0, 2000)	
	F = ROOT.TFile(path+f)	
	tree = F.Get("deepntuplizer/tree")
	tot = tree.GetEntries()
	n = 5000	
	pts = []
	H, QCD = 0 , 0
	for i in range(n):
		tree.GetEntry(i)
		pt = tree.fj_pt	
		pts.append(pt)
		H += tree.fj_isH
		QCD += tree.fj_isQCD
		if float(tree.fj_isH) != 0.:
			pt_H.Fill(pt)
		if float(tree.fj_isQCD) != 0.:
			pt_qcd.Fill(pt)

	print "==================================================================="
	print "File:", f, "In subset of ", n, "entries, file total:", tot
	print round(H/float(n)*100, 2),"% Higgs", round(QCD/float(n)*100, 2),"% QCD"
	print "Mean pt", np.mean(pts), "Median pt", np.median(pts)

	C = ROOT.TCanvas()
	C.cd
	pt_H.Scale(1/pt_H.Integral())
	pt_qcd.Scale(1/pt_qcd.Integral())
	pt_H.SetLineColor(1)
	pt_qcd.SetLineColor(2)
	pt_H.GetYaxis().SetRangeUser(0, max(pt_H.GetMaximum(), pt_qcd.GetMaximum()*1.3))
	pt_H.Draw()
	pt_qcd.Draw("same")
	C.SaveAs("pt_"+f+".png")

	F.Close()

