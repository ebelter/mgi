import os, unittest

from tests.cw.test_base import BaseWithDb
class DbTest(BaseWithDb):

    def test1_config(self):
        from cw import db, Config
        configs = Config.query.all()
        self.assertEqual(len(configs), 16)
        c = Config(name="status", group="server", value="running")
        db.session.add(c)
        db.session.commit()
        configs = Config.query.all()
        self.assertEqual(len(configs), 17)
        self.assertTrue(configs[0].name)
        self.assertTrue(configs[0].group)
        self.assertTrue(configs[0].value)

    def test2_pipeline(self):
        from cw import db, Pipeline
        pipelines = Pipeline.query.all()
        self.assertEqual(len(pipelines), 1)
        p = Pipeline(name="align", wdl="align.wdl", inputs="align.inputs.json", outputs="align.outputs.yaml", imports="align.imports.zip")
        db.session.add(p)
        db.session.commit()
        pipelines = Pipeline.query.all()
        self.assertEqual(len(pipelines), 2)
        p = pipelines[1]
        self.assertTrue(p.name)
        self.assertTrue(p.wdl)
        self.assertTrue(p.inputs)
        self.assertTrue(p.outputs)
        self.assertTrue(p.imports)
        self.assertEqual(len(p.workflows.all()), 0)

    def test3_workflow(self):
        from cw import db, Workflow
        wfs = Workflow.query.all()
        self.assertEqual(len(wfs), 1)
        wf = Workflow(wf_id="d10d2b6b-7f7e-4b20-a5dc-d4d0388e6d1a", name="SAMPLE", pipeline_id=0, inputs="IN", outputs="OUT")
        db.session.add(wf)
        db.session.commit()
        wfs = Workflow.query.all()
        self.assertEqual(len(wfs), 2)
        self.assertEqual(wfs[1].name, "SAMPLE")
        self.assertEqual(wfs[1].pipeline_id, 0)
        self.assertEqual(wfs[1].pipeline, None)
        self.assertEqual(wfs[1].inputs, "IN")
        self.assertEqual(wfs[1].outputs, "OUT")

if __name__ == '__main__':
    unittest.main(verbosity=2)
