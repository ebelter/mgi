version 1.0

struct RunEnv {
  String docker
  Int cpu
  Int memory
  String disks
}

workflow rna {
    meta {
        author: "Eddie Belter"
        version: "0.1"
        description: "ENCODE Bulk-RNA pipeline, see https://github.com/ENCODE-DCC/rna-seq-pipeline for details."
    }

    input {
        # only one docker for now
        String docker = "ebelter/mgi:rna-seq"

        # bamroot: root name for output bams. For example foo_bar will
        # create foo_bar_genome.bam and foo_bar_anno.bam
        String bamroot

        # endedness: paired or single
        # strandedness: is the library strand specific (stranded or unstranded)
        # strandedness_direction (forward, reverse, unstranded)
        String endedness
        String strandedness
        String strandedness_direction

        # fastqs_R1: fastq.gz files for Read1 (only these if single-ended)
        Array[Array[File]] fastqs_R1
        # fastqs_R2: fastq.gz files for Read2 (omit if single-ended) in order
        # corresponding to fastqs_R1
        Array[Array[File]] fastqs_R2 = []

        # Align
        # index: aligner index archive (tar.gz)
        File align_index
        Int align_cpu = 8
        Int align_memory = 48
        String? align_disks = "local-disk 100 HDD"

        # Bam to signals
        File chrom_sizes
        Int? bam_to_signals_cpu = 2
        Int bam_to_signals_memory = 8
        String? bam_to_signals_disks = "local-disk 100 HDD"
    }

    RunEnv runenv_default = {
      "docker": docker,
      "cpu": 1,
      "memory": 4,
      "disks": "local-disk 20 HDD",
    }
    RunEnv runenv_align = {
      "docker": docker,
      "cpu": align_cpu,
      "memory": align_memory,
      "disks": align_disks,
    }
    RunEnv runenv_bam_to_signals = {
      "docker": docker,
      "cpu": bam_to_signals_cpu,
      "memory": bam_to_signals_memory,
      "disks": bam_to_signals_disks,
    }

    # dummy variable value for the single-ended case
    Array[Array[File]] fastqs_R2_ = if (endedness == "single") then fastqs_R1 else fastqs_R2

    scatter (i in range(length(fastqs_R1))) {
        call align { input:
            endedness=endedness,
            fastqs_R1=fastqs_R1[i],
            fastqs_R2=fastqs_R2_[i],
            index=align_index,
            bamroot="rep"+(i+1)+bamroot,
            runenv=runenv_align,
        }

        call samtools_quickcheck as check_genome { input:
            bam=align.bam,
            runenv=runenv_default,
        }

        call bam_to_signals { input:
            input_bam=align.bam,
            chrom_sizes=chrom_sizes,
            strandedness=strandedness,
            bamroot="rep"+(i+1)+bamroot+"_genome",
            runenv=runenv_bam_to_signals,
        }
    }
}

task align {
    input {
        Array[File] fastqs_R1
        Array[File] fastqs_R2
        String endedness
        File index
        String bamroot
        RunEnv runenv
    }

    command {
        python3 $(which align.py) \
            --fastqs_R1 ~{sep=' ' fastqs_R1} \
            --fastqs_R2 ~{sep=' ' fastqs_R2} \
            --endedness ~{endedness} \
            --index ~{index} \
            ~{"--bamroot " + bamroot} \
            ~{"--ncpus " + runenv.cpu} \
            ~{"--ramGB " + runenv.memory}
    }

    output {
        File bam = "~{bamroot}_genome.bam"
        File flagstat = "~{bamroot}_genome_flagstat.txt"
        File log = "~{bamroot}_Log.final.out"
        File flagstat_json = "~{bamroot}_genome_flagstat.json"
        File log_json = "~{bamroot}_Log.final.json"
        File python_log = "align.log"
    }

    runtime {
      docker: runenv.docker
      cpu: runenv.cpu
      memory: "~{runenv.memory} GB"
      disks : runenv.disks
    }
}

task samtools_quickcheck {
    input {
        File bam
        RunEnv runenv
    }

    command {
        samtools quickcheck ~{bam}
    }

    runtime {
      docker: runenv.docker
      cpu: runenv.cpu
      memory: "~{runenv.memory} GB"
      disks : runenv.disks
    }
}

task bam_to_signals {
    input {
        File? null
        File input_bam
        File chrom_sizes
        String strandedness
        String bamroot
        RunEnv runenv
    }

    command {
        python3 $(which bam_to_signals.py) \
            --bamfile ~{input_bam} \
            --chrom_sizes ~{chrom_sizes} \
            --strandedness ~{strandedness} \
            --bamroot ~{bamroot}
    }

    output {
        File? unique_unstranded = if (strandedness == "unstranded") then glob("*_genome_uniq.bw")[0] else null
        File? all_unstranded = if (strandedness == "unstranded") then glob("*_genome_all.bw")[0] else null
        File? unique_plus = if (strandedness == "stranded") then glob("*_genome_plusUniq.bw")[0] else null
        File? unique_minus = if (strandedness == "stranded") then glob("*_genome_minusUniq.bw")[0] else null
        File? all_plus = if (strandedness == "stranded") then glob("*_genome_plusAll.bw")[0] else null
        File? all_minus = if (strandedness == "stranded") then glob("*_genome_minusAll.bw")[0] else null
        File python_log = "bam_to_signals.log"
    }

    runtime {
        docker: runenv.docker
        cpu: runenv.cpu
        memory: "~{runenv.memory} GB"
        disks : runenv.disks
    }
}
