version 1.0

struct RunEnv {
  String docker
  Int cpu
  Int memory
  #Int disks
}

workflow samtools {
    input {
        File fasta
        Boolean sizes = false
        String docker
        Int cpu = 1
        Int memory = 4
        #Int disks = 20
    }

    RunEnv runenv = {
      "docker": docker,
      "cpu": cpu,
      "memory": memory,
      #"disks": disks,
    }

    call faidx {
        input:
            fasta=fasta,
            runenv=runenv
    }

    output {
        File fai = faidx.fai
        File gzi = faidx.gzi
    }
}

task faidx {
    input {
        File fasta
        RunEnv runenv
    }

    String bn = basename(fasta)

    command {
        samtools faidx ${fasta} --fai-idx ${bn + ".fai"} --gzi-idx ${bn + ".gzi"}
    }

    output {
        File fai = "${bn}.fai"
				File gzi = "${bn}.gzi"
    }

    runtime {
        docker: runenv.docker
        cpu: runenv.cpu
        memory: runenv.memory + " GB"
        #disks : select_first([runenv.disks,"local-disk 100 SSD"])
    }
}
