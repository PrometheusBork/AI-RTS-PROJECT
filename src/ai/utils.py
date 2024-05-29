import tensorflow as tf


def get_num_units(player_channel, player_index):
    """
    Calculates the number of units belonging to a specific player in a game.

    This function takes in a tensor representing a channel of player units and the index of a player,
    and it returns the number of units that the specified player has in that channel.

    Parameters:
    player_channel (tf.Tensor): A tensor representing the channel of player units.
    player_index (int): The index of the player whose units are being counted.

    Returns:
    tf.Tensor: A scalar tensor in tf.int32 representing the number of units the specified player has.
    """
    base_value = 1000 * (player_index + 1)
    unit_range = tf.range(base_value + 1, base_value + 1000, dtype=player_channel.dtype)
    player_units = tf.reduce_any(tf.equal(tf.expand_dims(player_channel, -1), unit_range), axis=-1)
    return tf.reduce_sum(tf.cast(player_units, tf.int32))


def extract_agent_actions(actions, agent_id):
    """
    Extracts the actions corresponding to a specific agent from the list of actions.

    Parameters:
    actions (list): A list of actions taken by all agents.
    agent_id (int): The ID of the agent whose actions are to be extracted.

    Returns:
    list: A list of actions corresponding to the specified agent.
    """
    return [action[agent_id] for action in actions]


def get_unit_actions(agent_actions):
    """
    Converts the actions to their values and calculates the maximum number of unit actions.

    Parameters:
    agent_actions (list): A list of actions taken by a specific agent.

    Returns:
    tuple:
        - list: A list of lists containing the unit actions' values.
        - int: The maximum number of unit actions in any of the action lists.
    """
    unit_actions = []
    max_units = 0
    for action in agent_actions:
        unit_actions_list = [act.value for act in action[:-1]]
        max_units = max(max_units, len(unit_actions_list))
        unit_actions.append(unit_actions_list)
    return unit_actions, max_units


def pad_unit_actions(unit_actions, max_units):
    """
    Pads the unit actions to ensure they all have the same length.

    Parameters:
    unit_actions (list): A list of lists containing the unit actions' values.
    max_units (int): The maximum number of unit actions in any of the action lists.

    Returns:
    list: A list of lists containing the padded unit actions.
    """
    padded_unit_actions = []
    for actions_list in unit_actions:
        padding_length = max_units - len(actions_list)
        padded_actions = actions_list + [-1] * padding_length
        padded_unit_actions.append(padded_actions)
    return padded_unit_actions


def create_unit_sequences(states, unit_action_space, agent_id):
    """
    Creates sequences of unit actions for a specified agent across different game states.

    This function processes a list of game states to create sequences representing the actions
    of units belonging to a specific agent. It also determines the maximum number of units
    across all states to ensure proper padding of the sequences.

    Parameters:
    states (list of tf.Tensor): A list of tensors representing different game states.
                                Each state tensor should have shape (height, width, channels),
                                where the second channel (index 1) contains unit IDs.
    unit_action_space (int): The number of possible actions each unit can take.
    agent_id (int): The index of the agent whose unit actions are being sequenced.

    Returns:
    tf.Tensor: A 3D tensor containing the padded unit action sequences for the specified agent
               across all states. The shape of the tensor is (num_states, max_units, unit_action_space).
    """
    unit_sequences = []
    max_units = 0

    for state in states:
        player_channel = state[:, :, 1]
        num_units = get_num_units(player_channel, agent_id)
        max_units = tf.maximum(max_units, num_units)
        unit_sequence = tf.zeros((num_units, unit_action_space), dtype=tf.float32)
        unit_sequences.append(unit_sequence)

    return pad_sequences(unit_sequences, max_units)


def pad_sequences(sequences, max_length):
    """
    Pads a list of sequences to ensure they all have the same length.

    This function uses TensorFlow's `pad_sequences` utility to pad sequences
    to the specified maximum length. Padding is added at the end ('post') of each sequence.

    Parameters:
    sequences (list of tf.Tensor): A list of 2D tensors representing the sequences to be padded.
    max_length (int): The length to which each sequence will be padded.

    Returns:
    tf.Tensor: A 3D tensor containing the padded sequences. The shape of the tensor is
               (num_sequences, max_length, sequence_width), where `sequence_width` is inferred
               from the input sequences.
    """
    return tf.keras.preprocessing.sequence.pad_sequences(
        sequences,
        maxlen=max_length,
        padding='post',
        dtype='float32'
    )
