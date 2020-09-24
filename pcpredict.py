#!/opt/websites/anaconda/bin/python3.7
import cgi, os
import sys
import time
import shutil
import subprocess
import math
import numpy as np
from os import path
import uuid
import cgitb; cgitb.enable()
import timeit
start = timeit.default_timer()

ions_list=['HOH','AG1', 'AG', 'AL', 'AM', 'AS1', 'AS7', 'AS', 'AU1', 'AU2', 'AU', 'BA', 'BE', 'BI', 'CA1', 'CA', 'CD', 'CE', 'CF', \
'CM', 'CO3', 'CO', 'CR', 'CS', 'CU1', 'CU2', 'CU3', 'CU4', 'CU', 'DY', 'ER', 'EU', 'FE1', 'FE2', 'FE3', 'FE4', 'FE5', 'FE6', \
'FE7', 'FE8', 'FE9', 'FE', 'GA1', 'GA2', 'GA', 'GD', 'HF1', 'HFA', 'HFB', 'HFC', 'HFD', 'HFE', 'HG1', 'HG3', 'HG', 'HO5', 'HO', \
'IN', 'IR1', 'IR', 'K', 'LA', 'LI', 'LU', 'MG1', 'MG', 'MN1', 'MN2', 'MN3', 'MN4', 'MN', 'MO10', 'MO1', 'MO2', 'MO3', 'MO4', 'MO5',\
 'MO6', 'MO7', 'MO8', 'MO', 'MOM1', 'NA', 'NI1', 'NI', 'OS02', 'OS1', 'OS', 'PA', 'PB1', 'PB', 'PD1', 'PD', 'PR', 'PT1', 'PT2', 'PT', \
 'PU', 'RB', 'RE', 'RH1', 'RH', 'RU11', 'RU12', 'RU15', 'RU18', 'RU1', 'RU20', 'RU2', 'RU3', 'RU4', 'RU', 'SB', 'SC', 'SM', 'SN1', 'SN7',\
  'SR1', 'SR', 'TA1', 'TA2', 'TA3', 'TA4', 'TA5', 'TA6', 'TA', 'TB', 'TH', 'TI', 'TL', 'U', 'UNK', 'UNL', 'V02', 'V06', 'V10', 'V16', 'V1',\
   'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V', 'VB', 'VG', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16', 'W17', 'W18', 'W19', 'W1',\
    'W20', 'W21', 'W22', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'WA', 'W', 'WB', 'Y1', 'Y', 'YB', 'ZN', 'ZR1', 'ZR2', 'ZR3','SO4','SO3',\
    'SO2','EOH','CL','ACT','2HP', '3CO', '4PU', '4TI', 'ACT', 'ALF', 'AUC', 'AZI', 'BCT', 'BEF', 'BO4', 'BR', 'BS3', 'BSY', 'CAC', 'CHT', 'CL', 'CYN',\
     'DME', 'EMC', 'EU3', 'F', 'GD3', 'HAI', 'IOD', 'IR3', 'IUM', 'LCP', 'MLI', 'MMC', 'MOO', 'MOS', 'NH4', 'NO2', 'NO3', 'OAA', 'OH', 'OS4', 'OXL',\
      'PER', 'PI', 'PO3', 'PO4', 'SCN', 'SE4', 'SO3', 'SO4', 'TMA', 'VO4', 'YT3', 'ZCM', 'ZR']


#os.system("find -mmin +20 -type d -exec rmdir !('tmp') > files_older_last_deleted 2>&1")
#find dir_* -mmin +34 -type d -exec rm -r {} \;

if __name__ == '__main__':
	
	form = cgi.FieldStorage()

	if form.getvalue('fname')!='' and form.getvalue('chain')!='' and form.getvalue('lchain')!='' and form.getvalue('pdb')==b'':
		pdb_id_up=form.getvalue('fname').upper()
		chain=form.getvalue('chain')
		lchain=form.getvalue('lchain')
		sugar=form.getvalue('sugar')
		method=1
	elif form.getvalue('fname')!='' and form.getvalue('chain')!='' and form.getvalue('lchain')=='' and form.getvalue('pdb')==b'':
		pdb_id_up=form.getvalue('fname').upper()
		chain=form.getvalue('chain')
		lchain=form.getvalue('chain')
		sugar=form.getvalue('sugar')
		method=1
	elif form.getvalue('fname')=='' and form.getvalue('chain')!='' and form.getvalue('pdb')==b'':
		print ('Content-Type: text/html\r\n')
		print ('<html><head><title>Input error</title><body>PDB ID is missing</body></html>')
		exit()
	elif form.getvalue('fname')!='' and form.getvalue('chain')=='' and form.getvalue('pdb')==b'':
		print ('Content-Type: text/html\r\n')
		print ('<html><head><title>Input error</title><body>Chain ID is missing</body></html>')
		exit()
	elif form.getvalue('fname')=='' and form.getvalue('chain')!='' and form.getvalue('lchain')!='' and form.getvalue('pdb')!=b'':
		fileitem = form['pdb']
		chain=form.getvalue('chain')
		lchain=form.getvalue('lchain')
		sugar=form.getvalue('sugar')
		method=2
		#print (fileitem.filename)
		if fileitem.filename:
			fn = os.path.basename(fileitem.filename)
			open('tmp/' + fn, 'wb').write(fileitem.file.read())
	elif form.getvalue('fname')=='' and form.getvalue('chain')!='' and form.getvalue('lchain')=='' and form.getvalue('pdb')!=b'':
		fileitem = form['pdb']
		chain=form.getvalue('chain')
		lchain=form.getvalue('chain')
		sugar=form.getvalue('sugar')
		method=2
		#print (fileitem.filename)
		if fileitem.filename:
			fn = os.path.basename(fileitem.filename)
			open('tmp/' + fn, 'wb').write(fileitem.file.read())
	else:
		print ('Content-Type: text/html\r\n')
		print ('<html><head><title>Input error</title><body>No input found</body></html>')
		exit()
	model=form.getvalue('complex_type')

	if model=="None":
		print ('Content-Type: text/html\r\n')
		print ('<html><head><title>Please select the classfication model</title><body>Chain ID is missing</body></html>')
		exit()

	if model=='polysacc':
		modeltype="Oligosaccharide Classification"
	elif model=='trisacc':
		modeltype="Trisaccharide Classification"
	elif model=='disacc':
		modeltype="Disaccharide Classification"
	elif model=='mosacmono':
		modeltype="Monomer-Monosaccharide Classification"
	elif model=='mosacdi':
		modeltype="Dimer-Monosaccharide Classification"
	elif model=='mosacoli':
		modeltype="Oligomer-Monosaccharide Classification"


#########################################################################################################    Monosaccharide and Monomer      ###########################################################################################################
#########################################################################################################    Monosaccharide and Monomer      ###########################################################################################################
#########################################################################################################    Monosaccharide and Monomer      ###########################################################################################################
#########################################################################################################    Monosaccharide and Monomer      ###########################################################################################################


	if model=='mosacmono':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")
		elif method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')
				#print ("Use this url to obtain data: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+chain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+chain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			resultout.write(str(chain))
			resultout.write("\n")
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

			allproatms=['O-', 'N+', 'C', 'O', 'N', 'S']
			allhetatms=['C', 'F', 'H', 'CL', 'O', 'N', 'P', 'S']

			allproatoms=[]
			allhetatoms=[]
			proatoms=[]
			ligatoms=[]
			contcombo=[]
			reses=[]
			lig=[]
			residues=[]
			ligands=[]

			dictnor={'C_C':[50.28,1.39,18.93,27.298,7.44,35.759], 'C_CL':[0.16,5.34,0.08,0.018,6.00,0.034], 'C_F':[0.19,8.02,0.03,0.013,5.43,0.018], \
			'C_H':[39.70,10.09,6.29,3.456,8.66,4.035], 'C_N':[4.70,1.99,1.44,1.828,7.62,2.365], 'C_O':[148.74,5.47,25.28,22.486,8.16,25.133], \
			'C_P':[0.23,0.38,0.11,0.530,8.76,0.538], 'C_S':[0.75,1.78,0.31,0.334,7.82,0.427], 'N_C':[15.55,1.90,4.10,5.376,6.49,7.115], \
			'N_CL':[0.00,0.00,0.00,0.004,6.50,0.008], 'N_F':[0.04,8.29,0.01,0.003,6.50,0.005], 'N_H':[5.11,5.76,0.57,0.758,8.42,0.894], \
			'N_N':[1.54,2.89,0.33,0.418,7.72,0.546], 'N_O':[57.88,9.44,6.90,5.663,9.10,6.395], 'N_P':[0.80,5.92,0.27,0.209,15.27,0.214], \
			'N_S':[0.00,0.00,0.00,0.074,7.64,0.095], 'N+_C':[5.12,3.30,1.12,1.530,9.71,1.466], 'N+_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'N+_F':[0.01,11.42,0.00,0.004,35.03,0.004], 'N+_H':[0.56,3.34,0.05,0.086,5.00,0.073], 'N+_N':[0.18,1.73,0.03,0.065,6.31,0.062],\
			'N+_O':[13.46,11.53,1.33,1.540,13.00,1.259], 'N+_P':[0.21,8.15,0.06,0.051,19.44,0.037], 'N+_S':[0.18,10.15,0.04,0.028,15.42,0.026],\
			'O_C':[56.37,6.05,14.40,6.075,6.43,8.405], 'O_CL':[0.00,0.00,0.00,0.001,1.55,0.002], 'O_F':[0.05,8.52,0.01,0.004,6.21,0.006], \
			'O_H':[7.13,7.04,0.77,0.812,7.90,1.001], 'O_N':[7.18,11.79,1.49,0.487,7.88,0.664], 'O_O':[45.56,6.51,5.25,6.095,8.59,7.195], \
			'O_P':[0.56,3.65,0.18,0.132,8.45,0.141], 'O_S':[0.21,1.89,0.06,0.055,5.01,0.074], 'O-_C':[17.36,10.92,2.63,2.030,12.60,1.587],\
			'O-_CL':[0.00,0.00,0.00,0.001,7.94,0.001], 'O-_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'O-_H':[1.67,9.69,0.11,0.232,13.24,0.162], \
			'O-_N':[0.84,8.09,0.10,0.107,10.19,0.083], 'O-_O':[14.15,11.85,0.97,1.740,14.38,1.161], 'O-_P':[0.04,1.66,0.01,0.009,3.44,0.006],\
			'O-_S':[0.14,7.73,0.02,0.011,5.85,0.008], 'S_C':[1.42,6.62,0.42,0.173,7.94,0.243], 'S_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'S_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'S_H':[0.04,1.90,0.01,0.007,3.12,0.009], 'S_N':[0.00,0.00,0.00,0.005,3.53,0.007], \
			'S_O':[1.02,6.36,0.14,0.124,7.62,0.149], 'S_P':[0.00,0.00,0.00,0.000,1.36,0.001], 'S_S':[0.00,0.00,0.00,0.001,2.31,0.001]}

			allproatoms35=[]
			allhetatoms35=[]
			proatoms35=[]
			ligatoms35=[]
			contcombo35=[]
			reses35=[]
			lig35=[]
			residues35=[]
			ligands35=[]
			copot1,copot2,copot3,copot4,copot5,copot6=0.0,0.0,0.0,0.0,0.0,0.0

			countatoms=0
			atom=[x.rstrip() for x in open("{}_atom.pdb".format(pdb_id_up)).readlines()]
			countatoms+=len(atom)
			allpa=["N+" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']]
			allpa.extend(["O-" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allpa.extend([x[76:78].strip() for x in atom if x[17:20].strip()+x[12:16].strip() not in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ','ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allproatoms.extend(allpa)
			hetatom=[x.rstrip() for x in open("{}_hetatom.pdb".format(pdb_id_up)).readlines()]
			allha=[x[76:78].strip() for x in hetatom]
			allhetatoms.extend(allha)
			for j in atom:
				AX1=float(j[30:38])
				AY1=float(j[38:46])
				AZ1=float(j[46:54])
				res=j[17:20]
				pos=j[22:26]
				atmname=j[12:16]
				if res.strip()+atmname.strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']:
					atm='N+'
				elif res.strip()+atmname.strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']:
					atm='O-'
				else:
					atm=j[76:78]
				#print atm
				for k in hetatom:
					HX1=float(k[30:38])
					HY1=float(k[38:46])
					HZ1=float(k[46:54])
					hetres=k[17:20]
					hetpos=k[22:26]
					hetatmname=k[12:16]
					hetatm=k[76:78]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						residues.append(res+pos)
						ligands.append(hetres+hetpos)
						proatoms.append(atm.strip())
						re=res.strip()+pos.strip()+atmname.strip()+" "+atm.strip()
						#print re
						reses.append(re)
						li=hetres.strip()+hetpos.strip()+hetatmname.strip()+" "+hetatm.strip()
						lig.append(li)
						ligatoms.append(hetatm.strip())
						contcombo.append(atm.strip()+"-"+hetatm.strip())
					if round(distance,3)<3.5:
						y=atm.strip()+"_"+hetatm.strip()
						copot1+=dictnor[y][0]
						copot2+=dictnor[y][1]
						copot3+=dictnor[y][2]
						copot4+=dictnor[y][3]
						copot5+=dictnor[y][4]
						copot6+=dictnor[y][5]
			selec_contact=['N+-O','O--C','O--O','O-C']

			c_no=contcombo.count('N+'+"-"+'O')
			c_o_c=contcombo.count('O-'+"-"+'C')
			c_oo=contcombo.count('O-'+"-"+'O')
			c_oc=contcombo.count('O'+"-"+'C')

			keyres_pci_5= len([x for x in binres5 if x[:3] in ["ASN","ARG","ASP","GLU","HIS","GLN"]])
			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break
			sec_struct=[]
			total=[]
			backHbond=[]
			sideHbond=[]
			energy_VdW=[]
			electro=[]
			energy_SolvP=[]
			energy_SolvH=[]
			energy_vdwclash=[]
			entrop_sc=[]
			entrop_mc=[]
			energy_torsion=[]
			backbone_vdwclash=[]
			energy_dipole=[]
			water=[]
			disulfide=[]
			energy_kon=[]
			partcov=[]
			energyIonisation=[]
			Hetero_Backbone_HBond=[]
			entr_complex=[]
			Hetero_Sidechain_Hbond=[]
			Sidechain_Accessibility=[]
			Mainchain_Accessibility=[]
			Sidechain_Contact_Ratio=[]
			Mainchain_Contact_Ratio =[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				sec_struct.append(n[7])
				total.append(float(n[8]))
				backHbond.append(float(n[9]))
				#sideHbond.append(float(n[10]))
				#energy_VdW.append(float(n[11]))
				electro.append(float(n[12]))
				energy_SolvP.append(float(n[13]))
				#energy_SolvH.append(float(n[14]))
				#energy_vdwclash.append(float(n[15]))
				#entrop_sc.append(float(n[16]))
				#entrop_mc.append(float(n[17]))
				energy_torsion.append(float(n[21]))
				Sidechain_Accessibility.append(float(n[32]))
				num=[i for i in sec_struct if i in ['E','B','b','e']]
			energy_torsion_total=sum(energy_torsion)

			######################################################        NACCESS              ######################################################
			p3=subprocess.Popen("./naccess {}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p3.wait()

			p4=subprocess.Popen("./naccess {}_combined.pdb -h".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			allatomcount=0
			totalside=0
			mainchain=0
			allatomcount_rel=0
			totalside_rel=0
			mainchain_rel=0
			for j in binres5:
				#print (j)
				u=open("{}_atom.rsa".format(pdb_id_up)).readlines()
				v=open("{}_combined.rsa".format(pdb_id_up)).readlines()
				for k in u:
					k=k.rstrip()
					for l in v:
						l=l.rstrip()
						nn=k[4:7].strip()+k[9:13].strip()
						mm=l[4:7].strip()+l[9:13].strip()
						if nn==j.split("_")[0] and k[8]==j.split("_")[1] and mm==j.split("_")[0] and l[8]==j.split("_")[1] and k[0:3]=="RES" and l[0:3]=="RES":
							#print (nn,j.split("_")[0],k[8],j.split("_")[1],mm, j.split("_")[0],l[8],j.split("_")[1])
							asa=k[14:81].split()
							#print (asa)
							asa=[float(i) for i in asa]
							asaw_lig=l[14:81].split()
							asaw_lig=[float(i) for i in asaw_lig]
							#print(asaw_lig)
							allatoms=float(asa[0])-float(asaw_lig[0])
							allatoms_rel=float(asa[1])-float(asaw_lig[1])
							allatomcount+=allatoms
							allatomcount_rel+=allatoms_rel
							totside=float(asa[2])-float(asaw_lig[2])
							totside_rel=float(asa[3])-float(asaw_lig[3])
							totalside+=totside
							totalside_rel+=totside_rel
							mnchain=float(asa[4])-float(asaw_lig[4])
							mnchain_rel=float(asa[5])-float(asaw_lig[5])
							mainchain+=mnchain
							mainchain_rel+=mnchain_rel
			allatomcount_rel_35=0
			totalside_rel_35=0
			mainchain_rel_35=0
			for j in binres35:
				#print (j)
				u=open("{}_atom.rsa".format(pdb_id_up)).readlines()
				v=open("{}_combined.rsa".format(pdb_id_up)).readlines()
				for k in u:
					k=k.rstrip()
					for l in v:
						l=l.rstrip()
						nn=k[4:7].strip()+k[9:13].strip()
						mm=l[4:7].strip()+l[9:13].strip()
						if nn==j.split("_")[0] and k[8]==j.split("_")[1] and mm==j.split("_")[0] and l[8]==j.split("_")[1] and k[0:3]=="RES" and l[0:3]=="RES":
							#print (nn,j.split("_")[0],k[8],j.split("_")[1],mm, j.split("_")[0],l[8],j.split("_")[1])
							asa=k[14:81].split()
							#print (asa)
							asa=[float(i) for i in asa]
							asaw_lig=l[14:81].split()
							asaw_lig=[float(i) for i in asaw_lig]
							#print(asaw_lig)
							allatoms_rel_35=float(asa[1])-float(asaw_lig[1])
							allatomcount_rel_35+=allatoms_rel_35
							totside_rel_35=float(asa[3])-float(asaw_lig[3])
							totalside_rel_35+=totside_rel_35
							mnchain_rel_35=float(asa[5])-float(asaw_lig[5])
							mainchain_rel_35+=mnchain_rel_35

			predval= 0.10054837*(c_no)+0.22123107*(c_o_c)-0.28399224*(c_oo)-0.00769277*(copot4)+0.43737275*(energy_torsion_total)-0.5033322*(keyres_pci_5)+0.03146857*(totalside_rel_35)-0.03921815*(allatomcount_rel)+0.07307028*(c_oc)-2.7228043923750116
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.251")
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))


##########################################################################################                    Monosaccharide and Dimer              ##########################################################################################
##########################################################################################                    Monosaccharide and Dimer              ##########################################################################################
##########################################################################################                    Monosaccharide and Dimer              ##########################################################################################
##########################################################################################                    Monosaccharide and Dimer              ##########################################################################################


	if model=='mosacdi':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		elif method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("chmod -R 777 naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			chain=list(chain)
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')
				print ("Please wait. Result will load here when job is done.")
				print ("<br/>")
				#print ("Use the following link to obtain data when the job is done: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+protchain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+protchain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			#print (binres5)
			#print (binres35)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			chains_cons=''.join(chain)
			resultout.write(str(chains_cons))
			resultout.write("\n")
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

			aliphatic_count_5= len([x for x in binres5 if x[:3] in ["GLY","ALA","PRO","VAL","LEU","ILE","MET"]])
			#resultout.write(str(aliphatic_count_5))
			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			# print (len(file1))
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break
			sec_struct=[]
			total=[]
			backHbond=[]
			sideHbond=[]
			energy_VdW=[]
			electro=[]
			energy_SolvP=[]
			energy_SolvH=[]
			energy_vdwclash=[]
			entrop_sc=[]
			entrop_mc=[]
			energy_torsion=[]
			backbone_vdwclash=[]
			energy_dipole=[]
			water=[]
			disulfide=[]
			energy_kon=[]
			partcov=[]
			energyIonisation=[]
			Hetero_Backbone_HBond=[]
			entr_complex=[]
			Hetero_Sidechain_Hbond=[]
			Sidechain_Accessibility=[]
			Mainchain_Accessibility=[]
			Sidechain_Contact_Ratio=[]
			Mainchain_Contact_Ratio =[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				sec_struct.append(n[7])
				total.append(float(n[8]))
				backHbond.append(float(n[9]))
				electro.append(float(n[12]))
				energy_SolvP.append(float(n[13]))
				energy_torsion.append(float(n[21]))
				Sidechain_Accessibility.append(float(n[32]))
				num=[i for i in sec_struct if i in ['E','B','b','e']]
			energy_torsion_total=sum(energy_torsion)
			sec_struc_beta_count=len(num)
			#resultout.write(str(energy_torsion_total))
			allproatms=['O-', 'N+', 'C', 'O', 'N', 'S']
			allhetatms=['C', 'F', 'H', 'CL', 'O', 'N', 'P', 'S']
			allproatoms=[]
			allhetatoms=[]
			proatoms=[]
			ligatoms=[]
			contcombo=[]
			reses=[]
			lig=[]
			residues=[]
			ligands=[]

			dictnor={'C_C':[50.28,1.39,18.93,27.298,7.44,35.759], 'C_CL':[0.16,5.34,0.08,0.018,6.00,0.034], 'C_F':[0.19,8.02,0.03,0.013,5.43,0.018], \
			'C_H':[39.70,10.09,6.29,3.456,8.66,4.035], 'C_N':[4.70,1.99,1.44,1.828,7.62,2.365], 'C_O':[148.74,5.47,25.28,22.486,8.16,25.133], \
			'C_P':[0.23,0.38,0.11,0.530,8.76,0.538], 'C_S':[0.75,1.78,0.31,0.334,7.82,0.427], 'N_C':[15.55,1.90,4.10,5.376,6.49,7.115], \
			'N_CL':[0.00,0.00,0.00,0.004,6.50,0.008], 'N_F':[0.04,8.29,0.01,0.003,6.50,0.005], 'N_H':[5.11,5.76,0.57,0.758,8.42,0.894], \
			'N_N':[1.54,2.89,0.33,0.418,7.72,0.546], 'N_O':[57.88,9.44,6.90,5.663,9.10,6.395], 'N_P':[0.80,5.92,0.27,0.209,15.27,0.214], \
			'N_S':[0.00,0.00,0.00,0.074,7.64,0.095], 'N+_C':[5.12,3.30,1.12,1.530,9.71,1.466], 'N+_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'N+_F':[0.01,11.42,0.00,0.004,35.03,0.004], 'N+_H':[0.56,3.34,0.05,0.086,5.00,0.073], 'N+_N':[0.18,1.73,0.03,0.065,6.31,0.062],\
			'N+_O':[13.46,11.53,1.33,1.540,13.00,1.259], 'N+_P':[0.21,8.15,0.06,0.051,19.44,0.037], 'N+_S':[0.18,10.15,0.04,0.028,15.42,0.026],\
			'O_C':[56.37,6.05,14.40,6.075,6.43,8.405], 'O_CL':[0.00,0.00,0.00,0.001,1.55,0.002], 'O_F':[0.05,8.52,0.01,0.004,6.21,0.006], \
			'O_H':[7.13,7.04,0.77,0.812,7.90,1.001], 'O_N':[7.18,11.79,1.49,0.487,7.88,0.664], 'O_O':[45.56,6.51,5.25,6.095,8.59,7.195], \
			'O_P':[0.56,3.65,0.18,0.132,8.45,0.141], 'O_S':[0.21,1.89,0.06,0.055,5.01,0.074], 'O-_C':[17.36,10.92,2.63,2.030,12.60,1.587],\
			'O-_CL':[0.00,0.00,0.00,0.001,7.94,0.001], 'O-_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'O-_H':[1.67,9.69,0.11,0.232,13.24,0.162], \
			'O-_N':[0.84,8.09,0.10,0.107,10.19,0.083], 'O-_O':[14.15,11.85,0.97,1.740,14.38,1.161], 'O-_P':[0.04,1.66,0.01,0.009,3.44,0.006],\
			'O-_S':[0.14,7.73,0.02,0.011,5.85,0.008], 'S_C':[1.42,6.62,0.42,0.173,7.94,0.243], 'S_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'S_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'S_H':[0.04,1.90,0.01,0.007,3.12,0.009], 'S_N':[0.00,0.00,0.00,0.005,3.53,0.007], \
			'S_O':[1.02,6.36,0.14,0.124,7.62,0.149], 'S_P':[0.00,0.00,0.00,0.000,1.36,0.001], 'S_S':[0.00,0.00,0.00,0.001,2.31,0.001]}

			allproatoms35=[]
			allhetatoms35=[]
			proatoms35=[]
			ligatoms35=[]
			contcombo35=[]
			reses35=[]
			lig35=[]
			residues35=[]
			ligands35=[]
			copot1,copot2,copot3,copot4,copot5,copot6=0.0,0.0,0.0,0.0,0.0,0.0

			countatoms=0
			atom=[x.rstrip() for x in open("{}_atom.pdb".format(pdb_id_up)).readlines()]
			countatoms+=len(atom)
			allpa=["N+" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']]
			allpa.extend(["O-" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allpa.extend([x[76:78].strip() for x in atom if x[17:20].strip()+x[12:16].strip() not in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ','ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allproatoms.extend(allpa)
			hetatom=[x.rstrip() for x in open("{}_hetatom.pdb".format(pdb_id_up)).readlines()]
			allha=[x[76:78].strip() for x in hetatom]
			allhetatoms.extend(allha)
			for j in atom:
				AX1=float(j[30:38])
				AY1=float(j[38:46])
				AZ1=float(j[46:54])
				res=j[17:20]
				pos=j[22:26]
				atmname=j[12:16]
				if res.strip()+atmname.strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']:
					atm='N+'
				elif res.strip()+atmname.strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']:
					atm='O-'
				else:
					atm=j[76:78]
				#print atm
				for k in hetatom:
					HX1=float(k[30:38])
					HY1=float(k[38:46])
					HZ1=float(k[46:54])
					hetres=k[17:20]
					hetpos=k[22:26]
					hetatmname=k[12:16]
					hetatm=k[76:78]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						residues.append(res+pos)
						ligands.append(hetres+hetpos)
						proatoms.append(atm.strip())
						re=res.strip()+pos.strip()+atmname.strip()+" "+atm.strip()
						reses.append(re)
						li=hetres.strip()+hetpos.strip()+hetatmname.strip()+" "+hetatm.strip()
						lig.append(li)
						ligatoms.append(hetatm.strip())
						contcombo.append(atm.strip()+"-"+hetatm.strip())
					if round(distance,3)<3.5:
						y=atm.strip()+"_"+hetatm.strip()
						copot1+=dictnor[y][0]
						copot2+=dictnor[y][1]
						copot3+=dictnor[y][2]
						copot4+=dictnor[y][3]
						copot5+=dictnor[y][4]
						copot6+=dictnor[y][5]
			#resultout.write("\n")
			#resultout.write(str(copot3))
			#print ("<br/>")
			#print (copot3)
			p1=subprocess.Popen("/opt/websites/anaconda/bin/plipcmd -f {0}_combined.pdb -x > out_plip 2>&1".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p1.wait()
			f=open("report.xml").readlines()
			hbplip=[]
			for i in f:
				i=i.rstrip()
				if "<hydrogen_bond id=" in i:
					hbplip.append(i)



			hbplipl=len(hbplip)
			p4=subprocess.Popen("/opt/websites/anaconda/bin/babel -ipdb {0}_hetatom.pdb -osmi --append 'MW logP HBD' > out 2>&1".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			b=open("out").readlines()[0]
			#print (b.split()[0])
			y=str(b.split()[0])

			MW=b.split()[2]
			logP=b.split()[3]
			HBD=b.split()[4]
			y='\''+y+'\''
			#print ('<br/>')
			#print ("Smiles:",y)


			os.system("/opt/websites/anaconda/bin/python carb_features_new_rdkit.py {} > out_carb 2>&1".format(y))
			g=open("carb_features.txt").readlines()
			heavy_atoms=float(g[1].strip())


			os.system("/opt/websites/anaconda/bin/python3.7 descp.py {} > out_volume 2>&1".format(y))
			p5=subprocess.Popen("/opt/websites/anaconda/bin/python3.7 descp.py {} > out_volume 2>&1".format(y), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			g=open("volume_out.txt").readlines()[0]
			volume=float(g.strip())+40.0

			# #######################################               HBPLUS             ###################################################

			threeoneaa= {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
			     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
			     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
			     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
			oneletter=threeoneaa.keys()

			os.system("./hbplus {}_atom.pdb > hbplus_out.txt 2>&1".format(pdb_id_up))
			os.system("./hbplus {}.pdb > hbplus_out.txt 2>&1".format(pdb_id_up))

			h=open("{}.hb2".format(pdb_id_up)).readlines()[8:]
			donor=[]
			acceptor=[]
			for j in binres5:
			    res=j
			    j=j.split("_")
			    #print (j)
			    for k in h:
			        k=k.rstrip()
			        #print(k[0])
			        if k[0]==j[1] and k[:13].split()[0][-3:]+str(int(k[:13].split()[0][1:5]))+"_"+k[0]==res and k[:13].split()[0][-3:] in oneletter and k[14:27].split()[0][-3:] in oneletter:
			            donor.append(k)
			        if k[14]==j[1] and k[14:27].split()[0][-3:]+str(int(k[14:27].split()[0][1:5]))+"_"+k[14]==res and k[14:27].split()[0][-3:] in oneletter and k[:13].split()[0][-3:] in oneletter:
			            acceptor.append(k)
			merge=donor+acceptor
			hbond_donor=len(donor)
			######################################################        AutoDock calculations              ######################################################

			os.mkdir("autodock",0o777)
			adpath = os.path.join(path, "autodock")
			os.chdir(adpath)

			os.system("cp ../../clean_pdb.py clean_pdb.py")
			os.system("cp ../../prepare_dpf4.py prepare_dpf4.py")
			os.system("cp ../../prepare_gpf4.py prepare_gpf4.py")
			os.system("cp ../../prepare_ligand4.py prepare_ligand4.py")
			os.system("cp ../../prepare_receptor4.py prepare_receptor4.py")
			os.system("cp ../../autogrid4 autogrid4")
			os.system("cp ../../autodock4 autodock4")
			os.system("cp ../../pythonsh pythonsh")
			os.system("cp ../{0}_atom.pdb {0}_atom.pdb".format(pdb_id_up))
			os.system("cp ../{0}_hetatom.pdb {0}_hetatom.pdb".format(pdb_id_up))
			os.system("cp ../../ad_xyz_coords.py ad_xyz_coords.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}_atom.pdb".format(pdb_id_up))
			os.system("/usr/local/bin/python2.7 ad_xyz_coords.py {0}_atom.clean.pdb {0}_hetatom.pdb".format(pdb_id_up))

			with open("run.sh","w") as adfile:
				adfile.write("./pythonsh prepare_receptor4.py -r {}_atom.clean.pdb -A 'hydrogens'".format(pdb_id_up))
				adfile.write("\n")
				adfile.write("./pythonsh prepare_ligand4.py -l {}_hetatom.pdb -Z".format(pdb_id_up))
				adfile.write("\n")
				adfile.write("./pythonsh prepare_gpf4.py -l {0}_hetatom.pdbqt -r {0}_atom.clean.pdbqt -i {0}_atom.clean.pdb_conf.txt".format(pdb_id_up))
				adfile.write("\n")
				adfile.write("./pythonsh prepare_dpf4.py -l {0}_hetatom.pdbqt -r {0}_atom.clean.pdbqt".format(pdb_id_up))
				adfile.write("\n")
				adfile.write("./autogrid4 -p {0}_atom.clean.gpf -l {0}_hetatom.pdb.glg".format(pdb_id_up))
				adfile.write("\n")
				adfile.write("./autodock4 -p {0}_hetatom_{0}_atom.dpf -l {0}_atom_dock.dlg".format(pdb_id_up))
				adfile.write("\n")

			p5=subprocess.Popen("sh run.sh > ad_out 2>&1", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			while p5.poll() is None:
				time.sleep(5)
				print(" ")
				sys.stdout.flush()
			print(" ")


			try:
			    f=open("{}_atom_dock.dlg".format(pdb_id_up)).readlines()
			    advals=[]
			    for j in f:
			        j=j.rstrip()
			        if (j[0:4]=="USER"):
			            if "Estimated Free Energy of Binding" in j:
			                #print (j)
			                advals.append(j.split("=")[-2].split()[0].replace("+",""))
			            if "Final Intermolecular Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "vdW + Hbond + desolv Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "Electrostatic Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "Final Total Internal Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "Torsional Free Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "Unbound System's Energy" in j:
			                advals.append(j.split("=")[-1].split()[0].replace("+",""))
			            if "NEWDPF move	{}_ligand.pdbqt".format(i) in j:
			                #print (j)
			                break
			    adt_deltag=float(advals[0])
			    #print (pdb_id_up,advals)
			except FileNotFoundError:
			    print("Wrong file or file path")


			#print ("<br/>")
			#print ("Hydrogen bond count:", len(hbplip))
			#print ("<br/>")
			#print (copot3)
			#print ("<br/>")
			#print (energy_torsion_total)
			#print ("<br/>")
			#print (aliphatic_count_5)
			#print ("No of heavy atoms",heavy_atoms)
			#print ("<br/>")
			#print ("Donor",len(donor))
			#print ("<br/>")
			#print ("Acceptor",len(acceptor))
			#print ("<br/>")
			#print ("sec_struc_beta_count:",len(num))
			#print ("<br/>")
			#print ("ADT_DELG:",adt_deltag)
			os.chdir(path)

			predval= 0.513*(adt_deltag)+0.104*(hbond_donor)+0.562*(heavy_atoms)-0.174*(hbplipl)-0.008*(copot3)-0.599*(energy_torsion_total)+0.249*(sec_struc_beta_count) -0.050*(volume)+0.122*(aliphatic_count_5)-2.565
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.770")
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))



#####################################################################################                   Monosaccharide and Oligomer              #####################################################################################
#####################################################################################                   Monosaccharide and Oligomer              #####################################################################################
#####################################################################################                   Monosaccharide and Oligomer              #####################################################################################
#####################################################################################                   Monosaccharide and Oligomer              #####################################################################################


	if model=='mosacoli':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")
		if method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			chain=list(chain)
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')

				#print ("Use this url to obtain data: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+protchain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+protchain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			#print (binres5)
			#print (binres35)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			chains_cons=''.join(chain)
			resultout.write(str(chains_cons))
			resultout.write("\n")
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

			aromatic_count_35= len([x for x in binres35 if x[:3] in ['PHE','TYR','TRP','HIS']])
			#print ("aromatic_count_35:",aromatic_count_35)


			p4=subprocess.Popen("/opt/websites/anaconda/bin/babel -ipdb {0}_hetatom.pdb -osmi --append 'MW logP HBD' > out 2>&1".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			b=open("out").readlines()[0]
			#print (b.split()[0])
			y=str(b.split()[0])

			MW=float(b.split()[2])
			logP=b.split()[3]
			HBD=b.split()[4]
			y='\''+y+'\''
			#print ('<br/>')
			#print ("Smiles:",y)
			#print ('<br/>')			
			#print ('Molecular weight:',MW)
			os.system("/opt/websites/anaconda/bin/python3.7 carb_features_new_rdkit.py {} > out_carb 2>&1".format(y))
			g=open("carb_features.txt").readlines()
			rota_bonds=float(g[0])
			ohnh=float(g[2])
			#print ("<br/>")
			#print (rota_bonds)
			#print("<br/>")
			#print (ohnh)

			allproatms=['O-', 'N+', 'C', 'O', 'N', 'S']
			allhetatms=['C', 'F', 'H', 'CL', 'O', 'N', 'P', 'S']

			allproatoms=[]
			allhetatoms=[]
			proatoms=[]
			ligatoms=[]
			contcombo=[]
			reses=[]
			lig=[]
			residues=[]
			ligands=[]

			dictnor={'C_C':[50.28,1.39,18.93,27.298,7.44,35.759], 'C_CL':[0.16,5.34,0.08,0.018,6.00,0.034], 'C_F':[0.19,8.02,0.03,0.013,5.43,0.018], \
			'C_H':[39.70,10.09,6.29,3.456,8.66,4.035], 'C_N':[4.70,1.99,1.44,1.828,7.62,2.365], 'C_O':[148.74,5.47,25.28,22.486,8.16,25.133], \
			'C_P':[0.23,0.38,0.11,0.530,8.76,0.538], 'C_S':[0.75,1.78,0.31,0.334,7.82,0.427], 'N_C':[15.55,1.90,4.10,5.376,6.49,7.115], \
			'N_CL':[0.00,0.00,0.00,0.004,6.50,0.008], 'N_F':[0.04,8.29,0.01,0.003,6.50,0.005], 'N_H':[5.11,5.76,0.57,0.758,8.42,0.894], \
			'N_N':[1.54,2.89,0.33,0.418,7.72,0.546], 'N_O':[57.88,9.44,6.90,5.663,9.10,6.395], 'N_P':[0.80,5.92,0.27,0.209,15.27,0.214], \
			'N_S':[0.00,0.00,0.00,0.074,7.64,0.095], 'N+_C':[5.12,3.30,1.12,1.530,9.71,1.466], 'N+_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'N+_F':[0.01,11.42,0.00,0.004,35.03,0.004], 'N+_H':[0.56,3.34,0.05,0.086,5.00,0.073], 'N+_N':[0.18,1.73,0.03,0.065,6.31,0.062],\
			'N+_O':[13.46,11.53,1.33,1.540,13.00,1.259], 'N+_P':[0.21,8.15,0.06,0.051,19.44,0.037], 'N+_S':[0.18,10.15,0.04,0.028,15.42,0.026],\
			'O_C':[56.37,6.05,14.40,6.075,6.43,8.405], 'O_CL':[0.00,0.00,0.00,0.001,1.55,0.002], 'O_F':[0.05,8.52,0.01,0.004,6.21,0.006], \
			'O_H':[7.13,7.04,0.77,0.812,7.90,1.001], 'O_N':[7.18,11.79,1.49,0.487,7.88,0.664], 'O_O':[45.56,6.51,5.25,6.095,8.59,7.195], \
			'O_P':[0.56,3.65,0.18,0.132,8.45,0.141], 'O_S':[0.21,1.89,0.06,0.055,5.01,0.074], 'O-_C':[17.36,10.92,2.63,2.030,12.60,1.587],\
			'O-_CL':[0.00,0.00,0.00,0.001,7.94,0.001], 'O-_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'O-_H':[1.67,9.69,0.11,0.232,13.24,0.162], \
			'O-_N':[0.84,8.09,0.10,0.107,10.19,0.083], 'O-_O':[14.15,11.85,0.97,1.740,14.38,1.161], 'O-_P':[0.04,1.66,0.01,0.009,3.44,0.006],\
			'O-_S':[0.14,7.73,0.02,0.011,5.85,0.008], 'S_C':[1.42,6.62,0.42,0.173,7.94,0.243], 'S_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'S_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'S_H':[0.04,1.90,0.01,0.007,3.12,0.009], 'S_N':[0.00,0.00,0.00,0.005,3.53,0.007], \
			'S_O':[1.02,6.36,0.14,0.124,7.62,0.149], 'S_P':[0.00,0.00,0.00,0.000,1.36,0.001], 'S_S':[0.00,0.00,0.00,0.001,2.31,0.001]}

			allproatoms35=[]
			allhetatoms35=[]
			proatoms35=[]
			ligatoms35=[]
			contcombo35=[]
			reses35=[]
			lig35=[]
			residues35=[]
			ligands35=[]
			copot1,copot2,copot3,copot4,copot5,copot6=0.0,0.0,0.0,0.0,0.0,0.0

			countatoms=0
			atom=[x.rstrip() for x in open("{}_atom.pdb".format(pdb_id_up)).readlines()]
			countatoms+=len(atom)
			allpa=["N+" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']]
			allpa.extend(["O-" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allpa.extend([x[76:78].strip() for x in atom if x[17:20].strip()+x[12:16].strip() not in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ','ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allproatoms.extend(allpa)
			hetatom=[x.rstrip() for x in open("{}_hetatom.pdb".format(pdb_id_up)).readlines()]
			allha=[x[76:78].strip() for x in hetatom]
			allhetatoms.extend(allha)
			for j in atom:
				AX1=float(j[30:38])
				AY1=float(j[38:46])
				AZ1=float(j[46:54])
				res=j[17:20]
				pos=j[22:26]
				atmname=j[12:16]
				if res.strip()+atmname.strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']:
					atm='N+'
				elif res.strip()+atmname.strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']:
					atm='O-'
				else:
					atm=j[76:78]
				#print atm
				for k in hetatom:
					HX1=float(k[30:38])
					HY1=float(k[38:46])
					HZ1=float(k[46:54])
					hetres=k[17:20]
					hetpos=k[22:26]
					hetatmname=k[12:16]
					hetatm=k[76:78]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						residues.append(res+pos)
						ligands.append(hetres+hetpos)
						proatoms.append(atm.strip())
						re=res.strip()+pos.strip()+atmname.strip()+" "+atm.strip()
						#print re
						reses.append(re)
						li=hetres.strip()+hetpos.strip()+hetatmname.strip()+" "+hetatm.strip()
						lig.append(li)
						ligatoms.append(hetatm.strip())
						contcombo.append(atm.strip()+"-"+hetatm.strip())
					if round(distance,3)<3.5:
						# residues35.append(res+pos)
						# ligands35.append(hetres+hetpos)
						# proatoms35.append(atm.strip())
						# re35=res.strip()+pos.strip()+atmname.strip()+" "+atm.strip()
						# #print re
						# reses35.append(re35)
						# li35=hetres.strip()+hetpos.strip()+hetatmname.strip()+" "+hetatm.strip()
						# lig35.append(li35)
						# ligatoms35.append(hetatm.strip())
						# contcombo35.append(atm.strip()+"-"+hetatm.strip())
						y=atm.strip()+"_"+hetatm.strip()
							#print y,dictnor[y][0]
						copot1+=dictnor[y][0]
						copot2+=dictnor[y][1]
						copot3+=dictnor[y][2]
						copot4+=dictnor[y][3]
						copot5+=dictnor[y][4]
						copot6+=dictnor[y][5]
			selec_contact=['N-C']
			c_nc=contcombo.count('N'+"-"+'C')
			#print ("<br/>")
			#print (c_nc)

			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			# print (len(file1))
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break
			sec_struct=[]
			total=[]
			backHbond=[]
			sideHbond=[]
			energy_VdW=[]
			electro=[]
			energy_SolvP=[]
			energy_SolvH=[]
			energy_vdwclash=[]
			entrop_sc=[]
			entrop_mc=[]
			energy_torsion=[]
			backbone_vdwclash=[]
			energy_dipole=[]
			water=[]
			disulfide=[]
			energy_kon=[]
			partcov=[]
			energyIonisation=[]
			Hetero_Backbone_HBond=[]
			entr_complex=[]
			Hetero_Sidechain_Hbond=[]
			Sidechain_Accessibility=[]
			Mainchain_Accessibility=[]
			Sidechain_Contact_Ratio=[]
			Mainchain_Contact_Ratio =[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				backHbond.append(float(n[9]))
			#print ("<br/>")
			#print ("backHbond:",sum(backHbond))
			backhnond=sum(backHbond)
			p3=subprocess.Popen("./naccess {}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p3.wait()

			p4=subprocess.Popen("./naccess {}_combined.pdb -h".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			allatomcount=0
			totalside=0
			mainchain=0
			allatomcount_rel=0
			totalside_rel=0
			mainchain_rel=0
			for j in binres5:
				#print (j)
				u=open("{}_atom.rsa".format(pdb_id_up)).readlines()
				v=open("{}_combined.rsa".format(pdb_id_up)).readlines()
				for k in u:
					k=k.rstrip()
					for l in v:
						l=l.rstrip()
						nn=k[4:7].strip()+k[9:13].strip()
						mm=l[4:7].strip()+l[9:13].strip()
						if nn==j.split("_")[0] and k[8]==j.split("_")[1] and mm==j.split("_")[0] and l[8]==j.split("_")[1] and k[0:3]=="RES" and l[0:3]=="RES":
							#print (nn,j.split("_")[0],k[8],j.split("_")[1],mm, j.split("_")[0],l[8],j.split("_")[1])
							asa=k[14:81].split()
							#print (asa)
							asa=[float(i) for i in asa]
							asaw_lig=l[14:81].split()
							asaw_lig=[float(i) for i in asaw_lig]
							#print(asaw_lig)
							allatoms=float(asa[0])-float(asaw_lig[0])
							allatoms_rel=float(asa[1])-float(asaw_lig[1])
							allatomcount+=allatoms
							allatomcount_rel+=allatoms_rel
							totside=float(asa[2])-float(asaw_lig[2])
							totside_rel=float(asa[3])-float(asaw_lig[3])
							totalside+=totside
							totalside_rel+=totside_rel
							mnchain=float(asa[4])-float(asaw_lig[4])
							mnchain_rel=float(asa[5])-float(asaw_lig[5])
							mainchain+=mnchain
							mainchain_rel+=mnchain_rel
			# print (pdb_id_up,allatomcount,totalside,mainchain)
			# print (pdb_id_up,allatomcount_rel,totalside_rel,mainchain_rel)
			#print ("<br/>")
			#print ("absoulte_asa_difference:",totalside)
		## prop_direct_5 (values obtained from the file itself)
			occurence_5=[j[17:20].strip()+j[22:26].strip()+'_'+j[21] for j in atomrec]

			occurence_5_res=[x[:3] for x in set(occurence_5)]
			amino=['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
			resoccu=[occurence_5_res.count(u) for u in amino]

			occudict = dict(zip(amino, resoccu))

			binres5res=[x[:3] for x in binres5 if x in amino]
			# print (binres5res)
			kk=0
			for z in set(binres5res):
				val=(float(binres5res.count(z))/float(occudict[z]))/(float(len(binres5res))/float(sum(resoccu)))
				kk+=float(binres5res.count(z))*val
			prop_direct_5=kk
			#print ("<br/>")
			#print ("prop_direct_5:",prop_direct_5)


			predval= 0.762*(aromatic_count_35) -0.008*(MW) -0.065*(c_nc) +0.409*(rota_bonds) -0.024*(totalside) +0.556*(ohnh) -0.112*(prop_direct_5) -0.166*(backhnond)-3.077
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.517")
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))



##########################################################################################                    Disaccharide              ##########################################################################################
##########################################################################################                    Disaccharide              ##########################################################################################
##########################################################################################                    Disaccharide              ##########################################################################################
##########################################################################################                    Disaccharide              ##########################################################################################


	if model=='disacc':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")
		elif method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features_new_rdkit.py carb_features_new_rdkit.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			chain=list(chain)
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')

				#print ("Use this url to obtain data: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+protchain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+protchain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			#print (binres5)
			#print (binres35)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			chains_cons=''.join(chain)
			resultout.write(str(chains_cons))
			resultout.write("\n")
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

			binres5count=len(binres5)
			#print ("<br/>")
			#print (binres5count)
			#resultout.write("\n")
			#resultout.write(str(binres5count))

			threeoneaa= {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
			     'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
			     'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
			     'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
			oneletter=threeoneaa.keys()

			os.system("./hbplus {}_atom.pdb > hbplus_out.txt 2>&1".format(pdb_id_up))
			os.system("./hbplus {}.pdb > hbplus_out.txt 2>&1".format(pdb_id_up))

			h=open("{}.hb2".format(pdb_id_up)).readlines()[8:]
			donor=[]
			acceptor=[]
			for j in binres5:
			    res=j
			    j=j.split("_")
			    #print (j)
			    for k in h:
			        k=k.rstrip()
			        #print(k[0])
			        if k[0]==j[1] and k[:13].split()[0][-3:]+str(int(k[:13].split()[0][1:5]))+"_"+k[0]==res and k[:13].split()[0][-3:] in oneletter and k[14:27].split()[0][-3:] in oneletter:

			            donor.append(k)

			        if k[14]==j[1] and k[14:27].split()[0][-3:]+str(int(k[14:27].split()[0][1:5]))+"_"+k[14]==res and k[14:27].split()[0][-3:] in oneletter and k[:13].split()[0][-3:] in oneletter:

			            acceptor.append(k)
			merge=donor+acceptor
			hbond_acceptor=len(acceptor)
			#print ("<br/>")
			#print (hbond_acceptor)



			p4=subprocess.Popen("/opt/websites/anaconda/bin/babel -ipdb {0}_hetatom.pdb -osmi --append 'MW logP HBD' > out 2>&1".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			b=open("out").readlines()[0]
			#print (b.split()[0])
			y=str(b.split()[0])


			HBD=float(b.split()[4])
			y='\''+y+'\''
			#print ('<br/>')
			#print ("Smiles:",y)
			#print ('<br/>')
			#print ('Hydrogen Bond Donors:',HBD)

			os.system("/opt/websites/anaconda/bin/python carb_features_new_rdkit.py {} > out_carb 2>&1".format(y))
			g=open("carb_features.txt").readlines()
			fraction_sp3=float(g[3])
			#print ('<br/>')
			#print ("fraction_sp3:",fraction_sp3)
			rota_bonds=float(g[0])
			#print ("<br/>")
			#print (rota_bonds)

			allproatms=['O-', 'N+', 'C', 'O', 'N', 'S']
			allhetatms=['C', 'F', 'H', 'CL', 'O', 'N', 'P', 'S']

			allproatoms=[]
			allhetatoms=[]
			proatoms=[]
			ligatoms=[]
			contcombo=[]
			reses=[]
			lig=[]
			residues=[]
			ligands=[]

			dictnor={'C_C':[50.28,1.39,18.93,27.298,7.44,35.759], 'C_CL':[0.16,5.34,0.08,0.018,6.00,0.034], 'C_F':[0.19,8.02,0.03,0.013,5.43,0.018], \
			'C_H':[39.70,10.09,6.29,3.456,8.66,4.035], 'C_N':[4.70,1.99,1.44,1.828,7.62,2.365], 'C_O':[148.74,5.47,25.28,22.486,8.16,25.133], \
			'C_P':[0.23,0.38,0.11,0.530,8.76,0.538], 'C_S':[0.75,1.78,0.31,0.334,7.82,0.427], 'N_C':[15.55,1.90,4.10,5.376,6.49,7.115], \
			'N_CL':[0.00,0.00,0.00,0.004,6.50,0.008], 'N_F':[0.04,8.29,0.01,0.003,6.50,0.005], 'N_H':[5.11,5.76,0.57,0.758,8.42,0.894], \
			'N_N':[1.54,2.89,0.33,0.418,7.72,0.546], 'N_O':[57.88,9.44,6.90,5.663,9.10,6.395], 'N_P':[0.80,5.92,0.27,0.209,15.27,0.214], \
			'N_S':[0.00,0.00,0.00,0.074,7.64,0.095], 'N+_C':[5.12,3.30,1.12,1.530,9.71,1.466], 'N+_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'N+_F':[0.01,11.42,0.00,0.004,35.03,0.004], 'N+_H':[0.56,3.34,0.05,0.086,5.00,0.073], 'N+_N':[0.18,1.73,0.03,0.065,6.31,0.062],\
			'N+_O':[13.46,11.53,1.33,1.540,13.00,1.259], 'N+_P':[0.21,8.15,0.06,0.051,19.44,0.037], 'N+_S':[0.18,10.15,0.04,0.028,15.42,0.026],\
			'O_C':[56.37,6.05,14.40,6.075,6.43,8.405], 'O_CL':[0.00,0.00,0.00,0.001,1.55,0.002], 'O_F':[0.05,8.52,0.01,0.004,6.21,0.006], \
			'O_H':[7.13,7.04,0.77,0.812,7.90,1.001], 'O_N':[7.18,11.79,1.49,0.487,7.88,0.664], 'O_O':[45.56,6.51,5.25,6.095,8.59,7.195], \
			'O_P':[0.56,3.65,0.18,0.132,8.45,0.141], 'O_S':[0.21,1.89,0.06,0.055,5.01,0.074], 'O-_C':[17.36,10.92,2.63,2.030,12.60,1.587],\
			'O-_CL':[0.00,0.00,0.00,0.001,7.94,0.001], 'O-_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'O-_H':[1.67,9.69,0.11,0.232,13.24,0.162], \
			'O-_N':[0.84,8.09,0.10,0.107,10.19,0.083], 'O-_O':[14.15,11.85,0.97,1.740,14.38,1.161], 'O-_P':[0.04,1.66,0.01,0.009,3.44,0.006],\
			'O-_S':[0.14,7.73,0.02,0.011,5.85,0.008], 'S_C':[1.42,6.62,0.42,0.173,7.94,0.243], 'S_CL':[0.00,0.00,0.00,0.000,0.00,0.000], \
			'S_F':[0.00,0.00,0.00,0.000,0.00,0.000], 'S_H':[0.04,1.90,0.01,0.007,3.12,0.009], 'S_N':[0.00,0.00,0.00,0.005,3.53,0.007], \
			'S_O':[1.02,6.36,0.14,0.124,7.62,0.149], 'S_P':[0.00,0.00,0.00,0.000,1.36,0.001], 'S_S':[0.00,0.00,0.00,0.001,2.31,0.001]}

			allproatoms35=[]
			allhetatoms35=[]
			proatoms35=[]
			ligatoms35=[]
			contcombo35=[]
			reses35=[]
			lig35=[]
			residues35=[]
			ligands35=[]
			copot1,copot2,copot3,copot4,copot5,copot6=0.0,0.0,0.0,0.0,0.0,0.0

			countatoms=0
			atom=[x.rstrip() for x in open("{}_atom.pdb".format(pdb_id_up)).readlines()]
			countatoms+=len(atom)
			allpa=["N+" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']]
			allpa.extend(["O-" for x in atom if x[17:20].strip()+x[12:16].strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allpa.extend([x[76:78].strip() for x in atom if x[17:20].strip()+x[12:16].strip() not in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ','ASPOD1','ASPOD2','GLUOE1','GLUOE2']])
			allproatoms.extend(allpa)
			hetatom=[x.rstrip() for x in open("{}_hetatom.pdb".format(pdb_id_up)).readlines()]
			allha=[x[76:78].strip() for x in hetatom]
			allhetatoms.extend(allha)
			for j in atom:
				AX1=float(j[30:38])
				AY1=float(j[38:46])
				AZ1=float(j[46:54])
				res=j[17:20]
				pos=j[22:26]
				atmname=j[12:16]
				if res.strip()+atmname.strip() in ['ARGNH1','ARGNH2','ARGNE','HISND1','HISNE2','LYSNZ']:
					atm='N+'
				elif res.strip()+atmname.strip() in ['ASPOD1','ASPOD2','GLUOE1','GLUOE2']:
					atm='O-'
				else:
					atm=j[76:78]
				#print atm
				for k in hetatom:
					HX1=float(k[30:38])
					HY1=float(k[38:46])
					HZ1=float(k[46:54])
					hetres=k[17:20]
					hetpos=k[22:26]
					hetatmname=k[12:16]
					hetatm=k[76:78]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						residues.append(res+pos)
						ligands.append(hetres+hetpos)
						proatoms.append(atm.strip())
						re=res.strip()+pos.strip()+atmname.strip()+" "+atm.strip()
						#print re
						reses.append(re)
						li=hetres.strip()+hetpos.strip()+hetatmname.strip()+" "+hetatm.strip()
						lig.append(li)
						ligatoms.append(hetatm.strip())
						contcombo.append(atm.strip()+"-"+hetatm.strip())
					if round(distance,3)<3.5:
						y=atm.strip()+"_"+hetatm.strip()
						copot1+=dictnor[y][0]
						copot2+=dictnor[y][1]
						copot3+=dictnor[y][2]
						copot4+=dictnor[y][3]
						copot5+=dictnor[y][4]
						copot6+=dictnor[y][5]

			c_o_c=contcombo.count('O-'+"-"+'C')
			#print ("<br/>")
			#print (c_o_c)




			p3=subprocess.Popen("./naccess {}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p3.wait()
			p4=subprocess.Popen("./naccess {}_combined.pdb -h".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()
			allatomcount=0
			totalside=0
			mainchain=0
			allatomcount_rel=0
			totalside_rel=0
			mainchain_rel=0
			allatomcount_rel_35=0
			totalside_rel_35=0
			mainchain_rel_35=0
			for j in binres35:
				#print (j)
				u=open("{}_atom.rsa".format(pdb_id_up)).readlines()
				v=open("{}_combined.rsa".format(pdb_id_up)).readlines()
				for k in u:
					k=k.rstrip()
					for l in v:
						l=l.rstrip()
						nn=k[4:7].strip()+k[9:13].strip()
						mm=l[4:7].strip()+l[9:13].strip()
						if nn==j.split("_")[0] and k[8]==j.split("_")[1] and mm==j.split("_")[0] and l[8]==j.split("_")[1] and k[0:3]=="RES" and l[0:3]=="RES":
							#print (nn,j.split("_")[0],k[8],j.split("_")[1],mm, j.split("_")[0],l[8],j.split("_")[1])
							asa=k[14:81].split()
							#print (asa)
							asa=[float(i) for i in asa]
							asaw_lig=l[14:81].split()
							asaw_lig=[float(i) for i in asaw_lig]
							#print(asaw_lig)
							allatoms_rel_35=float(asa[1])-float(asaw_lig[1])
							allatomcount_rel_35+=allatoms_rel_35
							totside_rel_35=float(asa[3])-float(asaw_lig[3])
							totalside_rel_35+=totside_rel_35
							mnchain_rel_35=float(asa[5])-float(asaw_lig[5])
							mainchain_rel_35+=mnchain_rel_35
			# print (pdb_id_up,allatomcount_rel_35,totalside_rel_35,mainchain_rel_35)
			#print ("<br/>")
			#print ("rel_diff_asa_allatoms_35:",allatomcount_rel_35)





			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			# print (len(file1))
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break

			total=[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				total.append(float(n[8]))
			#print ("<br/>")
			#print ("total:",sum(total))

			aromatic_count_5= len([x for x in binres5 if x[:3] in ['PHE','TYR','TRP','HIS']])
			#print ("aromatic_count_5:",aromatic_count_5)



			predval= -0.379*(binres5count) +0.218*(hbond_acceptor) +2.726*(fraction_sp3) +0.380*(HBD) -0.029*(c_o_c) -0.192*(rota_bonds) +0.016*(allatomcount_rel_35) +0.091*sum(total) -0.144*(aromatic_count_5) -10.131
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.482")
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))






##########################################################################################                   Trisaccharide              ##########################################################################################
##########################################################################################                   Trisaccharide              ##########################################################################################
##########################################################################################                   Trisaccharide              ##########################################################################################
##########################################################################################                   Trisaccharide              ##########################################################################################


	if model=='trisacc':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("chmod -R 777 naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features.py carb_features.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")
		elif method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../naccess naccess")
			os.system("cp ../plipcmd plipcmd")
			os.system("cp ../3vvv.py 3vvv.py")
			os.system("cp ../carb_features.py carb_features.py")
			os.system("cp ../descp.py descp.py")
			os.system("cp ../hbplus hbplus")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			chain=list(chain)
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						sugar.split(",")
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')

				#print ("Use this url to obtain data: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			#print (binres5)
			#print (binres35)
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+protchain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+protchain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			#print (binres5)
			#print (binres35)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			chains_cons=''.join(chain)
			resultout.write(str(chains_cons))
			resultout.write("\n")
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			# print (len(file1))
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break
			energy_SolvP=[]
			Sidechain_Accessibility=[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				energy_SolvP.append(float(n[13]))
				Sidechain_Accessibility.append(float(n[32]))
			#print ("<br/>")
			#print ("energy_SolvP:",sum(energy_SolvP))
			#print ("<br/>")
			#print ("Sidechain_Accessibility:",sum(Sidechain_Accessibility))
			p4=subprocess.Popen("/opt/websites/anaconda/bin/babel -ipdb {0}_hetatom.pdb -osmi --append 'MW logP HBD' > out 2>&1".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()
			b=open("out").readlines()[0]
			#print (b.split()[0])
			y=str(b.split()[0])
			logP=float(b.split()[3])
			y='\''+y+'\''
			#print ('<br/>')
			#print ("Smiles:",y)
			#print ('<br/>')
			#print ('miLogP:',logP)



			p3=subprocess.Popen("./naccess {}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p3.wait()

			p4=subprocess.Popen("./naccess {}_combined.pdb -h".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p4.wait()

			allatomcount=0
			totalside=0
			mainchain=0
			allatomcount_rel=0
			totalside_rel=0
			mainchain_rel=0
			for j in binres5:
				#print (j)
				u=open("{}_atom.rsa".format(pdb_id_up)).readlines()
				v=open("{}_combined.rsa".format(pdb_id_up)).readlines()
				for k in u:
					k=k.rstrip()
					for l in v:
						l=l.rstrip()
						nn=k[4:7].strip()+k[9:13].strip()
						mm=l[4:7].strip()+l[9:13].strip()
						if nn==j.split("_")[0] and k[8]==j.split("_")[1] and mm==j.split("_")[0] and l[8]==j.split("_")[1] and k[0:3]=="RES" and l[0:3]=="RES":
							#print (nn,j.split("_")[0],k[8],j.split("_")[1],mm, j.split("_")[0],l[8],j.split("_")[1])
							asa=k[14:81].split()
							#print (asa)
							asa=[float(i) for i in asa]
							asaw_lig=l[14:81].split()
							asaw_lig=[float(i) for i in asaw_lig]
							#print(asaw_lig)
							allatoms=float(asa[0])-float(asaw_lig[0])
							allatoms_rel=float(asa[1])-float(asaw_lig[1])
							allatomcount+=allatoms
							allatomcount_rel+=allatoms_rel
							totside=float(asa[2])-float(asaw_lig[2])
							totside_rel=float(asa[3])-float(asaw_lig[3])
							totalside+=totside
							totalside_rel+=totside_rel
							mnchain=float(asa[4])-float(asaw_lig[4])
							mnchain_rel=float(asa[5])-float(asaw_lig[5])
							mainchain+=mnchain
							mainchain_rel+=mnchain_rel
			# print (pdb_id_up,allatomcount,totalside,mainchain)
			# print (pdb_id_up,allatomcount_rel,totalside_rel,mainchain_rel)

			#print ("relative_asa_difference:",allatomcount_rel)
			#print ("<br/>")
			#print ("relative_asa_difference_sidechain:",totalside_rel)


			predval= -0.615*sum(Sidechain_Accessibility)+0.167*sum(energy_SolvP)+1.436*(logP)-0.085*(allatomcount_rel)+0.056*(totalside_rel)+3.898
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.837")
			#print ("energy_SolvP:",sum(energy_SolvP))
			#print ("<br/>")
			#print ("Sidechain_Accessibility:",sum(Sidechain_Accessibility))
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))




#########################################################################################################    Polysaccharide      #####################################################################################################################
#########################################################################################################    Polysaccharide      #####################################################################################################################
#########################################################################################################    Polysaccharide      #####################################################################################################################
#########################################################################################################    Polysaccharide      #####################################################################################################################


	if model=='polysacc':
		if method==1:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			#os.system("chmod -R 777 {}".format(randname))
			os.chdir(path)
			os.system("wget 'https://files.rcsb.org/download/{}.pdb'".format(pdb_id_up))
			os.system("cp ../foldx foldx")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")
		elif method==2:
			dir_path = os.path.dirname(os.path.realpath(__file__))
			randname=uuid.uuid4().hex
			path = os.path.join(dir_path, randname)
			os.mkdir(path,0o777)
			os.chdir(path)
			os.system("mv ../tmp/{} input.pdb".format(fn))
			pdb_id_up='input'
			os.system("cp ../foldx foldx")
			os.system("cp ../style4.css style4.css")
			os.system("cp ../clean_pdb.py clean_pdb.py")
			os.system("/opt/websites/anaconda/bin/python3.7 clean_pdb.py {}.pdb".format(pdb_id_up))
			os.system("cp ../index.txt index.txt")
			os.system("cp ../footer.txt footer.txt")

		with open("result.txt","w") as resultout:
			f=open("{}.clean.pdb".format(pdb_id_up)).readlines()
			atomrec=[]
			hetatmrec=[]
			for i in f:
				i=i.rstrip()
				if i[0:4]=='ATOM' and i[21] in chain:
					atomrec.append(i)
				elif i[0:6]=='HETATM' and i[21] in lchain and i[17:20].strip() not in ions_list:
					if sugar=='':
						hetatmrec.append(i)
					elif sugar!='':
						if i[17:20].strip() in sugar:
							hetatmrec.append(i)
			with open("{}_atom.pdb".format(pdb_id_up),'w') as rec:
				for k in atomrec:
					rec.write(k)
					rec.write("\n")
			with open("{}_hetatom.pdb".format(pdb_id_up),'w') as hrec:
				for k in hetatmrec:
					if k[21] in lchain:
						hrec.write(k)
						hrec.write("\n")
			hetfile=open("{}_hetatom.pdb".format(pdb_id_up)).readlines()
			if len(hetfile)==0:
				print ('Content-Type: text/html\r\n')
				print (" ")
				print ('')
				print ('<html>')
				print ('  <head>')
				print ("No ligand found in interaction")
				os.chdir(dir_path)
				shutil.rmtree('{}'.format(randname))
				print ('</body>')
				print ('</html>')
				exit()
			else:
				redirectURL = "/bioinfo2/cgi-bin/pcapred/%s/result.py" % randname
				print ('Content-Type: text/html\r\n')
				print ('<html>')
				print ('  <head>')
				print ('    <meta http-equiv="refresh" content="0;url=%s" />' % redirectURL)
				print ('    <title>You are going to be redirected</title>')

				#print ("Use this url to obtain data: <a href='{}'>Result_page</a>".format(redirectURL))
			combinedpdb=atomrec + hetatmrec
			with open("{}_combined.pdb".format(pdb_id_up),'w') as crec:
				for k in combinedpdb:
					crec.write(k)
					crec.write("\n")
			binres35=[]
			binres5=[]
			binlig5=[]
			for u in hetatmrec:
				u=u.rstrip()
				HX1=float(u[30:38])
				HY1=float(u[38:46])
				HZ1=float(u[46:54])
				hetatm=u[77]
				hetatmname=u[13:16]
				hetres=u[17:20]
				hetposition=u[22:26]
				hetchain=u[21]
				for v in atomrec:
					v=v.rstrip()
					AX1=float(v[30:38])
					AY1=float(v[38:46])
					AZ1=float(v[46:54])
					atom=v[77]
					atomname=v[13:16]
					resname=v[17:20]
					position=v[22:26]
					protchain=v[21]
					distance=math.sqrt((HX1-AX1)**2+(HY1-AY1)**2+(HZ1-AZ1)**2)
					if round(distance,3)<5:
						binres5.append(resname.strip()+str(position).strip()+"_"+chain)
						binlig5.append(hetres.strip())
					if round(distance,3)<3.5:
						binres35.append(resname.strip()+str(position).strip()+"_"+chain)

			binres35=sorted(set(binres35),key=lambda x:int(x.split("_")[0][3:]))
			binres5=sorted(set(binres5),key=lambda x:int(x.split("_")[0][3:]))
			binlig5=set(binlig5)
			if pdb_id_up=='input':
				resultout.write("User input")
			else:
				resultout.write(pdb_id_up)
			resultout.write("\n")
			#print (chain)
			resultout.write(str(chain))
			resultout.write("\n")
			#print (binlig5)
			binlig5=",".join(binlig5)
			resultout.write(str(binlig5))

			resultout.write("\n")
			lchains_cons=''.join(lchain)
			resultout.write(str(lchains_cons))

		# # #######################################               FoldX             ###################################################

			p2=subprocess.Popen("./foldx --command=SequenceDetail --pdb={}_atom.pdb".format(pdb_id_up), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			p2.wait()
			file1=open("SD_{}_atom.fxout".format(pdb_id_up)).readlines()[:-1]
			# print (len(file1))
			with open("{}.csv".format(pdb_id_up),'w') as file:
				for r in binres5:
					r=r.split("_")
					for k in file1:
					 	k.rstrip()
					 	lines=k
					 	k=k.replace("H1S","HIS")
					 	k=k.replace("H2S","HIS")
					 	k=k.replace("H3S","HIS")
					 	k=k.split("\t")
					 	# print (r[1], k[2], r[0][:3], k[1],r[0][3:],k[3])
					 	if r[1]==k[2] and r[0][:3]==k[1] and r[0][3:]==k[3]:
					 		file.write(lines)
					 		break
			sec_struct=[]
			total=[]
			backHbond=[]
			sideHbond=[]
			energy_VdW=[]
			electro=[]
			energy_SolvP=[]
			energy_SolvH=[]
			energy_vdwclash=[]
			entrop_sc=[]
			entrop_mc=[]
			energy_torsion=[]
			backbone_vdwclash=[]
			energy_dipole=[]
			water=[]
			disulfide=[]
			energy_kon=[]
			partcov=[]
			energyIonisation=[]
			Hetero_Backbone_HBond=[]
			entr_complex=[]
			Hetero_Sidechain_Hbond=[]
			Sidechain_Accessibility=[]
			Mainchain_Accessibility=[]
			Sidechain_Contact_Ratio=[]
			Mainchain_Contact_Ratio =[]
			m=open("{}.csv".format(pdb_id_up)).readlines()
			for n in m:
				n=n.split("\t")
				sec_struct.append(n[7])
				total.append(float(n[8]))
				backHbond.append(float(n[9]))
				electro.append(float(n[12]))
				energy_SolvP.append(float(n[13]))
				energy_torsion.append(float(n[21]))
				Sidechain_Accessibility.append(float(n[32]))
				num=[i for i in sec_struct if i in ['E','B','b','e']]


		# ######################################################        volume              ######################################################
			threeoneaa= {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K','ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N','GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W','ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}
			oneletter=threeoneaa.keys()
			dict1={"A":91.5, "L":163.4, "R":196.1, "K":162.5, "N":138.3, "M":165.9, "D":135.2, "F":198.8, "C":114.4, 
			       "P":123.4, "Q":156.4, "S":102.0, "E":154.6, "T":126.0, "G":67.5, "W":209.8, "H":163.2, "Y":237.2, 
			       "I":162.6, "V":138.4}
			num=0
			i=i.rstrip().split("\t")                                    
			for j in binres5:
				if j[:3] in threeoneaa:
				    num+=dict1[threeoneaa[j[:3]]]

		# ######################################################        Residue Depth              ######################################################
			def Convertst(string): 
				list1=[] 
				list1[:0]=string 
				return list1  
			from Bio.PDB.ResidueDepth import ResidueDepth
			from Bio.PDB.PDBParser import PDBParser
			from Bio.PDB.ResidueDepth import get_surface
			from Bio.PDB.ResidueDepth import min_dist
			from Bio.PDB.ResidueDepth import residue_depth
			binres=binres5
			chains=[i.split("_")[1] for i in binres]
			for rs in chains:
				break
			res_dep=0
			print (rs)
			print (Convertst(rs))
			for j in Convertst(rs):
			    resnum=[int(i.split("_")[0][3:]) for i in binres if j==i.split("_")[1]]
			    parser = PDBParser()
			    structure = parser.get_structure("{0}", "{0}_atom.pdb".format(pdb_id_up))
			    model = structure[0]
			    rd = ResidueDepth(model)
			    surface = get_surface(model)
			    rschain = model["{}".format(j)]
			    resdepth=0
			    ax=[]
			    for a in resnum:
			        res = rschain[a]
			        rd = residue_depth(res, surface)
			        ax.append(rd)
			    res_dep+=sum(ax)
			predval= 0.20665088*res_dep-0.00410831*num-0.22996925*sum(electro)-0.00685319*sum(energy_SolvP)-4.093052692485966
			predval="%.2f" % predval
			resultout.write("\n")
			resultout.write(str(predval)+" ± 0.529")
			disass= '{:.3g}'.format(math.exp(float(predval)/(0.0019*298.15)))
			resultout.write("\n")
			resultout.write(str(disass))


########## common for all the classifications - start


timetaken=timeit.default_timer() - start

with open("result.py", "w") as polyout:
	polyout.write("""#!/opt/websites/anaconda/bin/python3.7\nimport cgi\nimport cgitb; cgitb.enable()\nprint ('Content-Type: text/html\\r\\n')\n""")
	g=open("index.txt").readlines()
	for gg in g:
		gg=gg.rstrip()
		polyout.write("""print (\"\"\"{}\"\"\")""".format(gg))
		polyout.write("\n")
	f=open("result.txt").readlines()
	# polyout.write ("print ('<center>Time taken for the calculation: {:.2f} seconds</center>')".format(timetaken))
	# polyout.write("\n")
	# polyout.write("print ('<br/>')")
	# polyout.write("\n")
	# polyout.write ("print ('<center>Model selected: {}</center>')".format(modeltype))
	# polyout.write("\n")
	# polyout.write("print ('<br/>')")
	# polyout.write("\n")


	polyout.write("""print ('<font face="Times New Roman" ><table id="customers">')""")
	polyout.write("\n")
	polyout.write("print ('<tr>')")
	polyout.write("\n")
	polyout.write("print ('<td><b>Time taken</b></td><td>{:.2f} seconds</td></td>')".format(timetaken))
	polyout.write("\n")
	polyout.write("print ('</tr>')")
	polyout.write("\n")
	polyout.write("print ('<tr>')")
	polyout.write("\n")
	polyout.write("print ('<td><b>Model selected</b></td><td>{}</td>')".format(modeltype))
	polyout.write("\n")
	polyout.write("print ('</tr>')")
	polyout.write("\n")
	polyout.write("print ('</table></font>')")
	polyout.write("\n")
	polyout.write("print ('<br/>')")
	polyout.write("\n")
	polyout.write("print ('<br/>')")
	polyout.write("\n")



	polyout.write("""print ('<font face="Times New Roman" ><table id="customers">')""")
	polyout.write("\n")
	polyout.write("print ('<tr>')")
	polyout.write("\n")
	polyout.write("print ('<td><b>PDB ID</b></td><td><b>Chain(s)</b></td><td><b>Ligand(s) </b></td><td><b>Ligand chain(s)</b></td><td><b>Predicted &Delta;G (kcal/mol)</b></td><td><b>K<sub>d</sub> (M)</b></td>')")
	polyout.write("\n")
	polyout.write("print ('</tr>')")
	polyout.write("\n")
	polyout.write("print ('<tr>')")
	polyout.write("\n")
	polyout.write("print ('<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>')".format(f[0].rstrip(),f[1].rstrip(),f[2].rstrip(),f[3].rstrip(),f[4].rstrip(),f[5].rstrip()))
	polyout.write("\n")
	polyout.write("print ('</tr>')")
	polyout.write("\n")
	polyout.write("print ('</table></font>')")
	polyout.write("\n")
	h=open("footer.txt").readlines()
	for hh in h:
		hh=hh.rstrip()
		polyout.write("""print (\"\"\"{}\"\"\")""".format(hh))
		polyout.write("\n")
os.system("chmod +x result.py")
os.system("ls > remfile")
remfile=open("remfile").readlines()
for rf in remfile:
	rf=rf.rstrip()
	if rf =='molecules':
		os.rmdir('{}'.format(rf))
	elif rf =='autodock':
		shutil.rmtree('autodock')
	elif rf not in ['result.txt','result.py']:
		os.remove('{}'.format(rf))

#print ('    Redirecting... <a href="%s">Click here if you are not redirected</a>' % redirectURL)
print ('</body>')
print ('</html>')

########## common for all the classifications - end
