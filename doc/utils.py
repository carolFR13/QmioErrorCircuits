from qiskit import QuantumCircuit

def create_example_circuit(num_qubits):
    # we are measuring 32 qubits so we need 32 classic qubits 
    # to save the results
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    # initialice all qubits to state |1⟩
    qc.x(range(num_qubits))
    
    # delay of 1 µs
    qc.delay(1, range(num_qubits), unit='us')
    
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    qc.delay(3, range(num_qubits), unit='us')
    qc.x(range(num_qubits))
    # delay of 1 µs
    qc.delay(1, range(num_qubits), unit='us')
    
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    qc.delay(3, range(num_qubits), unit='us')
    qc.x(range(num_qubits))
    # delay of 1 µs
    qc.delay(1, range(num_qubits), unit='us')
    
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    
    return qc