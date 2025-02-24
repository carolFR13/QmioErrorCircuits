from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio

# number of qubits
num_qubits = 5

backend = FakeQmio(gate_error = True, readout_error = True)

# we initialice the circuit with *num_qubits* qubits and the 
# same number of classical ones to measure them
qc = QuantumCircuit(num_qubits, num_qubits)

qc.x(range(num_qubits)) # applying x gate: |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')  # delay of  1 µs
qc.measure(range(num_qubits), range(num_qubits))


num_repetitions = 10

for i in range(num_repetitions):

    qct = transpile(qc, backend)
    job = backend.run(qct, shots=1, repetition_period = 500000) # repetition_period in ns ? 
    result = job.result()
    counts = result.get_counts(qc)
    
    print(f"Repetition {i+1} - FakeQmio Counts:", counts)