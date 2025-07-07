import streamlit as st
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

def eulers_method(k, x0, y0, x_target, h):
    """
    Implement Euler's method for dy/dx = ky
    
    Parameters:
    k: proportionality constant
    x0: initial x value
    y0: initial y value
    x_target: target x value to reach
    h: step size
    
    Returns:
    DataFrame with step-by-step calculations, x_values, y_values
    """
    # Calculate number of steps
    num_steps = int((x_target - x0) / h)
    
    # Initialize arrays to store results
    x_values = [x0]
    y_values = [y0]
    slopes = []
    
    x_current = x0
    y_current = y0
    
    # Perform Euler's method iterations
    for i in range(num_steps):
        # Calculate slope at current point: f(x,y) = ky
        slope = k * y_current
        slopes.append(slope)
        
        # Calculate next point using Euler's formula
        x_next = x_current + h
        y_next = y_current + h * slope
        
        x_values.append(x_next)
        y_values.append(y_next)
        
        # Update current values
        x_current = x_next
        y_current = y_next
    
    # Create DataFrame for display
    df_data = []
    for i in range(num_steps):
        df_data.append({
            'Step': i,
            'x_n': x_values[i],
            'y_n': y_values[i],
            'f(x_n, y_n) = k*y_n': slopes[i],
            'y_{n+1} = y_n + h*f(x_n, y_n)': y_values[i+1]
        })
    
    df = pd.DataFrame(df_data)
    
    return df, x_values, y_values

def analytical_solution(k, x0, y0, x):
    """
    Calculate the analytical solution for dy/dx = ky
    Solution: y = y0 * e^(k*(x-x0))
    """
    return y0 * math.exp(k * (x - x0))

