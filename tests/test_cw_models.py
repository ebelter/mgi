import os, unittest

from tests.test_cw_base import BaseWithDb
class DbTest(BaseWithDb):

    def test1_config(self):
        from cw import db, Config
        c = Config(name="status", group="server", value="running")
        db.session.add(c)
        db.session.commit()
        configs = Config.query.all()
        self.assertTrue(configs)
        self.assertEqual(len(configs), 13)
        self.assertTrue(configs[0].name)
        self.assertTrue(configs[0].group)
        self.assertTrue(configs[0].value)

    def test2_pipeline(self):
        from cw import db, Pipeline
        p = Pipeline(name="align", wdl="align.wdl", inputs="align.inputs.json", outputs="align.outputs.yaml", imports="align.imports.zip")
        db.session.add(p)
        db.session.commit()
        pipelines = Pipeline.query.all()
        self.assertTrue(pipelines)
        self.assertEqual(len(pipelines), 1)
        self.assertTrue(pipelines[0].name)
        self.assertTrue(pipelines[0].wdl)
        self.assertTrue(pipelines[0].inputs)
        self.assertTrue(pipelines[0].outputs)
        self.assertTrue(pipelines[0].imports)
        self.assertEqual(len(pipelines[0].workflows.all()), 0)

    def test3_workflow(self):
        from cw import db, Workflow
        wf = Workflow(wf_id="d10d2b6b-7f7e-4b20-a5dc-d4d0388e6d1a", name="SAMPLE", pipeline_id=0, inputs="IN", outputs="OUT")
        db.session.add(wf)
        db.session.commit()
        wfs = Workflow.query.all()
        self.assertTrue(wfs)
        self.assertEqual(len(wfs), 1)
        self.assertEqual(wfs[0].name, "SAMPLE")
        self.assertEqual(wfs[0].pipeline_id, 0)
        self.assertEqual(wfs[0].pipeline, None)
        self.assertEqual(wfs[0].inputs, "IN")
        self.assertEqual(wfs[0].outputs, "OUT")

if __name__ == '__main__':
    unittest.main(verbosity=2)
