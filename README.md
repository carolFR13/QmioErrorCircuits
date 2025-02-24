Here we provide the codes to perform some measurements about coherence times in qubits using qmio infrastructure at CESGA.

According to the qmio tutorial the first implementation should run agains FakeQmio backend (an emulator of the qpu) from qmio-tools to inspect the implementation of the code. We implement the testing codes for each measurement in ```test_codes_fakeqmio```. To run the codes we procede as follows:

- Load the qmio-tools module: ```module load qmio-tools```.
- Submit the job with the specifications ```sbatch -p ilk job_fakeqmio.sh```.
- You can check the status of the job with ``` squeue ```.


We want to implement the following codes:

1. Study of an asymmetry between transitions |0> -> |1>  and |1> -> |0>.

For that we expect to perform an algorithm which does the following: 

1. Initialize all qubits at state |1>
2. Wait 1 µs.
3. Measure the state of all qubits. 

Repeat the process after 5T_1 = 500 µs.

We will do this measurement both for initial states |0> and |1> to check if this asymmetry exists.

2. Study of the implementation with short times.

The algorithm would be something as follows:

1. Apply x gate. 
2. Wait 1 µs.
3. Measure the state of all qubits.
4. Wait 5 µs. (this could be any amount of time we would consider)
5. Apply x gate.
   
And repeat as many times as we want. With this implementation the number of errors has to be defined from 
the previous measurement.






