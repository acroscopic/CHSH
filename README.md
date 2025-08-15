# Introduction

The Clauser–Horne–Shimony–Holt (CHSH) inequality is a specific form of Bell's inequality which is used to test Bell's theorem, which demonstrates that quantum mechanics is incompatible with local hidden-variable theories. A hidden-variable theory is a deterministic model of physics which introduces additional "hidden" variables that cannot be measured to explain quantum phenomena, and local hidden-variable theories satisfy the principle of locality, which requires that distant events cannot influence each other faster than the speed of light, and that their outcomes are statistically independent.

This reposity contains three programs to demonstrate the violation of this inequality. Two of these programs use the Qiskit Aer simulator to experimentally prove the violation. One in a noiseless environment, one in a simulated noisy environment. The final of the three programs run directly on IBM Quantum Hardware.

This code was written for my undergraduate PHY 3035 Quantum Mechanics course as an honors project to give me the opportunity to learn Qiskit and the basics of Quantum Information Theory.

## File Structure Outline
```bash
.
├── requirements.txt       # Program dependencies for pip
├── Aer_Qasm.py            # Noisy simulation of the CHSH Experiment
├── Aer_StateVector.py     # Noiseless simulation of the CHSH Experiment
├── CHSH_Experiment.py     # The CHSH Experiment for IBM Quantum Hardware
├── CHSH.tex               # LaTeX Document to generate CHSH.pdf  
├── CHSH_Paper.pdf         # Exposition of all required information. **READ ME**
├── GSPlotter.py           # Plotting software that I wrote for MatPlotLib
├── Data.py                # Used for succesively running simulations for plot generation
├── LICENSE.md             # GNU General Public License
└── README.md              # The document you're reading right now
```

## Setup
```bash
# Clone the repository
$ git clone https://github.com/acroscopic/CHSH.git
$ cd CHSH

# Create the virtual environment
$ python -m venv venv
$ source venv/bin/activate
$ venv\Scripts\activate # For Windows users

# Install dependencies
$ pip install -r requirements.txt
```

### Aer Simulator Usage:
```bash
# For the Statevector simulator, simply run it without any arguments to see the static results
$ python Aer_StateVector.py

# For the Qasm simulator it is possible to achieve values above 2√2 because of the inherent noise
# When running the code, you can specify the number of shots you want to pass
# Higher shots means higher statistical significance, but longer run times
# The default is 2^20. Lower numbers are *not* recommended.
$ python Aer_Qasm.py --shots 1048576 
```

### For Usage on IBM Quantum Hardware

First, you will need to make an [IBM Cloud Account](https://quantum.cloud.ibm.com/registration).

Next, you will need to find your [IBM Qiskit API Key](https://quantum.cloud.ibm.com/).

Then, open `CHSH_Experiment.py` in whatever text editor and update the token variable at the start of the program.

Finally, run the program.

```bash
$ python CHSH_Experiment.py
```
