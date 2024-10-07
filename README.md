# ONLINE-MINADM Algorithm Simulation and Analysis
### Capstone Project - Ort Braude College

This project simulates and analyzes the ONLINE-MINADM algorithm for minimizing Add-Drop Multiplexers (ADMs) in optical networks. It implements a dynamic, online solution for managing lightpaths while comparing the performance against the optimal offline solution. The project focuses on two primary network topologies: **path** and **ring**, and provides a detailed analysis of the algorithm’s efficiency using competitive ratios and empirical performance measurements.

## Table of Contents
- [Overview](#overview)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Algorithm Details](#algorithm-details)
- [Analysis and Results](#analysis-and-results)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
Optical networks are essential for modern communication, allowing the transmission of large volumes of data over long distances. The ONLINE-MINADM algorithm is designed to dynamically assign wavelengths to lightpaths in such networks to minimize the switching cost, measured in the number of Add-Drop Multiplexers (ADMs).

This project is divided into two phases:
1. **Phase A**: An in-depth study of the algorithm, exploring its theoretical foundation, competitive ratios, and efficiency in various topologies.
2. **Phase B**: Implementation of a Python program with a graphical interface to simulate the algorithm, compare it with an optimal offline solution, and perform algorithm analysis.

---

## Installation and Setup

### Prerequisites
- Python 3.x
- PyQt5 (for GUI)
- Matplotlib (for graphical representation)
- Any other Python libraries listed in the `requirements.txt` file.

### Steps to Set Up the Project
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Online-MinADM-Simulation.git
   cd Online-MinADM-Simulation
