from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import QmioBackend
import time

# number of qubits
num_qubits = 6
init_state = None  # CHANGE MANUALLY

backend = QmioBackend(logging_level=3)

# we initialice the circuit with *num_qubits* qubits and the 
# same number of classical ones to measure them
qc = QuantumCircuit(num_qubits, num_qubits)

# ---- circuit definition -----
qc.x(range(num_qubits)) # applying x gate: |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')  # delay of  1 µs
qc.measure(range(num_qubits), range(num_qubits)) # this operation takes about 5 µs

qct = transpile(qc, backend, initial_layout=[20, 21, 22, 23, 30, 31])

#------ parameters ------
n_repetitions = 8192              # max allowed by hardware
repetition_period = 0.000015      # 15 µs per shot
target_time = 100                 # run ~100 seconds


start_time = time.time() #initial time t = 0
total_batches = 0
total_shots = 0


with open("results_cosmic.txt", "a") as f:
    f.write(f"# repetition_period: {repetition_period} s\n")
    f.write(f"# state initialized to: {init_state} \n")
    f.write("Batch\tShot\tState\tAbsTime[s]\n")

    # keep running until we reach ~target_time
    while True:
        batch_start = time.time()

        # run one batch
        result = backend.run(
            qct,
            shots=n_repetitions,
            repetition_period=repetition_period,
            output_qasm3=True,
            memory=True
        ).result()

        memory = result.get_memory(qct)
        del result  # free memory

        total_batches += 1

        # append results immediately
        for (i, state) in enumerate(memory):
            shot_index = total_shots + i + 1
            abs_time = time.time() - start_time
            f.write(f"{total_batches}\t{shot_index}\t{state}\t{abs_time:.6f}\n")

        total_shots += n_repetitions

        # check elapsed time
        elapsed = time.time() - start_time
        print(f"Batch {total_batches} done, elapsed {elapsed:.2f} s")

        if elapsed >= target_time:
            print("Reached target time (~100s), stopping.")
            break
