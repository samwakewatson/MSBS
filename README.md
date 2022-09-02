# Modular Sharded Blockchain Simulator (MSBS)

## What is MSBS?
**MSBS** is an open source sharded blockchain simulator based on the BlockSim simulator. It is a transaction level blockchain simulator that aims to accommodate the more complex consensus mechanisms implemented by sharded blockchains. The simulator aims to be applicable to the majority of sharded blockchain systems, and adapts the consensus, network, and incentives layer abstractions seen in BlockSim to the case of sharded blockchains. MSBS is implemented in **Python**.

A paper detailing the design of our simulator will be released in the near future.

## Installation and Requirements

Before you can use BlockSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter
- matplotlib
>pip install matplotlib
- openpyxl
>pip install openpyxl

## Running the simulator

Before you run the simulator, you must specify a base config in the Config.py file. Once this is done, you can specify variables to alter between each run by modifying the experimentConfigs.json file. A few other alterations may need to be made in the Main.py and Multiprocessing.py files to ensure the config is updated on each run, and that the automatic graph plotting is functioning as desired.

To run the simulator, one needs to trigger the main class in *Multiprocessing.py* 
> python Multiprocessing.py

Alternatively, to run only a single simulation one can run the main class in *Main.py* (however this will require minor modification to the main function)
> python Main.py

## Statistics and Results

There are several possible formats for results. Excel files providing a detailed per block breakdown of the simulation are automatically produced. The main function returns a results object containing data on the simulation configuration and certain statistics from the simulation, and this can be leveraged to automatically plot graphs of the results. The code for this is contained in Multiprocessing.py

## Contact

I can be contacted at **swakewatson@gmail.com** for any questions about the simulator or how to extend it.
