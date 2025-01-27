Here we provide the codes to perform some measurements about coherence times in qubits using qmio infrastructure at CESGA.

At the end of the file there arethe algorithms to implement to perform each measurement.

According to the qmio tutorial the first implementation should run agains FakeQmio backend (an emulator of the qpu) from qmio-tools to inspect the implementation of the code. We implement the testing codes for each measurement in ```test_codes_fakeqmio```. To run the codes we procede as follows:

- Load the qmio-tools module: ```module load qmio-tools```.
- Submit the job with the specifications ```sbatch job_fakeqmio.sh```.
- You can check the status of the job with ``` squeue ```.




We will perform the following measurements:

1. First measurement. First description of qubits coherence times.

*Starting with state |1 >* to perform the measurement (verification).

    1. Initialize all qubits at state |1>
    2. Wait 1 µs.
    3. Measure the stateof all qubits. 
    

Repeat the process each 100 µs.


2. Second measurement. First description of qubits coherence times.


*Starting with state |0 >* to perform the measurement (verification).

    1. Initialize all qubits at state |0>
    2. Wait 1 µs.
    3. Measure the stateof all qubits.

Repeat the process each 100 µs.


3. Third measurement. Measurement of phase coherence times.

*Starting with state |1 >* (verification).

    1. Initialize all qubits by applying a pi/2-pulse
    2. Let the qubits evolve for a time t = n * 0.2 µs
    3. Apply another pi/2-pulse to all qubits.
    4. Measure the state of all qubits

being n a parameter that runs from 0 to 100, studying the interval [0,20]µs.

Repeat each 100 µs.


4. Fourth measurement. Detailed study of qubits coherence times.

*Starting with state |1 >* (verification).

    1. Initialize all qubits at state |1>
    2. Wait 1 µs.
    3. Measure the stateof all qubits.

Repeat the process each 3 µs.


5. Fifth measurement. Accurate measure to study impact of quasiparticles in the chip.

*Starting with state |1 >* (verification).

    1. Initialize all qubits at state |1>
    2. After 0 µs performe the measurement of all qubits.
    3. Initialize all qubits at state |1>
    4. After 0.5 µs performe the measurement of all qubits.
    5. Initialize all qubits at state |1>
    6. After 1 µs performe the measurement of all qubits.
    7. Initialize all qubits at state |1>
    8. After 1.5 µs performe the measurement of all qubits.
    9. Initialize all qubits at state |1>
    10. After 2 µs performe the measurement of all qubits.

Repeat the process after 100 µs






