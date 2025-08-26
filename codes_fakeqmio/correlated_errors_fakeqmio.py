from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio
import time

# number of qubits
num_qubits = 6

backend = FakeQmio(gate_error = True, readout_error = True)

# we initialice the circuit with *num_qubits* qubits and the 
# same number of classical ones to measure them
qc = QuantumCircuit(num_qubits, num_qubits)

# ---- circuit definition -----
qc.x(range(num_qubits)) # applying x gate: |0> -> |1>
qc.delay(1, range(num_qubits), unit='us')  # delay of  1 µs
qc.measure(range(num_qubits), range(num_qubits)) # this operation takes about 5 µs

# delay of *repetition_periot - execution_circuit_time* from equivalent circuit in qmio
qc.delay(600, range(num_qubits), unit='us') 

qct = transpile(qc, backend, initial_layout=[20, 21, 22, 23, 30, 31])

#------ circuit execution ------
n_repetitions = 1000 ; circuit_time = 621

start_time = time.time() #initial time t = 0

n_shots = n_repetitions
result = backend.run(qct, shots=n_repetitions, memory = True).result()  
memory = result.get_memory(qct)

# absolute time the circuit lasted
absolute_time = time.time() - start_time

# free memory
del result

#----- results ----
print('The absolute exectution time was: ', absolute_time)
print('The theoretical exectution time is(mus): ', n_repetitions*circuit_time)
print('memory:\n', memory)


with open("results2_fakeqmio.txt", "a") as f:
    f.write("Repetition\tState\n")
    for (i,state) in enumerate(memory):
        f.write(f"{i + 1}\t{state}\n")

