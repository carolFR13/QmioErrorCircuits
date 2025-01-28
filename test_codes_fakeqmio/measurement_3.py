from qiskit import QuantumCircuit, transpile
from qmiotools.integrations.qiskitqmio import FakeQmio


num_qubits = 32

backend = FakeQmio()

# creating the base circuit
def create_phase_coherence_circuit(num_qubits, evolve_time_us):

    qc = QuantumCircuit(num_qubits, num_qubits)

    # inital pi/2 pulse to all qubits
    for qubit in range(num_qubits):
        qc.rx(3.14159 / 2, qubit)  
    
    # letting qubits evolve for *evolve_time_us* us
    qc.delay(evolve_time_us, range(num_qubits), unit='us')  
    
    # final pi/2 pulse to all qubits
    for qubit in range(num_qubits):
        qc.rx(3.14159 / 2, qubit)  
    
    # measuring the states of all qubits
    qc.measure(range(num_qubits), range(num_qubits))
    return qc


num_repetitions =  100

# Repeating each measurement each 100 mus
for cycle in range(num_repetitions):
    print(f"Cycle {cycle + 1}/{num_repetitions}")
    for n in range(101):
        # creating a new circuit with the corresponding evolve_time
        qc = create_phase_coherence_circuit(n * 0.2)
        
        qct = transpile(qc, backend)
        
        job = backend.run(qct, shots=1024)
        result = job.result()
        counts = result.get_counts(qc)
        
        # printting the results
        print(f"Evolve time {n*0.2} µs - FakeQmio Counts:", counts)
    
    qc.delay(100, range(num_qubits), unit='mu')  
