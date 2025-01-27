from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio


# number of qubits
num_qubits = 32

def create_circuit(num_qubits):

    # we are measuring 32 qubits so we need 32 classic qubits to save the results
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    qc.delay(1000, range(num_qubits), unit='us') # delay of 1000 ns = 1 µs
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

qc = create_circuit(num_qubits)

backend = FakeQmio()

qct = transpile(qc, backend)

# executing the circuit in the emulator
job = backend.run(qct, shots=1024)
result = job.result()
counts = result.get_counts(qc)

# printing results
print("FakeQmio Counts:", counts)

# repeating each 100 µs for 100s
# num_repetitions = int(100 / 0.0001)
num_repetitions = 100
for i in range(num_repetitions):

    qc.delay(100000, range(num_qubits), unit='us')  # delay of 100000 ns = 100 µs

    # initializing again the circuit ?
    qc = create_circuit(num_qubits)
    
    # executing the circuit ? 
    qct = transpile(qc, backend)
    job = backend.run(qct, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    # printing results
    print(f"Repetition {i+1} - FakeQmio Counts:", counts)