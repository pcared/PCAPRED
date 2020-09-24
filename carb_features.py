import sys
import time
import rdkit
from pychem.pychem import Chem
from pychem import constitution
from pychem import pychem
from pychem.pychem import PyChem2d
i=sys.argv[1]
smi=i
mol=Chem.MolFromSmiles(smi)
#res=constitution.GetConstitutional(mol)
drug=pychem.PyChem2d()
drug.ReadMolFromSmile(smi)
vals=constitution.GetConstitutional(mol)


with open("carb_features.txt","w") as f:
#	print>> f, drug.GetMolProperty()
#	print>> f, constitution.GetConstitutional(mol)
	print>> f, vals['nrot']
	print>> f, mol.GetNumHeavyAtoms()
	print>> f, vals['ndonr']
#	print>> f, constitution.CalculateMolWeight(mol)
	print>> f, rdkit.Chem.rdMolDescriptors.CalcFractionCSP3(mol)
