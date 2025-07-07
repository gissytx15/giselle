# Euler's Method Calculator

A Streamlit web application that implements Euler's method for solving differential equations of the form dy/dx = ky.

## Features

- Interactive parameter input (k, initial values, target x, step size)
- Step-by-step calculation display
- Comparison with analytical solution
- Error analysis and accuracy feedback
- Educational content about Euler's method

## Running the Application

### Local Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install streamlit numpy pandas
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

### Online Demo

Visit the deployed application at: [Streamlit Cloud URL will be here after deployment]

## Usage

1. Enter the proportionality constant (k)
2. Set initial x and y values
3. Choose your target x value
4. Set the step size (smaller = more accurate)
5. Click "Calculate" to see results

The app will show:
- Step-by-step Euler's method calculations
- Final approximation vs exact analytical solution
- Error analysis and accuracy recommendations

## Mathematical Background

This application solves differential equations where the rate of change is proportional to the current amount:

**dy/dx = ky**

Examples include:
- Population growth (k > 0)
- Radioactive decay (k < 0)
- Compound interest calculations

The analytical solution is: **y = y₀ × e^(k×(x-x₀))**

Euler's method approximates this using: **y_{n+1} = y_n + h × k × y_n**