from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio


# number of qubits
num_qubits = 32

backend = FakeQmio()

def create_circuit(num_qubits, wait_time_us):

    qc = QuantumCircuit(num_qubits, num_qubits)

    # initialice all qubits to state |1⟩
    qc.x(range(num_qubits))
    
    qc.delay(wait_time_us, range(num_qubits), unit='us') # delay of *wait_time_us* µs
    # measuring all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

# repeating each 100 µs for 100s
# num_repetitions = int(100 / 0.0001)
num_repetitions = 100

wait_times = [0, 0.5, 1, 1.5, 2]  # µs

for cycle in range(num_repetitions):

    print(f"Cycle {cycle + 1}")

    for wait_time in wait_times:

        # initializing the circuit
        qc = create_circuit(num_qubits, wait_time)
        
        qct = transpile(qc, backend)
        job = backend.run(qct, shots=1024)
        result = job.result()
        counts = result.get_counts(qc)
        
        # printing results
        print(f"Wait time {wait_time} µs - FakeQmio Counts:", counts)

    
    qc.delay(100, range(num_qubits), unit='us')  # delay of 100 µs