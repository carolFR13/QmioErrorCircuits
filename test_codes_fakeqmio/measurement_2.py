from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio


# number of qubits
num_qubits = 32

backend = FakeQmio()

def create_circuit(num_qubits):

    # we are measuring 32 qubits so we need 32 classic qubits to save the results
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    qc.delay(1, range(num_qubits), unit='us') # delay of 1 µs
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    return qc


# repeating each 100 µs for 100s
# num_repetitions = int(100 / 0.0001)
num_repetitions = 100

for i in range(num_repetitions):

    # initializing the circuit 
    qc = create_circuit(num_qubits)
    
    # executing the circuit 
    qct = transpile(qc, backend)
    job = backend.run(qct, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    # printing results
    print(f"Repetition {i+1} - FakeQmio Counts:", counts)

    qc.delay(100, range(num_qubits), unit='us')  # delay of 100 µs