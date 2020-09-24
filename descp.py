import sys
from padelpy import from_smiles
i=sys.argv[1]
smi=i
descriptors = from_smiles(smi,timeout=30)
vol=descriptors['McGowan_Volume']
with open("volume_out.txt","w") as f:
	f.write(str(float(vol)*100))
