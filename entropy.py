import numpy as np
from measure_circuit import get_random_basis_list, get_meas_output


def calculate_entropy(counts):
    total_shots = sum(counts.values())
    probabilities = [count / total_shots for count in counts.values()]

    # Calculate the Shannon entropy
    entropy = -sum(
        p * np.log2(p) if p > 0 else 0 for p in probabilities
    )  # Avoid log(0) by conditioning
    entropy /= np.log2(total_shots)  # Normalization
    return entropy


def get_average_entropy(circuit, runs, backend):
    avg_entropy = 0
    num_q = circuit.num_qubits

    # Measure given circuit
    basis_list = get_random_basis_list(runs, num_q)
    meas = get_meas_output(circuit, backend, basis_list)

    # Calculate entropy
    for i in range(0, len(meas)):
        avg_entropy += calculate_entropy(meas[i][1])

    avg_entropy /= runs
    return avg_entropy
