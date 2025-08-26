from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import QmioBackend
import numpy as np
import csv

# number of qubits
num_qubits = 6

backend = QmioBackend(logging_level=3)

delays = np.logspace(0, 3, 20)  # 20 points from 1 µs to 1000 µs
delays = [int(d) for d in delays]

# prepare CSV file
with open("t1_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["delay_us", "qubit", "p1"])  # header

    for t in delays:
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.x(range(num_qubits))  # prepare |1>
        qc.delay(t, range(num_qubits), unit="us")
        qc.measure(range(num_qubits), range(num_qubits))

        qct = transpile(qc, backend, initial_layout=[20, 21, 22, 23, 30, 31])

        result = backend.run(qct, shots=1000).result()
        counts = result.get_counts(qct)

        # compute P(1) for each qubit
        for qubit in range(num_qubits):
            ones = sum([count for bitstring, count in counts.items() if bitstring[num_qubits-1-qubit] == "1"])
            p1 = ones / 1000
            writer.writerow([t, qubit, p1])




