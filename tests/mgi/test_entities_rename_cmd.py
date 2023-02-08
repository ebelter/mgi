import unittest
from click.testing import CliRunner

from tests.test_base_classes import TestBaseWithDb

class EntitiesRenameCmdTest(TestBaseWithDb):
    def _test(self, kind, cmd):
        from mgi.entity.helpers import add_entity, get_entity
        from mgi.models import db

        name = "Thor"
        new_name = "The Greatest Avenger"
        e = add_entity(name=name, kind=kind)
        self.assertTrue(e)
        db.session.add(e)
        db.session.flush()
        db.session.commit()

        runner = CliRunner()
        result = runner.invoke(cmd, [name, new_name], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Rename {kind} from {name} to {e.name}\n"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(e.name, new_name)

    def test_rename_cmd(self):
        from mgi.samples.cli import rename_cmd as cmd1
        from mgi.refs.cli import rename_cmd as cmd2
        cmds = (cmd1, cmd2)
        for i, kind in enumerate(["sample", "ref"]):
            self._test(kind, cmds[i])

# -- SamplesRenameCmdTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
