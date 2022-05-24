version 1.0

struct RunEnv {
  String docker
  Int cpu
  Int memory
  Int disks
}

workflow build_bwa_idx {
    meta {
        author: "Eddie Belter"
        version: "0.1"
        description: "Build BWA index from FASTA reference"
    }

    input {
        String name
        File fasta
        String docker = "ebelter/bwa:0.7.17"
        Int cpu = 4
        Int memory = 20
        Int disks = 20
    }

    RunEnv runenv = {
      "docker": docker,
      "cpu": cpu,
      "memory": memory,
      "disks": disks,
    }

    call bwa_idx { input:
        name=name
        fasta=fasta
        runenv=runenv
    }

    output {
        File idx_tgz = bwa_idx.idx_tgz
        File fai = bwa_idx.fai
        File gzi = bwa_idx.fai_gzi
        File chr_sizes = bwa_idxchr_sizes
    }
}

task bwa_idx {
    input {
        File fasta
        File fai
        String name
        RunEnv runenv
    }

    String fasta_bn = basename(fasta)
# GZIP Reference
#'docker(ebelter/linux-tk:latest)' tar czvvf /scratch1/fs1/ccdg/ebelter/hprc/idx/HG002.mat.tgz HG002.* 
#HG002.mat.fasta	  HG002.mat.fasta.ann  HG002.mat.fasta.chr-sz.tsv  HG002.mat.fasta.pac HG002.mat.fasta.amb  HG002.mat.fasta.bwt  HG002.mat.fasta.fai	   HG002.mat.fasta.sa
    command {
        samtools faidx ${fasta} --fai-idx ${fasta_bn + ".fai"} --gzi-idx ${fasta_bn + ".gzi"}
        cat ${fasta_bn + ".fai"} | awk '{print $1"\t"$2}' > ${fasta_bn + ".chr.tsv"}
        bwa index ${fasta}
        tar cvvfz ${name}.tgz ${fasta + ".*"}
    }

    output {
        File idx_tgz = "${name}.tgz"
        File fai = "${fasta_bn}.fai"
        File gzi = "${fasta_bn}.gzi"
        File chr_sizes = "${fasta_bn}.chr.tsv"
    }
}
