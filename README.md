# Lift-Elevator-Control-System

## Overview
The Lift Control System is a simulation project designed to optimize elevator scheduling and improve efficiency in multi-story buildings. The system implements and compares three different scheduling algorithms: **SCAN, LOOK, and MYLIFT**. The goal is to minimize waiting times while effectively handling passenger requests using data structures like priority queues and dictionaries.

This project was developed as part of the **ECM1414: Data Structures and Algorithms** module.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Implemented Algorithms](#implemented-algorithms)
5. [Simulation & Results](#simulation--results)
6. [Contributors](#contributors)
7. [Acknowledgements](#acknowledgements)

## Project Structure
```
/[740047493]                 
│
├── specification             
│   ├── coursework_spec.pdf   
│   └── additional_docs/      
│
├── sources                   
│   ├── main.py               
│   ├── Lift.py               
│   ├── Request.py            
│   │   ├── LiftSystem_SCAN.py
│   │   ├── LiftSystem_LOOK.py
│   │   ├── MyLift.py        
│   │   ├── PriorityQueue_SCAN.py
│   │   ├── PriorityQueue_LOOK.py
│   │   ├── Base_PriorityQueue.py
│   │   ├── validate_requests.py
│   │   ├── check_floors_and_capacity.py
│   │   ├── finalTestingforSCANLOOK.py
│
├── presentation              
│   └── presentation_link.txt
│
├── results                   
│   ├── simulation_report.pdf
│   ├── charts/               
│   └── data/                 
│
└── README.md                 
```

## Installation
1. Ensure you have **Python 3.x** installed.
2. Clone or extract the repository.
3. Navigate to the project directory:
   ```bash
   cd [740047493]/sources
   ```
4. Install required dependencies (if any):
   ```bash
   pip install -r requirements.txt  # If applicable
   ```

## Usage
To run the simulation, execute:
```bash
python main.py
```
The system will:
- Load input request data from JSON files.
- Simulate elevator scheduling using the SCAN, LOOK, and MYLIFT algorithms.
- Output performance results in the **results/** directory.

## Implemented Algorithms
### **SCAN Algorithm**
- Moves in one direction until reaching the highest or lowest requested floor, then reverses.
- Ensures all requests are served but may result in longer wait times.

### **LOOK Algorithm**
- Similar to SCAN but reverses direction early if no further requests exist in the current direction.
- Reduces unnecessary travel, leading to improved efficiency.

### **MYLIFT Algorithm**
- Custom-developed algorithm designed to outperform SCAN and LOOK.
- Dynamically picks up passengers while dropping off existing ones.
- Considers lift capacity, waiting time, and real-time constraints.

## Simulation & Results
The performance of each algorithm was tested across multiple scenarios. Key findings include:
- **MYLIFT consistently outperforms SCAN and LOOK**, achieving lower average wait times and higher efficiency.
- **LOOK performs better than SCAN**, especially under high-demand scenarios.
- **SCAN has the highest wait times**, particularly in large buildings with many requests.

Example Performance Data:
| Algorithm | Avg Wait Time (s) | Requests Served | Efficiency Score |
|-----------|-----------------|----------------|------------------|
| SCAN      | 146             | 14             | 0.0959          |
| LOOK      | 94              | 14             | 0.1489          |
| MYLIFT    | 80              | 14             | 0.1750          |

For detailed simulation results, refer to the **results/** directory.

## Contributors
- **Necla Derin Lara Eksi** – SCAN & LOOK Algorithm Implementation
- **George Littler** – MYLIFT Algorithm & Main File Development
- **Su Bektas** – Pseudocode & Documentation
- **Rafe Frederick Crowley** – Performance Analysis & Simulations
- **Amelia Hope** – Documentation & Video Editing

## Acknowledgements
This project was completed as part of **ECM1414: Data Structures and Algorithms** at the **University of Exeter**. Special thanks to our module instructors and teaching assistants for their support.

