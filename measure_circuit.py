from qiskit import transpile
from qiskit.circuit.library import HGate, SdgGate

"""Helper module for running measurements on circuits, and storing the measurement 
outcomes (probability distributions) in an output object."""


class _MeasurementHelper:
    """Helper class containing all utility functions to perform measurements on circuit in three
    different basis X, Y, Z"""
    
    ## Parametrized constructor 
    def __init__(self, noq, circuit, backend): 
        self.num_q = noq 
        self.circuit = circuit 
        self.backend = backend

    ## Defining output object (for storing measurement outcomes) - dictionary with basis as keys
    @staticmethod
    def get_obj_inst():
        keyList = ["X", "Y", "Z"]
        obj = {}
        for i in keyList:
            obj[i] = None
        return obj

    ## Circuit measurement on given backend service, and storing the output
    def measure_circuit(self, circ, obj, basis):
        circ.measure_all()
        backend = self.backend
        tqc = transpile(circ, backend)      ## Optional - can skip transpilation
        counts = backend.run(tqc).result().get_counts()
        obj.update({basis:counts})
        circ.remove_final_measurements()

    ## Measuring given circuit in X, Y, Z basis
    def get_measurement_output(self):
        obj = self.get_obj_inst() 
        
        # Measurement in X basis 
        tempCirc = self.circuit.copy()
        tempCirc.append(HGate(), [range(0, self.num_q)])
        self.measure_circuit(tempCirc, obj, "X")
        
        # Measurement in Y basis
        tempCirc = self.circuit.copy()
        tempCirc.append(HGate(), [range(0, self.num_q)])
        tempCirc.append(SdgGate(), [range(0, self.num_q)])
        self.measure_circuit(tempCirc, obj, "Y")
        
        # # Measurement in Z basis
        self.measure_circuit(self.circuit, obj, "Z")
        return obj


"""Utilty function called on the circuit to perform measurement and return the output object."""

def get_circuit_output(circuit, runs, backend):
    """
    Args:
    circuit (QuantumCircuit): circuit on which to perform measurment
    run (int): number of times measurement is performed
    backend (IBMBackendService): IBM backend service to be called
    
    The final object returned is a list of 'n' measurements run on the circuit."""
    
    num_q = circuit.num_qubits
    output = [dict() for x in range(runs)]
    
    helperObj = _MeasurementHelper(num_q, circuit, backend)
    for i in range(0, runs):
        result = helperObj.get_measurement_output()
        output[i] = result 
    return output
