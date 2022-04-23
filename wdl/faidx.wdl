
struct RunEnv {
  String docker
  Int cpus = 1
  Int mem = 4
  Int disk = 20
}

workflow samtools {
      input {
        File fasta
        Boolean sizes = false
        String docker
        Int cpus = 1
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
            fasta=
            runenv=runenv
        }
    }
}

task faidx {
    input {
        File fasta
        String docker
        Int cpus
        Int mem
        Int disk
    }
    File idx = "~{fasta}.faidx"
    output {
        File idx = idx
    }
    runtime {
      docker: runenv.docker
      cpu: runenv.cpu
      memory: runenv.memory + " GB"
      disks : select_first([runenv.disks,"local-disk 100 SSD"])
      singularity: runtime_environment.singularity
    }
    command {
      samtools faidx ${fasta} -o ${idx}
    }
}