def main():
    st.title("Euler's Method for Differential Equations")
    st.markdown("### Solving dy/dx = ky")
    
    st.markdown("""
    This application implements Euler's method to solve differential equations where 
    the rate of change of a quantity is directly proportional to the amount present.
    """)
    
    # Create input section
    st.header("Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        k = st.number_input(
            "Proportionality constant (k):",
            value=1.0,
            format="%.6f",
            help="The constant of proportionality in dy/dx = ky"
        )
        
        x0 = st.number_input(
            "Initial x value (x₀):",
            value=0.0,
            format="%.6f",
            help="Starting x coordinate"
        )
    
    with col2:
        y0 = st.number_input(
            "Initial y value (y₀):",
            value=1.0,
            format="%.6f",
            help="Starting y coordinate"
        )
        
        x_target = st.number_input(
            "Target x value:",
            value=1.0,
            format="%.6f",
            help="X value to stop the calculation at"
        )
    
    h = st.number_input(
        "Step size (h):",
        value=0.1,
        min_value=0.001,
        max_value=1.0,
        format="%.6f",
        help="Size of each step in the Euler's method calculation"
    )
    
    # Input validation
    if st.button("Calculate", type="primary"):
        # Validate inputs
        if h <= 0:
            st.error("Step size must be positive!")
            return
        
        if x_target <= x0:
            st.error("Target x value must be greater than initial x value!")
            return
        
        if (x_target - x0) / h > 10000:
            st.error("Too many steps! Please increase step size or decrease target range.")
            return
        
        try:
            # Perform Euler's method calculation
            df, x_values, y_values = eulers_method(k, x0, y0, x_target, h)
            final_x, final_y = x_values[-1], y_values[-1]
            
            # Display step-by-step calculations
            st.header("Step-by-Step Calculations")
            st.markdown("**Euler's Formula:** y_{n+1} = y_n + h × f(x_n, y_n)")
            st.markdown("**For dy/dx = ky:** f(x, y) = k × y")
            
            # Display the calculations table
            st.dataframe(
                df.style.format({
                    'x_n': '{:.6f}',
                    'y_n': '{:.6f}',
                    'f(x_n, y_n) = k*y_n': '{:.6f}',
                    'y_{n+1} = y_n + h*f(x_n, y_n)': '{:.6f}'
                }),
                use_container_width=True
            )
            
            # Calculate analytical solution for comparison
            analytical_y = analytical_solution(k, x0, y0, final_x)
            
            # Create analytical solution curve for plotting
            x_analytical = np.linspace(x0, x_target, 100)
            y_analytical = [analytical_solution(k, x0, y0, x) for x in x_analytical]
            
            # Create interactive plot
            st.header("Visualization")
            
            fig = go.Figure()
            
            # Add Euler's method points and lines
            fig.add_trace(go.Scatter(
                x=x_values, 
                y=y_values,
                mode='markers+lines',
                name='Euler\'s Method',
                line=dict(color='blue', width=2),
                marker=dict(size=6, color='blue')
            ))
            
            # Add analytical solution curve
            fig.add_trace(go.Scatter(
                x=x_analytical,
                y=y_analytical,
                mode='lines',
                name='Analytical Solution',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            # Add step visualization (optional)
            if len(x_values) <= 20:  # Only show steps if not too many
                for i in range(len(x_values)-1):
                    # Horizontal line for each step
                    fig.add_trace(go.Scatter(
                        x=[x_values[i], x_values[i+1]],
                        y=[y_values[i], y_values[i]],
                        mode='lines',
                        line=dict(color='lightblue', width=1, dash='dot'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    # Vertical line for each step
                    fig.add_trace(go.Scatter(
                        x=[x_values[i+1], x_values[i+1]],
                        y=[y_values[i], y_values[i+1]],
                        mode='lines',
                        line=dict(color='lightblue', width=1, dash='dot'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
            
            fig.update_layout(
                title=f'Euler\'s Method vs Analytical Solution (dy/dx = {k}y)',
                xaxis_title='x',
                yaxis_title='y',
                hovermode='x unified',
                template='plotly_white',
                width=800,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display results
            st.header("Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Final Approximation (Euler's)",
                    f"{final_y:.6f}",
                    help="Result from Euler's method"
                )
            
            with col2:
                st.metric(
                    "Analytical Solution",
                    f"{analytical_y:.6f}",
                    help="Exact solution: y₀ × e^(k×(x-x₀))"
                )
            
            with col3:
                error = abs(analytical_y - final_y)
                relative_error = (error / abs(analytical_y)) * 100 if analytical_y != 0 else 0
                st.metric(
                    "Absolute Error",
                    f"{error:.6f}",
                    delta=f"{relative_error:.2f}% relative",
                    help="Difference between Euler's approximation and exact solution"
                )
            
            # Display formula information
            st.header("Mathematical Background")
            
            st.markdown(f"""
            **Differential Equation:** dy/dx = {k}y
            
            **Analytical Solution:** y = {y0} × e^({k} × (x - {x0}))
            
            **Euler's Method Formula:** y_{{n+1}} = y_n + {h} × {k} × y_n
            
            **Number of steps:** {len(df)}
            
            **Step size:** {h}
            """)
            
            # Accuracy note
            if relative_error > 5:
                st.warning(f"⚠️ High relative error ({relative_error:.2f}%). Consider using a smaller step size for better accuracy.")
            elif relative_error < 0.1:
                st.success(f"✅ Excellent accuracy! Relative error is only {relative_error:.4f}%.")
            else:
                st.info(f"ℹ️ Good accuracy. Relative error: {relative_error:.2f}%.")
                
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
    
    # Add information section
    st.header("About Euler's Method")
    
    with st.expander("Learn more about Euler's Method"):
        st.markdown("""
        **Euler's Method** is a first-order numerical procedure for solving ordinary differential equations 
        with a given initial value.
        
        **For the equation dy/dx = ky:**
        - This represents exponential growth (k > 0) or decay (k < 0)
        - Examples include population growth, radioactive decay, compound interest
        
        **How it works:**
        1. Start with initial point (x₀, y₀)
        2. Calculate the slope at this point: slope = k × y₀
        3. Move a small step h in the x direction
        4. Estimate the new y value: y₁ = y₀ + h × slope
        5. Repeat until reaching the target x value
        
        **Accuracy:**
        - Smaller step sizes generally give more accurate results
        - The method becomes less accurate over longer intervals
        - Error accumulates with each step
        """)

if __name__ == "__main__":
    main()
