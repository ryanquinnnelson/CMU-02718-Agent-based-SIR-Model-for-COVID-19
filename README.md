# 02718-HW4
Fall 2020 - Computational Medicine course project - Agent-Based Model for SARS-CoV-2 Virus Spread

### Summary

This project implements and tests a simple Agent Based Model (ABM) to study the spread of a virus through a population. A casual SRI model was built using a simplified set of rules for infection and recovery, with metrics captured at simulated time steps for later visualization and analysis. The code for the model was developed as a Python package, complete with unit tests and documentation.

Simulations were performed using 250 agents over a 365 day period under multiple scenarios (i.e. Agents wearing or not wearing masks, Agents practicing or not practicing physical distancing, Percentage vaccinated) and results were visualized using a Jupyter Notebook.



### Project Structure
The code for the Agent Based Model is defined as Python package `abm` under /packages.
