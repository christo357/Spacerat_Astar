# Space Rat and Bot

This project simulates a bot searching for a rat on a ship represented by a grid. It uses different algorithms and strategies to demonstrate bot navigation, rat movement, and search efficiency. The project is modular, allowing flexibility for experimentation with various strategies.

## Files and Structure

- **`main.py`**: Entry point for the simulation. Initializes the ship, bots, and rat locations, and runs the search simulations.
- **`ship.py`**: Contains the `Ship` class, which represents the grid (ship) and handles cell manipulation, rat movements, and neighbor calculations.
- **`cell.py`**: Defines the `Cell` class, which is the fundamental unit of the grid. Each cell has properties such as value, neighbors, and probability.
- **`bot1.py` and `bot1_m.py`**: Implement bot algorithms for locating the rat. These files differ in strategies for handling stationary and moving rats.
- **`bot2.py` and `bot2_m.py`**: Advanced bot implementations with enhanced strategies for efficiency and adaptability.
- **`astar.py`**: Contains the `Astar` class, which uses the A* pathfinding algorithm to navigate the grid.
- **`logger.py`**: Provides utilities to log simulation states and bot movements for analysis and debugging.

## Setup

### Requirements

- Python 3.8 or later
- Required Python packages:
  - `pygame` (optional, for visualization if applicable)
  - `numpy`

## Execution

Run:
- pip install -r requirements.txt
- python main.py