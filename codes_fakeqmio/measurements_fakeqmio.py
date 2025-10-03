from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio
import time

# ---------------- PARAMETERS ----------------
num_qubits = 6
init_state = None  
n_repetitions = 8192              # max per batch
repetition_period = 15e-6         # desired repetition period in seconds
target_exposure = 100             # 100s exposure to compare with qmio results

# ---------------- BACKEND ----------------
backend = FakeQmio(gate_error=True, readout_error=True)

# ---------------- CIRCUIT ----------------
qc = QuantumCircuit(num_qubits, num_qubits)
qc.x(range(num_qubits))                # |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')
qc.measure(range(num_qubits), range(num_qubits))

# approximate intrinsic duration of the active ops (µs)
active_time = 12e-6   # ~1 µs delay + ~5 µs measure + overhead ≈ 12 µs

# pad with idle delay so that total ~ repetition_period
extra_delay = max(0, repetition_period - active_time)
qc.delay(extra_delay * 1e6, range(num_qubits), unit='us')

# transpile
qct = transpile(qc, backend, initial_layout=[20, 21, 22, 23, 30, 31])

# ---------------- EXECUTION LOOP ----------------
total_batches = 0
total_shots = 0
start_wall = time.time()

with open("results_fakeqmio.txt", "a") as f:
    f.write(f"# repetition_period: {repetition_period} s\n")
    f.write(f"# extra delay inserted: {extra_delay} s\n")
    f.write(f"# state initialized to: {init_state} \n")
    f.write("Batch\tShot\tState\tElapsedQPU[s]\tElapsedWall[s]\n")

    while True:
        # run one batch
        result = backend.run(qct, shots=n_repetitions, memory=True).result()
        memory = result.get_memory(qct)
        del result  # free memory

        total_batches += 1
        elapsed_qpu = total_shots * repetition_period
        elapsed_wall = time.time() - start_wall

        # save results shot by shot
        for (i, state) in enumerate(memory):
            shot_index = total_shots + i + 1
            shot_qpu_time = shot_index * repetition_period
            f.write(f"{total_batches}\t{shot_index}\t{state}\t{shot_qpu_time:.6f}\t{elapsed_wall:.6f}\n")

        total_shots += n_repetitions

        print(f"Batch {total_batches} done, QPU exposure {elapsed_qpu:.3f} s, Wall {elapsed_wall:.2f} s")

        if elapsed_qpu >= target_exposure:
            print("Reached target exposure, stopping.")
            break

