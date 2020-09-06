#!/usr/bin/environment python
import subprocess
import os
import sys

import yaml
from procgen_cli.utils.console import logger


def get_exp_cfg():
    if not os.path.exists("run.sh"):
        logger.error("Can't find `run.sh` in the current directory")
        sys.exit(1)
    ret = subprocess.run(
        'bash -c "source ./run.sh > /dev/null; echo \$EXPERIMENT"',
        shell=True,
        capture_output=True,
    )
    cfg_path = ret.stdout.decode().strip()
    if cfg_path == "" or not os.path.exists(cfg_path):
        logger.error("Can't determine the experiment YAML path :cry:")
        logger.normal(
            "Please set `EXPERIMENT_DEFAULT` or `EXPERIMENT` to point your experiment YAML file"
        )
        sys.exit(1)
    return cfg_path


def get_cfg_key(cfg, key):
    exp = list(cfg.keys())[0]
    res = cfg[exp].get("config").get(key)
    if res is None:
        logger.error(f"Please make sure that {exp}.config.{key} exists!")
        sys.exit(1)
    return res


def validate():
    exp_cfg_path = get_exp_cfg()
    with open(exp_cfg_path) as fp:
        cfg = yaml.safe_load(fp)
        workers = get_cfg_key(cfg, "num_workers")
        gpus = get_cfg_key(cfg, "num_gpus")
        gpus_per_worker = get_cfg_key(cfg, "num_gpus_per_worker")
        exp = list(cfg.keys())[0]
        eval_worker = not cfg.get(exp).get("disable_evaluation_worker", False)
        error = False
        if eval_worker:
            workers += 1
        if (workers + 1) > 8:
            logger.error(f"Please make sure that `num_workers + {1 + bool(eval_worker)} <= 8`")
            error = True
        if gpus + gpus_per_worker * workers > 1:
            logger.error(
                "Please make sure that `num_gpus + num_gpus_per_worker*(num_workers+1) <= 1"
            )
            error = True
        if error:
            if eval_worker:
                logger.normal("Alternatively, you can set `disable_evaluation_worker`")
                logger.normal(
                    "Refer: https://discourse.aicrowd.com/t/running-the-evaluation-worker-during-evaluations-is-now-optional/3520"
                )
            sys.exit(1)
    logger.success("All good with the experiment YAML! :tada:")
