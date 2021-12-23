import click

@click.group(short_help="work with samples")
def samples_cli():
    """
    Samples!
    """
    pass

#from mgi.samples.create import samples_add_cmd, samples_create_cmd
#samples_cli.add_command(samples_add_cmd, name="add")
#samples_cli.add_command(samples_create_cmd, name="create")

#from mgi.samples.list import samples_list_cmd
#samples_cli.add_command(samples_list_cmd, name="list")

#from mgi.sample_features import sample_features_cli
#samples_cli.add_command(sample_features_cli, name="features")

#from mgi.samples.update import update_cmd
#samples_cli.add_command(update_cmd, name="update")
