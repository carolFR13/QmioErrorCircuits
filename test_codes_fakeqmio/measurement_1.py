from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio
import time

# number of qubits
num_qubits = 5

backend = FakeQmio(gate_error = True, readout_error = True)

# list to save results
results_list = []

# we initialice the circuit with *num_qubits* qubits and the 
# same number of classical ones to measure them
qc = QuantumCircuit(num_qubits, num_qubits)

qc.x(range(num_qubits)) # applying x gate: |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')  # delay of  1 µs
qc.measure(range(num_qubits), range(num_qubits))

qct = transpile(qc, backend)

num_repetitions = 100000

start_time = time.time() #initial time t = 0

with open("results1.txt", "w") as f:
    f.write("Repetition\tTime(s)\tState\n")

# including try except to save each iteration in the file
# in case the job is interrupted
try: 
    for i in range(num_repetitions):
        job = backend.run(qct, shots=1, repetition_period=500000)  # repetition_period en ns
        result = job.result()
        counts = result.get_counts(qc)

        # absolute time between measurements ?
        absolute_time = time.time() - start_time

        for state in counts:
            # saving the result in each iteration
            with open("results1.txt", "a") as f:
                f.write(f"{i + 1}\t{absolute_time:.6f}\t{state}\n")
                f.flush()  # forcing the file to be immediately saved

        print(f"Repetition {i+1}: Measured state = {state}, Absolute time = {absolute_time:.6f} s")

        # free memory
        del job, result, counts

except Exception:
    print("\n Program interrupted.")

print("Execution finalized. Results available in 'results1.txt'")