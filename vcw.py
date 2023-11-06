from pathlib import Path

import click
import shutil
import subprocess
import yaml


def read_yaml_file(filepath):
    with open(filepath, "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """
    VCW is an automated tool for music playlist video creation
    """


@cli.command(
    "run",
    context_settings=dict(ignore_unknown_options=True),
    short_help="Run VCW",
)
@click.option(
    "--cores", "-c", default=1, help="Number of cores to use for Snakemake"
)
@click.option(
    "--dryrun",
    "-n",
    is_flag=True,
    help="Print Snakemake commands without executing them",
)
def run_workflow(cores, dryrun):
    """
    Run Snakemake workflow of choice
    """
    print(f"Starting workflow...")
    root_dir = Path(__file__).parent.absolute()
    config_path = root_dir / "workflow/configs/params.yaml"
    config = read_yaml_file(config_path)
    working_dir = config["working_dir"]
    if not dryrun:
        print("See Snakemake logs in: " f"{root_dir}/workflow/.snakemake/log")
        print(f"See detailed logs in: {working_dir}log")
    cmd = (
        "time snakemake -c {cores} "
        "--profile {profile} "
        "--directory {smk_dir} "
        "--snakefile {snakefile} "
        "--configfile {configfile} "
        "--config root_dir={root_dir}/ "
        "{dryrun}"
    ).format(
        cores=cores,
        profile=f"{root_dir}/workflow/configs",
        smk_dir=f"{root_dir}/workflow",
        snakefile=f"{root_dir}/workflow/Snakefile",
        configfile=f"{root_dir}/workflow/configs/params.yaml",
        root_dir=root_dir,
        dryrun="-n" if dryrun else "",
    )
    try:
        subprocess.run(
            cmd,
            shell=True,
            executable="/bin/bash",
            capture_output=False if dryrun else True,
        ).check_returncode()
    except Exception as e:
        print(f"\n{e}\n")
        print("ERROR: Failed to run workflow")
        print("See snakemake logs in: workflow/.snakemake/log")
        print(f"See detailed logs in: {working_dir}log")
    else:
        print("SUCCESS: Finished workflow")


@cli.command(
    "clean",
    context_settings=dict(ignore_unknown_options=True),
    help="Clean all redundant files",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Do not ask for confirmation",
)
def clean(yes):
    print(f"Cleaning...")
    root_dir = Path(__file__).parent.absolute()
    config_path = root_dir / "workflow/configs/params.yaml"
    config = read_yaml_file(config_path)
    working_dir = Path(config["working_dir"])

    paths_to_remove = [
        (working_dir / "log"),
        (working_dir / "benchmark"),
        (working_dir / "output"),
        (root_dir / "workflow" / ".snakemake" / "log"),
        (root_dir / "workflow" / ".snakemake" / "metadata"),
    ]

    if yes:
        for path in paths_to_remove:
            if path.exists():
                print("Removing:", path)
                shutil.rmtree(path)
    else:
        for path in paths_to_remove:
            ans = input(f"Remove {path}? [y/N] ")
            if ans in ["y", "Y"] and path.exists():
                print("Removing:", path)
                shutil.rmtree(path)
            else:
                print("Skipping:", path)


if __name__ == "__main__":
    cli()
