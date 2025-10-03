from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import QmioBackend
import time
from datetime import datetime

# number of qubits
num_qubits = 32
init_state = 1  

backend = QmioBackend(logging_level=0)
print(f"Backend initialized: {backend}")

# we initialice the circuit with *num_qubits* qubits and the 
# same number of classical ones to measure them
qc = QuantumCircuit(num_qubits, num_qubits)

# ---- circuit definition -----
qc.x(range(num_qubits)) # applying x gate: |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')  # delay of  1 µs
qc.measure(range(num_qubits), range(num_qubits)) # this operation takes about 5 µs

initial_layout=[6, 8, 10, 11, 12, 14, 15, 16, 20, 21, 22, 23, 25, 26, 30, 31]
print(f"Transpiling circuit with {num_qubits} qubits...")
qct = transpile(qc, backend)
print(f"Circuit transpiled successfully")

#------ parameters ------
n_repetitions = 8192              # max allowed by hardware
repetition_period = 0.00015     # 150 µs per shot
target_time = 25                # run ~50 seconds


start_wall = time.time() #initial time t = 0
total_batches = 0
total_shots = 0

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

pwd = "/mnt/netapp2/Store_uni/home/usc/ie/cfr/"
# Create unique filename
filename = pwd+f"high_period_{num_qubits}_qubits_{target_time}_s_{timestamp}.txt"


print(f"Starting measurement loop, writing to: {filename}")
print(f"Target time: {target_time}s, shots per batch: {n_repetitions}, repetition period: {repetition_period}s")

with open(filename, "a") as f:
    f.write(f"# repetition_period: {repetition_period} s\n")
    f.write(f"# state initialized to: {init_state} \n")
    f.write("Batch\tShot\tState\tAbsTime[s]\n")

    # keep running until we reach ~target_time
    while True:
        batch_start = time.time()

        # run one batch
        try:
            print(f"Starting batch {total_batches + 1}...")
            result = backend.run(
                qct,
                shots=n_repetitions,
                repetition_period=repetition_period,
                output_qasm3=True,
                memory=True
            ).result()

            memory = result.get_memory(qct)
            del result  # free memory
        except Exception as e:
            print(f"Error in batch {total_batches + 1}: {e}")
            raise

        total_batches += 1
        elapsed_qpu = total_shots * repetition_period
        elapsed_wall = time.time() - start_wall

        # append results immediately
        for (i, state) in enumerate(memory):
            shot_index = total_shots + i + 1
            f.write(f"{total_batches}\t{shot_index}\t{state}\t{elapsed_wall:.6f}\n")

        total_shots += n_repetitions

        print(f"Batch {total_batches} done, QPU exposure {elapsed_qpu:.2f}s, Wall {elapsed_wall:.2f} s")

        if elapsed_qpu >= target_time:
            print(f"Reached target exposure (~{target_time}s of qubit evolution), stopping.")
            break

print("Total time:", time.time() - start_wall)

