# ncov-sequence-filter
An ML based approach to spotting possible recombinants.

Works best on sequences from North America and Europe


This project is still being tweaked for performance improvements. This is an initial release.


This project requires conda. Get it here:

https://anaconda.org/conda-forge/conda

To download the prerequisites run: `conda env create -f conda.yaml`

Drag your GISAID tar into ./data

Then run `snakemake --cores all`


The output will be a CSV that can be pasted into the GISAID search query
