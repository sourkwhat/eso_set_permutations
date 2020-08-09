CHEST = 1
GLOVES = 2
BELT = 3
LEGS = 4
BOOTS = 5
NECKLACE = 6
RING = 7
DEST_STAFF = 8
ONE_HANDER = 9
SHIELD = 10
TWO_HANDER = 11
BOW = 12
RESTO_STAFF = 13


_SLOT_TRANSLATION = {
    CHEST: "Chest",
    GLOVES: "Gloves",
    BELT: "Belt",
    LEGS: "Legs",
    BOOTS: "Boots",
    NECKLACE: "Necklace",
    RING: "Ring",
    DEST_STAFF: "Destruction Staff",
    ONE_HANDER: "One-hander",
    SHIELD: "Shield",
    TWO_HANDER: "Two-hander",
    BOW: "Bow",
    RESTO_STAFF: "Restoration Staff",
}

_INVERSE_SLOT_TRANSLATION = {v: k for k, v in _SLOT_TRANSLATION.items()}

ARMOR_SLOTS = set([CHEST, GLOVES, BELT, LEGS, BOOTS, NECKLACE, RING])
WEAPON_SLOTS = set([DEST_STAFF, ONE_HANDER, SHIELD, TWO_HANDER, BOW, RESTO_STAFF])


class Slot:
    __slots__ = ["_value"]

    def __init__(self, value):
        self._value = value

    @property
    def human_readable(self):
        return _SLOT_TRANSLATION[self._value]

    @property
    def is_armor_slot(self):
        return self._value in ARMOR_SLOTS

    @property
    def is_weapon_slot(self):
        return self._value in WEAPON_SLOTS

    @classmethod
    def from_human_readable(cls, human_readable):
        return cls(_INVERSE_SLOT_TRANSLATION[human_readable])
