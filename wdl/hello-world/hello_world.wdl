version 1.0

struct RuntimeEnvironment {
  String docker
  String memory
  String cpu
}

workflow hw {

    input {
        String name # the name to say hello to!
        String docker = "ebelter/mgi:cromwell"
    }

    RuntimeEnvironment runenv= {
      "docker": docker,
      "memory": "2",
      "cpu": "1"
    }

    call run_hello_world { input:
        name=name,
        runenv=runenv
    }
}

task run_hello_world {
    input {
        String name
        RuntimeEnvironment runenv
    }

    String output_file = "hello_world.txt"
    command {
        echo Hello ${name}! You have successfully run your first Cromwell pipeline with MGI CW CLI! | tee ${output_file}
    }

    output {
        File output_file = output_file
    }

    runtime {
      cpu: runenv.cpu
      memory: "${runenv.memory} GB"
      docker: runenv.docker
    }
}
