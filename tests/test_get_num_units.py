import tensorflow as tf

from src.ai.utils import get_num_units


def test_correct_num_units():
    player_channel = tf.constant([[1001, 1002, 1003], [1004, 1005, 1006], [2004, 2005, 2006]], dtype=tf.int32)
    expected_units_player_1 = 6
    expected_units_player_2 = 3

    result_player_1 = get_num_units(player_channel, player_index=0)
    result_player_2 = get_num_units(player_channel, player_index=1)

    tf.debugging.assert_equal(result_player_1, expected_units_player_1, 'Player 1 should have 6 units')
    tf.debugging.assert_equal(result_player_2, expected_units_player_2, 'Player 2 should have 3 units')


def test_no_units():
    player_channel = tf.constant([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=tf.int32)
    player_index = 0
    expected_units = 0

    result = get_num_units(player_channel, player_index)

    tf.debugging.assert_equal(result, expected_units)


def test_no_array():
    player_channel = tf.constant([], dtype=tf.int32)
    player_index = 0
    expected_units = 0

    result = get_num_units(player_channel, player_index)

    tf.debugging.assert_equal(result, expected_units)

