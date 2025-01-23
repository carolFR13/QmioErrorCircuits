We will perform the following measurements using qmio infrastructure at CESGA: 

1. First measurement. First description of qubits coherence times.

*Starting with state |1 >* to perform the measurement (verification).

    1. Initialize all qubits at state |1>
    2. Wait 1 mus.
    3. Measure the stateof all qubits.

Repeat the process each 100 mus.


2. Second measurement. First description of qubits coherence times.


*Starting with state |0 >* to perform the measurement (verification).

    1. Initialize all qubits at state |0>
    2. Wait 1 mus.
    3. Measure the stateof all qubits.

Repeat the process each 100 mus.


3. Third measurement. Measurement of phase coherence times.

    1. Initialize all qubits by applying a pi/2-pulse
    2. Let the qubits evolve for a time t = n * 0.2 mus
    3. Apply another pi/2-pulse to all qubits.
    4. Measure the state of all qubits

being n a parameter that runs from 0 to 100, studying the interval [0,20]mus.

Repeat each 100 mus.


4. Fourth measurement. Detailed study of qubits coherence times

    1. Initialize all qubits at state |1>
    2. Wait 1 mus.
    3. Measure the stateof all qubits.

Repeat the process each 100 mus.


5. Fifth measurement. Accurate measure to study impact of quasiparticles in the chip.

    1. Initialize all qubits at state |1>
    2. After 0 mus performe the measurement of all qubits.
    3. Initialize all qubits at state |1>
    4. After 0.5 mus performe the measurement of all qubits.
    5. Initialize all qubits at state |1>
    6. After 1 mus performe the measurement of all qubits.
    7. Initialize all qubits at state |1>
    8. After 1.5 mus performe the measurement of all qubits.
    9. Initialize all qubits at state |1>
    10. After 2 mus performe the measurement of all qubits.

Repeat the process after 100 mus


According to qmio tutorial the first implementation should run agains FakeQmio backend from qmio-tools to inspect the implementation of the code. We implement the testing codes for each measurement in ```test_codes_fakeqmio```. To run the codes we procede as follows:




