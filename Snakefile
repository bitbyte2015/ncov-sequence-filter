rule build:
    input:
        "recombinants.csv"

def input_for_do_stuff(wildcards):
    try:
        return str(next(Path("data").glob("*.tar")))
    except StopIteration as err:
        raise Exception("No tar found") from err

rule unpack_gisaid_tar:
    input: input_for_do_stuff
    output:
        sequences = "data/gisaid.fasta",
        metadata = "data/metadata.tsv",
    shell:
        """
        tar -xvf {input} -C data/unpacked
        mv data/unpacked/*metadata.tsv {output.metadata}
        mv data/unpacked/*.fasta {output.sequences}
        """

rule nextalign:
    input:
        nextalign_dir = "nextalign",
        fasta = rules.unpack_gisaid_tar.output.sequences
    output:
        "data/aligned.fasta"
    shell:
        """
        nextalign --sequences={input.fasta} --reference={input.nextalign_dir}/reference.fasta --genemap={input.nextalign_dir}/genemap.gff --genes=E,M,N,ORF1a,ORF1b,ORF3a,ORF6,ORF7a,ORF7b,ORF8,ORF9b,S --output-dir=output --output-basename=nextalign
        mv output/nextalign.aligned.fasta {output}
        """

rule prediction:
    input:
        rules.nextalign.output
    output:
        "recombinants.csv"
    shell:
        "python predicter.py > {output}"