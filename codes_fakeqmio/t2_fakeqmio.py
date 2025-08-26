from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio
import numpy as np
import csv

# number of qubits
num_qubits = 6

backend = FakeQmio(gate_error = True, readout_error = True)


delays = np.logspace(0, 3, 20)  # 20 points from 1 µs to 1000 µs
delays = [int(d) for d in delays]

# prepare CSV file
with open("t2_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["delay_us", "qubit", "p1"])  # header

    for t in delays:
        qc = QuantumCircuit(num_qubits, num_qubits)

        # --- Step 1: π/2 pulse with phase = +i ---
        for q in range(num_qubits):
            qc.u(np.pi/2, 0, np.pi/2, q)   # (|0> + i|1>)/√2

        # --- Step 2: free evolution ---
        qc.delay(t, range(num_qubits), unit="us")

        # --- Step 3: final π/2 pulse ---
        for q in range(num_qubits):
            qc.u(np.pi/2, 0, 0, q)   # standard π/2 pulse (like Hadamard)

        # --- Step 4: measurement ---
        qc.measure(range(num_qubits), range(num_qubits))

        qct = transpile(qc, backend, initial_layout=[20, 21, 22, 23, 30, 31])

        result = backend.run(qct, shots=1000).result()
        counts = result.get_counts(qct)

        # compute P(1) for each qubit
        for qubit in range(num_qubits):
            ones = sum([count for bitstring, count in counts.items() if bitstring[num_qubits-1-qubit] == "1"])
            p1 = ones / 1000
            writer.writerow([t, qubit, p1])


