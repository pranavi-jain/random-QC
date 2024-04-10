from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info.analysis import hellinger_fidelity


def get_matched_fidelity(op1, op2, basis):
    res1 = op1.get(basis)
    res2 = op2.get(basis)
    fidelity = hellinger_fidelity(res1, res2)
    return fidelity


def get_fidelity_data(meas1, meas2, noisyMeas):
    """Utility function to get fidelities between
        - the circuit and itself, and
        - the circuit and the noisy circuit
        for a single measurement set performed in all 3 basis.

    Args:
        meas1 (_type_): _description_
        meas2 (_type_): _description_
        noisyMeas (_type_): _description_

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
        for b in ("X", "Y", "Z"):
            sumC += get_matched_fidelity(meas1[i], meas2[i], b)
            fidCC.append(sumC)
            sumN += get_matched_fidelity(meas1[i], noisyMeas[i], b)
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
