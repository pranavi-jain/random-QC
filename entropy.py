import numpy as np


def _calculate_entropy(counts):
    num_q = len(list(counts.keys())[0])
    total_shots = sum(counts.values())
    probabilities = [count / total_shots for count in counts.values()]

    # Calculate the Shannon entropy
    entropy = -sum(
        p * np.log2(p) if p > 0 else 0 for p in probabilities
    )  # Avoid log(0) by conditioning
    entropy /= num_q  # Normalization
    return entropy


def get_entropy_list(meas):
    """Return entropy for each of the measurement outcomes

    Args:
        meas: probability distribuitions of the measurements of the circuit

    Returns:
        dict: basis-entropy pair of the measurement outcomes
    """
    entropy_list = {}
    runs = len(meas)
    for i in range(0, runs):
        entropy = _calculate_entropy(meas[i][1])
        basis = meas[i][0]
        if basis in entropy_list:
            entropy_list[basis] += entropy
        else:
            entropy_list[basis] = entropy

    return entropy_list


def get_average_entropy(meas):
    """Return average entropy of the circuit, given the measurement outcomes

    Args:
        meas: probability distribuitions of the measurements of the circuit

    Returns:
        int: average entropy of the circuit over 'n' runs
    """
    avg_entropy = 0
    runs = len(meas)
    for i in range(0, runs):
        avg_entropy += _calculate_entropy(meas[i][1])

    avg_entropy /= runs
    return avg_entropy


def get_extreme_entropy_data(data, depth):
    """Utility function to fetch data with highest and lowest entropy for a given depth"""
    filtered_df = data[data["depth"] == depth]

    if filtered_df.empty:
        raise ValueError("No circuits found for this depth.")

    highest_entropy_data = filtered_df.loc[filtered_df["entropy"].idxmax()]
    lowest_entropy_data = filtered_df.loc[filtered_df["entropy"].idxmin()]
    return highest_entropy_data, lowest_entropy_data
