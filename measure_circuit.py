import random
from qiskit import transpile
from qiskit.circuit.library import HGate, SdgGate

"""Helper module for running measurements on circuits, and storing the measurement 
outcomes (probability distributions) in an output object."""


def get_standard_basis_list(runs, num_q):
    basis_list = []
    bases = ["X", "Y", "Z"]
    for i in range(runs):
        current_basis = bases[i % len(bases)]
        basis_string = current_basis * num_q
        basis_list.append(basis_string)
    return basis_list


def get_random_basis_list(runs, num_q):
    """Utility function to get a list of random basis choice for circuit measurement

    Returns:
        basis_list: array of strings selected as basis choice for 'n' qubits
    """
    basis_list = []
    basis = ""
    for i in range(runs):
        for q in range(num_q):
            basis += random.choice(["X", "Y", "Z"])
        basis_list.append(basis)
        basis = ""
    return basis_list


class _MeasurementHelper:
    """Helper class containing all utility functions to perform measurements on circuit in three
    different basis X, Y, Z"""

    ## Parametrized constructor
    def __init__(self, noq, circuit, backend):
        self.num_q = noq
        self.circuit = circuit
        self.backend = backend

    ## Circuit measurement on given backend service, and storing the output
    def measure_circuit(self, circuit):
        circuit.measure_all()
        backend = self.backend
        tqc = transpile(circuit, backend)  ## Optional - can skip transpilation
        counts = backend.run(tqc).result().get_counts()
        return counts

    ## Measuring given circuit in X, Y, Z basis
    def get_measurement_output(self, basis):
        tempCirc = self.circuit.copy()
        tempCirc.barrier()

        for q in range(len(basis)):
            if basis[q] == "X":
                tempCirc.h(q)

            elif basis[q] == "Y":
                tempCirc.sdg(q)
                tempCirc.h(q)

            elif basis[q] == "Z":
                continue

            else:
                raise ValueError("Problem in given basis - " + basis)

        return self.measure_circuit(tempCirc)


"""Utilty function called on the circuit to perform measurement and return the output object."""


def get_meas_output(circuit, backend, basis_list):
    """
    Args:
    circuit (QuantumCircuit): circuit on which to perform measurment
    backend (IBMBackendService): IBM backend service to be called
    basis_list (array): array of basis choice for which to perform measurement

    The final object returned is a list of 'n' measurements run on the circuit in the given basis_list.
    """

    runs = len(basis_list)
    num_q = circuit.num_qubits
    output = [[None] * 2 for x in range(runs)]

    helperObj = _MeasurementHelper(num_q, circuit, backend)
    arr = [None] * 2
    for i in range(runs):
        result = helperObj.get_measurement_output(basis_list[i])
        arr[0] = basis_list[i]
        arr[1] = result
        output[i] = arr
        arr = [None] * 2
    return output
