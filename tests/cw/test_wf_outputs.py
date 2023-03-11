import json, os, sys, unittest, yaml
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import Mock, patch

from tests.cw.test_base import BaseWithDb
class CwWfOutputsTest(BaseWithDb):
    def _setUpClass(self):
        os.chdir(self.temp_d.name)
        self.destination = os.path.join(self.temp_d.name, "outputs")
        os.makedirs(self.destination, exist_ok=True)

        self.tasks_and_outputs = {"test.task1": ["file1"], "test.task2": ["file2", "file3"], "test.missing_task": ["?"]}
        self.tasks_and_outputs_fn = os.path.join(self.temp_d.name, "pipelines", "outputs.yaml")
        os.makedirs(os.path.dirname(self.tasks_and_outputs_fn))
        with open(self.tasks_and_outputs_fn, "w") as f:
            f.write(yaml.dump(self.tasks_and_outputs))

    def test_cli(self):
        runner = CliRunner()
        from cw.wf_outputs import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["gather", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["gather"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 2)

    def test_resolve_tasks_and_outputs(self):
        from cw import Pipeline
        from cw.wf_outputs import resolve_tasks_and_outputs as fun

        # pipeline
        pipeline = Pipeline.query.get(1)
        got = fun(pipeline, None)
        self.assertDictEqual(got, {"hw.run_hello_world": ["output_file"]})

        # file
        got = fun(pipeline, self.tasks_and_outputs_fn)
        self.assertDictEqual(got, self.tasks_and_outputs)

    def test_collect_shards_outputs(self):
        from cw.wf_outputs import collect_shards_outputs as fun

        task_name = "test.task2"
        task = [
            {
                "shardIndex": 0,
                "executionStatus": "Done",
                "outputs": {
                    "file2": "file2",
                    "file3": "file3",
                },
            },
            {
                "shardIndex": 0,
                "executionStatus": "Failed",
                "outputs": {
                    "file2": "file2",
                    "file3": "file3",
                },
            },
            {
                "shardIndex": 1,
                "executionStatus": "Done",
                "outputs": {
                    "file2": "file2",
                    "file3": "file3",
                },
            },
            {
                "shardIndex": 2,
                "executionStatus": "Failed",
                "outputs": {
                    "file2": "file2",
                    "file3": "file3",
                },
            },
        ]
        shards, shard_idxs = fun(task, self.tasks_and_outputs[task_name])
        self.assertEqual(shards, [[0, ["file2", "file3"]], [1, ["file2", "file3"]]])
        self.assertEqual(shard_idxs, set([0, 1, 2]))

    def test_copy_shards_outputs(self):
        from cw.wf_outputs import copy_shards_outputs as fun
        with open(os.devnull, 'w') as stdout:
            sys.stdout = stdout
            shards = [[0, ["file2", "file3"]], [1, ["file2", "file3"]]]
            task2_dn = os.path.join(self.destination, "task2")
            fun(shards, task2_dn)
            self.assertTrue(os.path.join(task2_dn))
            self.assertTrue(os.path.exists(os.path.join(task2_dn, "shard0")))
            self.assertTrue(os.path.exists(os.path.join(task2_dn, "shard1")))
        sys.stdout = sys.__stdout__

    def test_list_shards_outputs(self):
        from cw.wf_outputs import  list_shards_outputs as fun
        fn = os.path.join(self.temp_d.name, "stdout")
        with open(fn, "w") as f:
            sys.stdout = f
            shards = [[0, ["file2", "file3"]], [1, ["file2", "file3"]]]
            fun("generate_files", shards)
        sys.stdout = sys.__stdout__

        expected = """generate_files
 shard 0
  file2
  file3
 shard 1
  file2
  file3
"""
        with open(fn, "r") as f:
            self.assertEqual(f.read(), expected)

    @patch("cw.server.server_factory")
    def test_gather_cmd(self, factory_p):
        from cw.wf_outputs import gather_cmd as cmd
        runner = CliRunner()

        # create files
        # create metadata
        task1_shard0_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task1")
        task1_shard1_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task1")
        task2_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task2")
        for dn in task1_shard0_dn, task1_shard1_dn, task2_dn:
            os.makedirs(dn, exist_ok=True)
        task1_file1_1 = os.path.join(task1_shard0_dn, "file1-1")
        task1_file1_2 = os.path.join(task1_shard1_dn, "file1-2")
        task2_file2 = os.path.join(task2_dn, "file2")
        task2_file3 = os.path.join(task2_dn, "file3")
        for fn in task1_file1_1, task1_file1_2, task2_file2, task2_file3:
            Path(fn).touch()
        metadata = {
            "workflowName": "test",
            "calls": {
                "test.task1": [
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": task1_file1_1,
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 0,
                        "executionStatus": "Failed",
                        "outputs": {
                            "file1": "failed",
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 1,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": task1_file1_2,
                            "nocopy": "failed",
                        },
                    },
                    {
                        "shardIndex": 2,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": None,
                            "nocopy": "failed",
                        },
                    },
                ],
                "test.task2": [
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file2": task2_file2,
                            "file3": task2_file3,
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 0,
                        "executionStatus": "Failed",
                        "outputs": {
                            "file2": "failed",
                            "file3": "failed",
                            "nocopy": "nocopy",
                        },
                    },
                ],
                "test.task3": [ # ignored
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file": "ignored",
                        },
                    },
                ],
            }
        }
        server = Mock()
        server.configure_mock(**{"metadata_for_workflow.return_value": metadata})
        factory_p.return_value = server

        result = runner.invoke(cmd, ["1", self.destination, "-t", self.tasks_and_outputs_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected = f"""[INFO] Task <test.missing_task> files: <?>
[WARN] No task found for <test.missing_task> ... skipping
[INFO] Task <test.task1> files: <file1>
[INFO] Found 3 of 3 tasks DONE
[INFO] Copy {task1_file1_1} to {self.temp_d.name}/outputs/task1/shard0
[INFO] Copy {task1_file1_2} to {self.temp_d.name}/outputs/task1/shard1
[INFO] Task <test.task2> files: <file2 file3>
[INFO] Found 1 of 1 tasks DONE
[INFO] Copy {self.temp_d.name}/runs/test/UUID/call-task2/file2 to {self.temp_d.name}/outputs/task2
[INFO] Copy {self.temp_d.name}/runs/test/UUID/call-task2/file3 to {self.temp_d.name}/outputs/task2
[INFO] Done
"""
        self.maxDiff = 10000
        self.assertEqual(result.output, expected)

        got = []
        for (root, dirs, files) in os.walk(self.destination):
            for fn in files:
                got.append(os.path.join(root, fn))
        expected = ["task1/shard0/file1-1", "task1/shard1/file1-2", "task2/file2", "task2/file3"]
        expected = list(map(lambda f: os.path.join(self.destination, f), expected))
        self.assertEqual(got.sort(), expected.sort())

    @patch("cw.server.server_factory")
    def test_list_cmd(self, factory_p):
        from cw.wf_outputs import list_cmd as cmd
        runner = CliRunner()

        # create files
        # create metadata
        task1_shard0_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task1")
        task1_shard1_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task1")
        task2_dn = os.path.join(self.temp_d.name, "runs", "test", "UUID", "call-task2")
        for dn in task1_shard0_dn, task1_shard1_dn, task2_dn:
            os.makedirs(dn, exist_ok=True)
        task1_file1_1 = os.path.join(task1_shard0_dn, "file1-1")
        task1_file1_2 = os.path.join(task1_shard1_dn, "file1-2")
        task2_file2 = os.path.join(task2_dn, "file2")
        task2_file3 = os.path.join(task2_dn, "file3")
        for fn in task1_file1_1, task1_file1_2, task2_file2, task2_file3:
            Path(fn).touch()
        metadata = {
            "workflowName": "test",
            "calls": {
                "test.task1": [
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": task1_file1_1,
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 0,
                        "executionStatus": "Failed",
                        "outputs": {
                            "file1": "failed",
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 1,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": task1_file1_2,
                            "nocopy": "failed",
                        },
                    },
                    {
                        "shardIndex": 2,
                        "executionStatus": "Done",
                        "outputs": {
                            "file1": None,
                            "nocopy": "failed",
                        },
                    },
                ],
                "test.task2": [
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file2": task2_file2,
                            "file3": task2_file3,
                            "nocopy": "nocopy",
                        },
                    },
                    {
                        "shardIndex": 0,
                        "executionStatus": "Failed",
                        "outputs": {
                            "file2": "failed",
                            "file3": "failed",
                            "nocopy": "nocopy",
                        },
                    },
                ],
                "test.task3": [ # ignored
                    {
                        "shardIndex": 0,
                        "executionStatus": "Done",
                        "outputs": {
                            "file": "ignored",
                        },
                    },
                ],
            }
        }
        server = Mock()
        server.configure_mock(**{"metadata_for_workflow.return_value": metadata})
        factory_p.return_value = server

        result = runner.invoke(cmd, ["1", "-t", self.tasks_and_outputs_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected = f"""[INFO] Task <test.missing_task> files: <?>
[WARN] No task found for <test.missing_task> ... skipping
[INFO] Task <test.task1> files: <file1>
[INFO] Found 3 of 3 tasks DONE
[INFO] Listing files for test.task1
test.task1
 shard 0
  {self.temp_d.name}/runs/test/UUID/call-task1/file1-1
 shard 1
  {self.temp_d.name}/runs/test/UUID/call-task1/file1-2
 shard 2

[INFO] Task <test.task2> files: <file2 file3>
[INFO] Found 1 of 1 tasks DONE
[INFO] Listing files for test.task2
test.task2
 shard 0
  {self.temp_d.name}/runs/test/UUID/call-task2/file2
  {self.temp_d.name}/runs/test/UUID/call-task2/file3
"""
        self.maxDiff = 10000
        self.assertEqual(result.output, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
