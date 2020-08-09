from __future__ import annotations

import click
import colorama
from dataclasses import dataclass
import logging
import os
from pathlib import Path

from eso_set_permutations import constants
from eso_set_permutations.config import Config
from eso_set_permutations.exceptions import NoConfigFileError
from eso_set_permutations.log import init_cli_logger
from eso_set_permutations.solver import solve_compatible_gear_sets

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


@click.group()
def cli_entry():
    init_cli_logger()
    print(colorama.Fore.GREEN)
    print("Hello!")
    print(colorama.Style.RESET_ALL)


@cli_entry.group()
def gear():
    pass


@gear.command()
def compatible():
    print(colorama.Fore.GREEN)
    print(
        "We are going to find all possible combinations of sets you can wear such that both sets give a five piece bonus."
    )
    print("Let's get busy with it.")
    config = Config.from_default()
    solve_compatible_gear_sets(config.gear_sets, config.desired_weapons)
    print(colorama.Style.RESET_ALL)


@cli_entry.group()
def config():
    pass


@config.command()
def open():
    if not Config.default_config_file_exists():
        logger.warning("Configuration file does not exist, creating a default one!")
        Config.write_default()

    os.system(f"notepad \"{constants.DEFAULT_CONFIG_PATH}\"")


@config.command()
def explorer():
    config_dir = Path(constants.DEFAULT_CONFIG_PATH).parent
    logger.info(f"Opening {config_dir} in explorer.")
    os.system("explorer \"{config_dir}\"")


if __name__ == "__main__":
    cli_entry()
