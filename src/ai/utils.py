import tensorflow as tf


def get_num_units(player_channel, player_index):
    base_value = 1000 * (player_index + 1)
    unit_range = tf.range(base_value + 1, base_value + 1000, dtype=player_channel.dtype)
    player_units = tf.reduce_any(tf.equal(tf.expand_dims(player_channel, -1), unit_range), axis=-1)
    num_units = tf.reduce_sum(tf.cast(player_units, tf.int32))
    return num_units
