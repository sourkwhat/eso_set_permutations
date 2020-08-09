from dataclasses import dataclass
import io
import itertools
import logging


logger = logging.getLogger(__name__)


class PartialGearSetPermutation:
    def __init__(self, set_name, slot_permutation):
        self._set_name = set_name
        self._slot_permutation = sorted(slot_permutation)

    @property
    def set_name(self):
        return self._set_name

    @property
    def slot_permutation(self):
        return self._slot_permutation

    def __eq__(self, other):
        return (self.set_name == other.set_name) and (
            self.slot_permutation == other.slot_permutation
        )


@dataclass
class FullGearSetPermutation:
    weapon_set_permutation: PartialGearSetPermutation
    armor_set_permutation: PartialGearSetPermutation

    @property
    def weapon_set_name(self):
        return self.weapon_set_permutation.set_name

    @property
    def weapon_set_slots(self):
        return self.weapon_set_permutation.slot_permutation

    @property
    def armor_set_name(self):
        return self.armor_set_permutation.set_name

    @property
    def armor_set_slots(self):
        return self.armor_set_permutation.slot_permutation

    def __eq__(self, other):
        return (self.weapon_set_permutation == other.weapon_set_permutation) and (
            self.armor_set_permutation == other.armor_set_permutation
        )


class PartialGearSet:
    def __init__(self, set_name, slots, desired_weapon_slots=None):
        self._set_name = set_name
        self._slots = slots
        self._desired_weapon_slots = desired_weapon_slots or []

    @property
    def is_weapon_set(self):
        if not self._desired_weapon_slots:
            return False

        # this is not quite right.
        return set(self._desired_weapon_slots).issubset(set(self._slots))

    @property
    def set_name(self):
        return self._set_name

    @property
    def slots(self):
        return self._slots

    @property
    def available_weapon_slots(self):
        return [slot for slot in self.slots if slot in self.desired_weapon_slots]

    @property
    def armor_slots(self):
        return [slot for slot in self.slots if slot in ARMOR_SLOTS]

    @property
    def weapon_slots(self):
        return [slot for slot in self.slots if slot in WEAPON_SLOTS]

    def __eq__(self, other):
        return (sorted(self.slots) == sorted(other.slots)) and (
            self.set_name.lower() == other.set_name.lower()
        )

    def to_gear_name(self, slot):
        return f"{self._set_name} {GEAR_TRANSLATION[slot]}"

    def __str__(self):
        return "\n\t".join([self.to_gear_name(slot) for slot in self.slots])


class FullGearSet:
    def __init__(self, weapon_set, armor_set):
        self._weapon_set = weapon_set
        self._armor_set = armor_set
        self._double_set_bonus_permutations = None

    @property
    def weapon_set_name(self):
        return self._weapon_set.set_name

    @property
    def weapon_set_slots(self):
        return self._weapon_set.slots

    @property
    def armor_set_name(self):
        return self._armor_set.set_name

    @property
    def armor_set_slots(self):
        return self._armor_set.slots

    @property
    def double_set_bonus_permutations(self):
        if self._double_set_bonus_permutations is None:
            self._double_set_bonus_permutations = (
                self._solve_double_bonus_slot_permutations()
            )

        return self._double_set_bonus_permutations

    @property
    def double_set_bonus_permutations_as_string(self):
        output = io.StringIO()
        for full_gear_permutation in self.double_set_bonus_permutations:
            output.write(f"{full_gear_permutation.weapon_set_name}\n")
            output.write(str(full_gear_permutation.weapon_set_slots))
            output.write(f"\n{full_gear_permutation.armor_set_name}\n")
            output.write(str(full_gear_permutation.armor_set_slots))
            output.write("\n")
        return output.getvalue()

    def __eq__(self, other):
        return (self._weapon_set == other._weapon_set) and (
            self._armor_set == other._armor_set
        )

    def __str__(self):
        output = io.StringIO()
        output.write(
            f"Weapon Set: {self.weapon_set_name}, Armor Set: {self.armor_set_name}"
        )
        output.write("\n\t")
        output.write(str(self._weapon_set))
        output.write("\n\t")
        output.write(str(self._armor_set))
        return output.getvalue()

    @staticmethod
    def _valid_slots(gear_set1, gear_set2):
        required_rings = 2

        ring_count = gear_set1.count(RING)
        ring_count += gear_set2.count(RING)

        if ring_count != required_rings:
            logger.debug("Too many or too few rings!")
            return False

        return True

    def _solve_double_bonus_slot_permutations(self):
        logger.debug("Solving for double bonus permutations")

        double_bonus_permutations = []
        for weapon_set_armor_slots_permutation in itertools.permutations(
            self._weapon_set.armor_slots, 3
        ):
            for armor_set_armor_slots_permutation in itertools.permutations(
                self._armor_set.armor_slots, 5
            ):
                logger.debug(
                    f"Weapon set permutation: {_to_english(weapon_set_armor_slots_permutation)}"
                )
                logger.debug(
                    f"Armor set permutation: {_to_english(armor_set_armor_slots_permutation)}"
                )

                if not self._valid_slots(
                    weapon_set_armor_slots_permutation,
                    armor_set_armor_slots_permutation,
                ):
                    continue

                together = set(weapon_set_armor_slots_permutation).union(
                    set(armor_set_armor_slots_permutation)
                )

                if len(together) != 7:
                    logger.debug(
                        f"Combined gear does not work: {_to_english(together)} because {len(together)}"
                    )
                    continue

                full_gear_permutation = FullGearSetPermutation(
                    PartialGearSetPermutation(
                        self.weapon_set_name, weapon_set_armor_slots_permutation
                    ),
                    PartialGearSetPermutation(
                        self.armor_set_name, armor_set_armor_slots_permutation
                    ),
                )

                if full_gear_permutation not in double_bonus_permutations:
                    double_bonus_permutations.append(full_gear_permutation)

        return double_bonus_permutations
