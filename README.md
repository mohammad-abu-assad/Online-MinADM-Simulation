# ONLINE-MINADM Algorithm Simulation and Analysis

### Capstone Project - Ort Braude College

This project simulates and analyzes the **ONLINE-MINADM algorithm** for minimizing Add-Drop Multiplexers (ADMs) in optical networks. It implements a dynamic, online solution for managing lightpaths while comparing the performance against the optimal offline solution. The project focuses on two primary network topologies: **path** and **ring**, and provides a detailed analysis of the algorithm’s efficiency using competitive ratios and empirical performance measurements.

## Table of Contents

- [Overview](#overview)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Steps to Set Up the Project](#steps-to-set-up-the-project)
- [Usage](#usage)
  - [User Interface Overview](#user-interface-overview)
  - [Workflow](#workflow)
- [Algorithm Details](#algorithm-details)
  - [ONLINE-MINADM Algorithm](#online-minadm-algorithm)
    - [Key Features](#key-features)
    - [How It Works](#how-it-works)
  - [Optimal Offline Solution](#optimal-offline-solution)
    - [Characteristics](#characteristics)
- [Analysis and Results](#analysis-and-results)
  - [Competitive Ratio](#competitive-ratio)
  - [Empirical Results](#empirical-results)
    - [Simulation Scenarios](#simulation-scenarios)
    - [Findings](#findings)
  - [Visualizations](#visualizations)
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

- **Python 3.x**
- **PyQt5** (for GUI)
- **Matplotlib** (for graphical representation)
- **NumPy** (for numerical operations)
- **Pandas** (for data handling)
- Any other Python libraries listed in the `requirements.txt` file.

### Steps to Set Up the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/Online-MinADM-Simulation.git
   cd Online-MinADM-Simulation
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, manually install the required packages:

   ```bash
   pip install PyQt5 matplotlib numpy pandas
   ```

---

## Usage

To run the application, execute the main Python script:

```bash
python main.py
```

### User Interface Overview

Upon launching the application, you will see a graphical interface with the following sections:

1. **Algorithm Simulation**:

   - **Input Network Parameters**: Set the number of nodes, select the network topology (path or ring), and specify available wavelengths.
   - **Define Traffic Demands**: Manually input lightpaths or import from a file.
   - **Run Simulation**: Execute the ONLINE-MINADM algorithm and visualize wavelength assignments and ADM placements.

2. **Optimal Solution Comparison**:

   - **Generate Optimal Solution**: Compute the optimal offline solution for the same traffic demands.
   - **Compare Results**: View side-by-side comparisons of ADM usage, wavelength assignments, and performance metrics.

3. **Algorithm Analysis**:

   - **Performance Metrics**: Analyze competitive ratios, ADM counts, and resource utilization.
   - **Graphs and Charts**: Generate visual representations of the algorithm's performance under various scenarios.
   - **Export Reports**: Save analysis results and graphs for documentation or further study.

### Workflow

1. **Setting Up the Network**:

   - Choose the **network topology**: Path or Ring.
   - Set the **number of nodes** in the network.
   - Define the **available wavelengths**.

2. **Defining Traffic Demands**:

   - **Manual Entry**: Add lightpaths by specifying source and destination nodes.
   - **Import Data**: Load traffic demands from a CSV file.

3. **Running the Simulation**:

   - Navigate to the **Algorithm Simulation** tab.
   - Click **Run Simulation** to execute the ONLINE-MINADM algorithm.
   - Observe the **real-time visualization** of the algorithm's decision-making process.

4. **Comparing with Optimal Solution**:

   - Switch to the **Optimal Solution Comparison** tab.
   - Generate the **optimal offline solution**.
   - Compare **ADM usage**, **wavelength assignments**, and **efficiency** between the online and optimal solutions.

5. **Analyzing Results**:

   - Go to the **Algorithm Analysis** tab.
   - Adjust parameters to explore different scenarios.
   - Generate and export **graphs**, **charts**, and **reports**.

---

## Algorithm Details

### ONLINE-MINADM Algorithm

The **ONLINE-MINADM algorithm** is an online approach for wavelength assignment in optical networks, aiming to minimize the number of ADMs used, see more details about the algorithm in Capstone Project Phase A-23-1-R-19.

#### Key Features

- **Online Decision-Making**: Makes wavelength assignment decisions as lightpath requests arrive, without knowledge of future requests.
- **Minimizing ADMs**: Efficiently reduces the number of ADMs, leading to cost savings.
- **Support for Multiple Topologies**: Applicable to both path and ring network configurations.

#### How It Works

1. **Initialization**:

   - Set up the network parameters and initialize available wavelengths.

2. **Processing Lightpath Requests**:

   - For each incoming request, assign a wavelength that minimizes the introduction of new ADMs.

3. **ADM Allocation**:

   - Determine ADM placements based on the assigned wavelengths and network topology.

4. **Dynamic Updates**:

   - Update the network state to reflect the new assignments and prepare for subsequent requests.

### Optimal Offline Solution

The optimal offline solution computes the minimum number of ADMs required by considering all lightpath requests collectively.

#### Characteristics

- **Global Knowledge**: Has complete information about all lightpath requests beforehand.
- **Minimum ADM Usage**: Provides a baseline for the lowest possible number of ADMs needed.
- **Benchmarking**: Used to evaluate the efficiency of the online algorithm.

---

## Analysis and Results

### Competitive Ratio

The **competitive ratio** is used to measure the performance of the online algorithm relative to the optimal offline solution.
see more about the analysis and results in Capstone Project Phase B-23-1-R-19

- **Definition**: Competitive Ratio = (Cost of Online Algorithm) / (Cost of Optimal Offline Algorithm)
- **Interpretation**: A competitive ratio closer to 1 indicates better performance of the online algorithm.

### Empirical Results

#### Simulation Scenarios

- **Variable Network Sizes**: Tested on networks with different numbers of nodes.
- **Traffic Demand Variations**: Analyzed performance under varying volumes and patterns of lightpath requests.
- **Topology Comparison**: Compared results between path and ring topologies.

#### Findings

- **Efficiency**: The ONLINE-MINADM algorithm consistently achieves a competitive ratio within a small constant factor of the optimal.
- **Scalability**: Performance scales well with increased network size and traffic volume.
- **Topology Impact**: The algorithm performs differently on path and ring topologies, with specific competitive ratios for each.

### Visualizations

- **Graphs**:

  - **ADM Usage vs. Number of Lightpaths**: Shows how ADM count increases with more lightpath requests.
  - **Competitive Ratio over Network Sizes**: Illustrates how the competitive ratio changes with network scale.

- **Charts**:

  - **Wavelength Utilization**: Depicts how effectively wavelengths are used.
  - **ADM Distribution**: Visualizes the placement of ADMs across the network.

- **Reports**:

  - Detailed analysis reports are available in the `analysis/reports/` directory.

---

## Technologies Used

- **Python 3.x**: Core programming language.
- **PyQt5**: For building the graphical user interface.
- **Matplotlib**: For generating plots and charts.
- **NumPy**: For numerical computations and data manipulation.
- **Pandas**: For handling datasets and CSV files.
- **JSON**: For storing network configurations.

---

## Contributing

Contributions are welcome! To contribute to this project:

1. **Fork the Repository**:

   - Click on the 'Fork' button at the top right of the repository page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/yourusername/Online-MinADM-Simulation.git
   ```

3. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Commit Your Changes**:

   ```bash
   git commit -m 'Add your feature description'
   ```

5. **Push to Your Branch**:

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Open a Pull Request**:

   - Go to your fork on GitHub and click on the 'New pull request' button.

Please ensure your code follows the project's coding standards and includes appropriate documentation.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

If you have any questions or need further assistance, feel free to open an issue on GitHub or contact the project maintainers.

---

**Thank you for using the ONLINE-MINADM Algorithm Simulation and Analysis tool!**
