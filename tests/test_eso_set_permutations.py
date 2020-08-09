from eso_set_permutations.eso_set_permutations import (
    CHEST,
    GLOVES,
    BELT,
    LEGS,
    BOOTS,
    NECKLACE,
    RING,
    STAFF,
    ONE_HANDER,
    SHIELD,
    solve_valid_gear_sets,
    _is_weapon_set,
    _valid_configuration,
    _remove_desired_weapons
)

# Both rings on the second set.
TEST_COMPATIBLE_SETS = {
    'Torug': [
        CHEST,
        GLOVES,
        BELT,
        LEGS,
        BOOTS
    ],
    'Yolnahkrin': [
        NECKLACE,
        RING,
        RING,
        STAFF,
        ONE_HANDER,
        SHIELD
    ]
}

# One ring on each set.
TEST_COMPATIBLE_SETS_ONE_RING = {
    'Torug': [
        CHEST,
        RING,
        BELT,
        LEGS,
        BOOTS
    ],
    'Yolnahkrin': [
        NECKLACE,
        GLOVES,
        RING,
        STAFF,
        ONE_HANDER,
        SHIELD
    ]
}

# Too many rings! 3 total.
TEST_INCOMPATIBLE_SETS = {
    'Torug': [
        CHEST,
        GLOVES,
        BELT,
        LEGS,
        RING
    ],
    'Yolnahkrin': [
        NECKLACE,
        RING,
        RING,
        STAFF,
        ONE_HANDER,
        SHIELD
    ]
}


def test_is_weapon_set():
    assert not _is_weapon_set(TEST_COMPATIBLE_SETS['Torug'])
    assert _is_weapon_set(TEST_COMPATIBLE_SETS['Yolnahkrin'])


def test_valid_configuration():
    assert _valid_configuration(TEST_COMPATIBLE_SETS['Torug'], TEST_COMPATIBLE_SETS['Yolnahkrin'])
    assert _valid_configuration(TEST_COMPATIBLE_SETS_ONE_RING['Torug'], TEST_COMPATIBLE_SETS_ONE_RING['Yolnahkrin'])
    assert not _valid_configuration(TEST_INCOMPATIBLE_SETS['Torug'], TEST_INCOMPATIBLE_SETS['Yolnahkrin'])


def test_remove_desired_weapons():
    assert _remove_desired_weapons(TEST_COMPATIBLE_SETS['Yolnahkrin']) == [NECKLACE, RING, RING]
    assert _remove_desired_weapons(TEST_COMPATIBLE_SETS['Torug']) == [CHEST, GLOVES, BELT, LEGS, BOOTS]


def test_successfully_find_compatible_sets():
    assert len(solve_valid_gear_sets(TEST_COMPATIBLE_SETS)) == 1