from src.game.objects.Base import Base
from src.game.players.Player import Player
from src.game.units.InfantryUnit import InfantryUnit
from src.game.units.WorkerUnit import WorkerUnit


def test_add_unit():
    base = Base()
    player = Player(100, base)

    # Add first unit
    unit1 = WorkerUnit()
    player.add_unit(unit1)
    assert player.units == {1: unit1}

    # Add second unit
    unit2 = InfantryUnit()
    player.add_unit(unit2)
    assert player.units == {1: unit1, 2: unit2}

    # Add existing unit
    player.add_unit(unit1)
    assert player.units == {1: unit1, 2: unit2}


def test_remove_unit():
    base = Base()
    player = Player(100, base)

    unit1 = WorkerUnit()
    unit2 = WorkerUnit()
    unit3 = InfantryUnit()

    player.add_unit(unit1)
    player.add_unit(unit2)
    player.add_unit(unit3)

    # Remove existing unit
    player.remove_unit(unit2)
    assert player.units == {1: unit1, 3: unit3}

    # Remove non-existing unit
    player.remove_unit(object())
    assert player.units == {1: unit1, 3: unit3}

    # Remove all units
    player.remove_unit(unit1)
    player.remove_unit(unit3)
    assert player.units == {}


def test_get_base_position():
    base1 = Base()
    base1.set_position((2, 3))
    player1 = Player(100, base1)

    base2 = Base()
    base2.set_position((5, 7))
    player2 = Player(200, base2)

    assert player1.get_base_position() == (2, 3)
    assert player2.get_base_position() == (5, 7)


def test_get_player_by_unit():
    base1 = Base()
    base2 = Base()

    player1 = Player(100, base1)
    player2 = Player(200, base2)

    unit1 = WorkerUnit()
    unit2 = WorkerUnit()
    unit3 = InfantryUnit()

    player1.add_unit(unit1)
    player1.add_unit(unit2)
    player2.add_unit(unit3)

    # Test for existing unit
    assert player1.get_unit_index(unit1) == 1
    assert player1.get_unit_index(unit2) == 2
    assert player2.get_unit_index(unit3) == 1

    # Test for non-existing unit
    assert player1.get_unit_index(unit3) == 0
    assert player2.get_unit_index(unit1) == 0
    assert player2.get_unit_index(unit2) == 0

    player1.remove_unit(unit1)
    player2.remove_unit(unit3)

    # Check if unit 2 still has index 2
    assert player1.get_unit_index(unit1) == 0
    assert player1.get_unit_index(unit2) == 2
    assert player2.get_unit_index(unit3) == 0


def test_get_unit_index():
    base = Base()
    player = Player(100, base)

    unit1 = WorkerUnit()
    unit2 = WorkerUnit()
    unit3 = InfantryUnit()

    player.add_unit(unit1)
    player.add_unit(unit2)
    player.add_unit(unit3)

    assert player.get_unit_index(unit1) == 1
    assert player.get_unit_index(unit2) == 2
    assert player.get_unit_index(unit3) == 3
    assert player.get_unit_index(object()) == 0

    player.remove_unit(unit2)
    assert player.get_unit_index(unit1) == 1
    assert player.get_unit_index(unit2) == 0
    assert player.get_unit_index(unit3) == 3
