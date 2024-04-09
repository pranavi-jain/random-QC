from qiskit.quantum_info.analysis import hellinger_fidelity

"""Utility function to get fidelity for our output dictionary object - measuring 
fidelity on matching basis"""

def get_matched_fidelity(op1, op2, basis):
    res1 = op1.get(basis)
    res2 = op2.get(basis)
    fidelity = hellinger_fidelity(res1, res2)
    return fidelity
