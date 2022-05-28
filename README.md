# NNSF
<img src="https://github.com/bitbyte2015/ncov-sequence-filter/raw/main/NNSF.png" width="30%" height="30%">

An experimental dense autoencoder that filters out SARS-CoV-2 sequences

Works best on sequences from Europe

## Requisites

This project requires conda. Get it here: https://anaconda.org/conda-forge/conda

To download the prerequisites run: `conda env create -f conda.yaml`

##### Note: the nextalign package is only available for Unix systems

Drag your GISAID tar into ./data

Then run `snakemake --cores all`

The output is data/pruned.fasta that can be run through https://nextclade.org or any other tool
