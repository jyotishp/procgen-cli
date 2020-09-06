#!/usr/bin/environment python

import sys
import platform
from functools import partial
from urllib.request import urlopen
import subprocess
import os
from pathlib import Path
from procgen_cli.utils.console import logger

MINICONDA_BASE_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-"
MINICONDA_DOWNLOAD_PATH = "/tmp/miniconda.sh"


def get_os():
    return platform.system()


def get_download_link():
    os = get_os()
    if os == "Linux":
        logger.info("Detected Linux")
        return MINICONDA_BASE_URL + "Linux-x86_64.sh"
    if os == "Darwin":
        logger.info("Detected MacOS")
        return MINICONDA_BASE_URL + "MacOSX-x86_64.sh"
    logger.error("You are using an unsupported operating system")
    sys.exit(1)


def download(fpath="./miniconda.sh"):
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        TextColumn,
        TransferSpeedColumn,
        TimeRemainingColumn,
        Progress,
    )

    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    )
    with progress:
        url = get_download_link()
        task_id = progress.add_task("download", filename="Miniconda", start=False)
        response = urlopen(url)
        # This will break if the response doesn't contain content length
        progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(fpath, "wb") as dest_file:
            progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.update(task_id, advance=len(data))


def install():
    if not os.path.exists(MINICONDA_DOWNLOAD_PATH):
        download(MINICONDA_DOWNLOAD_PATH)
    os.chmod(MINICONDA_DOWNLOAD_PATH, 0o777)
    cmds = [
        f"bash {MINICONDA_DOWNLOAD_PATH} -b -p {Path.home()}/miniconda3",
        f". {Path.home()}/miniconda3/etc/profile.d/conda.sh",
        "conda init",
    ]
    ret = subprocess.run(" && ".join(cmds), shell=True)
    if ret.returncode != 0:
        logger.error(
            "Something went wrong while installing miniconda :cry: :broken_heart:"
        )
        logger.normal("Please try installing miniconda manually")
        logger.normal(
            "Instructions available at: https://docs.conda.io/en/latest/miniconda.html"
        )
        return
    logger.success("Installed Miniconda!")


def create_procgen_env():
    if os.path.exists(f"{Path.home()}/miniconda3/envs/procgen"):
        logger.info("Detected an existing conda env!")
        logger.normal(
            "If you this is a mistake, please run `procgen-cli env teardown` and then run `procgen-cli env setup`"
        )
        return
    setup_cmds = [f". {Path.home()}/miniconda3/etc/profile.d/conda.sh"]
    cmds = [
        "conda create -n procgen -y",
        "conda activate procgen",
        "conda install python=3.7 -y",
        "pip install ray[rllib]==0.8.6 procgen",
    ]
    execution_cmd = " && ".join(setup_cmds)
    if execution_cmd != "":
        execution_cmd += " && "
    execution_cmd += " && ".join(cmds)
    ret = subprocess.run(execution_cmd, shell=True)
    if ret.returncode != 0:
        remove_procgen_env()
        logger.error("Something went wrong! :cry: :broken_heart:")
        logger.normal("Please try running these commands manually")
        cmds = "```\n{}\n```".format("\n".join(cmds))
        logger.normal(cmds)
        return
    logger.success("The procgen environment is ready for use! :rocket:")
    logger.info("Please restart the shell to load the changes!")
    logger.normal("Please run `conda activate procgen` to activate the procgen env.")
    logger.normal("Please install TensorFlow/PyTorch as per your choice.")


def check():
    if os.path.exists(f"{Path.home()}/miniconda3"):
        return True
    if os.path.exists(f"{Path.home()}/anaconda3"):
        return True
    return False


def remove_procgen_env():
    setup_cmd = f". {Path.home()}/miniconda3/etc/profile.d/conda.sh"
    cmd = "conda env remove -n procgen"
    ret = subprocess.run(" && ".join([setup_cmd, cmd]), shell=True)
    if ret.returncode != 0:
        logger.error(
            "Something went wrong while removing the conda environment :cry: :broken_heart:"
        )
        return
    logger.success("Removed procgen environment")
