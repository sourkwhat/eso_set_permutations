import logging

from eso_set_permutations.gear_sets import PartialGearSet, FullGearSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def solve_compatible_gear_sets(raw_gear_sets, desired_weapon_slots):
    logger.debug("Solving for compatible gear sets.")

    weapon_sets = []
    armor_sets = []
    for name, slots in raw_gear_sets.items():
        gear_set = PartialGearSet(name, slots, desired_weapon_slots)
        armor_sets.append(gear_set)

        if gear_set.is_weapon_set:
            weapon_sets.append(gear_set)

    logger.debug("Sets that contain the desired weapons: ")
    for weapon_set in weapon_sets:
        logger.debug(f"\t{weapon_set.set_name}")

    compatible_full_gear_sets = []
    compatible_gear_set_permutations = []
    for weapon_set in weapon_sets:
        weapon_set_armor_slots = weapon_set.armor_slots

        for armor_set in armor_sets:

            if weapon_set.set_name == armor_set.set_name:
                continue

            full_gear_set = FullGearSet(weapon_set, armor_set)

            if full_gear_set.double_set_bonus_permutations:
                compatible_full_gear_sets.append(full_gear_set)

    for idx, compatible_full_gear_set in enumerate(compatible_full_gear_sets):
        print(compatible_full_gear_set)
        print(compatible_full_gear_set.double_set_bonus_permutations_as_string)

    return compatible_full_gear_sets
