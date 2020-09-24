# PCAPRED
<h2>Protein-Carbohydrate complex binding Affinity PREDiction</h2>


<p>This program predicts protein-carbohydrate binding affinity using structure-based features and classes based on protein chains and saccharide count. Generally, binding site residues, accessible surface area, interactions between various atoms and their energy contributions are important to understand the binding affinity. PCA-Pred shows a correlation of 0.731 and a mean absolute error (MAE) of 1.149 kcal/mol in jack-knife test. In the test dataset, the performance remains consistent with a correlation of 0.723 with MAE of 1.158 kcal/mol. </p>



<b>Requirements:</b>
<b><p>Programs standalone:</p></b>
<ol>
  <li>Python version 2.7 and 3.7</li>
  <li>AutoDock 4.2</li>
  <li>HBPLUS</li>
  <li>Open Babel</li>
  <li>Protein-Ligand Interaction Profiler (plipcmd)</li>
  <li>FoldX</li>
  <li>NACCESS</li>
</ol>

<b><p>Python packages:<p></b>
  <ol>
<li>BioPython - Residue Depth</li>
    <li>RDKit</li>
    <li>PyChem</li>
    <li>PaDELPy</li>
    <li>Shutil</li>
    <li>Subprocess</li>
</ol>

    
<b><p>Supporting programs included here:</p></b>
<ol>
    <li>carb_features.py</li>
    <li>descp.py</li>
</ol>
<h3>CAUTION:</h3>
<p>This is an webserver file. You need to construct the webpage to pass the data to the program and the program has to be kept in the cgi-bin.</p> 

To use the prediction program, you need to install above mentioned packages and softwares. We are working on the standalone version and it will released in the future.

