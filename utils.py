from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.analysis import hellinger_fidelity


def get_fidelity_data(meas1, meas2, noisyMeas):
    """Utility function to get fidelities between
        - the circuit and itself, and
        - the circuit and the noisy circuit
        for a single measurement set performed in all 3 basis.

    Args:
        meas1: measurement output of random circuit
        meas2: a second measurement output of random circuit
        noisyMeas: measurement output of noisy circuit

    Returns:
        tuple: {{"C2C":fidelity of circuit},{"C2N":fidelity of circuit with noise}}
    """
    data = {}
    sumC = 0.0
    sumN = 0.0
    fidCC = []
    fidCN = []
    runs = len(meas1)

    for i in range(0, runs):
        sumC += hellinger_fidelity(meas1[i][1], meas2[i][1])
        fidCC.append(sumC)
        sumN += hellinger_fidelity(meas1[i][1], noisyMeas[i][1])
        fidCN.append(sumN)
    data.update({"C2C": fidCC})
    data.update({"C2N": fidCN})
    return data


def modify_circuit(qbits, gate, depth, circuit):
    """Utility function to generate new circuit with arbitary gate added at arbitary depth"

    Args:
        qbit (int): list of qubit numbers to which gate is added
        gate (standard_gate): arbitrary gate from standard_gates set of qiskit library
        depth (int): the depth at which gate is to be added, starts at 1
        circuit (qiskit.circuit.QuantumCircuit): existing circuit to be modified

    Returns:
        QuantumCircuit: modified circuit
    """
    newCirc = circuit.copy()
    numQ = circuit.num_qubits

    for q in qbits:
        if q > numQ:
            raise ValueError("Qubits mismatch for given ciruit.")

    insertCirc = QuantumCircuit(numQ)
    insertCirc.append(gate, qbits)
    ci_pos = 0
    qpos = 0
    lst = set(qbits)
    for inst, qargs, cargs in circuit.data:
        idx = set([qubit._index for qubit in qargs])
        if len(lst.intersection(idx)) != 0:
            qpos += 1
        if qpos == depth:
            break
        ci_pos += 1
    newCirc.data = circuit[:ci_pos] + insertCirc.data + circuit[ci_pos:]
    return newCirc
