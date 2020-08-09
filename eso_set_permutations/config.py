from pathlib import Path
import itertools
import logging

from eso_set_permutations import constants
from eso_set_permutations.exceptions import NoConfigFileError
from eso_set_permutations.slot import (
    Slot,
    CHEST,
    GLOVES,
    BELT,
    LEGS,
    BOOTS,
    NECKLACE,
    RING,
    DEST_STAFF,
    ONE_HANDER,
    SHIELD,
    TWO_HANDER,
    BOW,
    RESTO_STAFF,
)

import toml

logger = logging.getLogger(__name__)

GEAR_SETS = {
    "Yolnakhrin": [NECKLACE, CHEST, BELT, LEGS, DEST_STAFF, RING, BOOTS],
    "Imperium": [CHEST, GLOVES, BELT, LEGS, DEST_STAFF, NECKLACE, RING, SHIELD],
    "EternalYokeda": [BELT, DEST_STAFF, ONE_HANDER, RING, SHIELD],
    "Ebon": [CHEST, GLOVES, BELT, NECKLACE, RING, RING, BOOTS, ONE_HANDER],
    "Torug": [BELT, LEGS, DEST_STAFF, RING, SHIELD, ONE_HANDER],
}

DESIRED_WEAPONS = {"Front-bar": [ONE_HANDER, SHIELD], "Back-bar": [DEST_STAFF]}


class Config:
    def __init__(self, raw):
        self._gear_sets = {
            name: [Slot(value) for value in values] for name, values in raw.items()
        }

        self._desired_weapons = DESIRED_WEAPONS

    @property
    def gear_sets(self):
        return self._gear_sets

    @property
    def desired_weapons(self):
        #return set([slot for slot in itertools.chain(self.desired_weapons.values())])
        return set([ONE_HANDER, SHIELD, DEST_STAFF])

    @staticmethod
    def _to_human_readable_slots(slots):
        return [Slot(slot).human_readable for slot in slots]

    @classmethod
    def _to_human_readable_gear_sets(cls, gear_sets):
        return {
            name: cls._to_human_readable_slots(values)
            for name, values in gear_sets.items()
        }

    @staticmethod
    def _from_human_readable_gear_sets(gear_sets):
        return {
            name: [
                Slot.from_human_readable(human_readable)
                for human_readable in human_readables
            ]
            for name, human_readables in gear_sets.items()
        }

    @staticmethod
    def default_config_file_exists():
        return Path(constants.DEFAULT_CONFIG_PATH).exists()

    @classmethod
    def write_default(cls):
        logger.info("Writing a default configuration file.")
        with open(constants.DEFAULT_CONFIG_PATH, "w") as fh:
            fh.write(toml.dumps(cls._to_human_readable_gear_sets(GEAR_SETS)))
        logger.info("Done!")

    @classmethod
    def from_default(cls):
        if not cls.default_config_file_exists():
            logger.error(
                f"Default configuration file doesn't exist: {constants.DEFAULT_CONFIG_PATH}"
            )
            raise NoConfigFileError

        return cls(
            cls._from_human_readable_gear_sets(
                toml.load(constants.DEFAULT_CONFIG_PATH)
            )
        )
