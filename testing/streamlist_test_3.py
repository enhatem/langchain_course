import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Initialize session state to store points and their status
if 'points' not in st.session_state:
    st.session_state.points = {'x': [], 'y': [], 'z': [], 'status': []}

st.title("3D Surface Point Checker")

# Create reference surface (z = x² - y² as example)
x_range = np.linspace(-5, 5, 50)
y_range = np.linspace(-5, 5, 50)
x_grid, y_grid = np.meshgrid(x_range, y_range)
z_surface = x_grid**2 - y_grid**2  # Example surface equation

# Input form for points
with st.form("point_input"):
    st.subheader("Input 3D Point")
    col1, col2, col3 = st.columns(3)
    x = col1.number_input("X coordinate", value=0.0)
    y = col2.number_input("Y coordinate", value=0.0)
    z = col3.number_input("Z coordinate", value=0.0)
    
    submitted = st.form_submit_button("Check Point")
    if submitted:
        # Calculate surface z at (x,y)
        surface_z = x**2 - y**2  # Same as surface equation
        status = "above" if z > surface_z else "below"
        
        # Store point and status
        st.session_state.points['x'].append(x)
        st.session_state.points['y'].append(y)
        st.session_state.points['z'].append(z)
        st.session_state.points['status'].append(status)
        
        st.success(f"Point is {status} the surface (surface z: {surface_z:.2f})")

# Create figure
fig = go.Figure()

# Add reference surface
fig.add_trace(go.Surface(
    x=x_grid,
    y=y_grid,
    z=z_surface,
    colorscale='Blues',
    opacity=0.6,
    name="Reference Surface",
    showscale=False
))

# Add points with color coding
if st.session_state.points['x']:
    # Convert status to colors
    colors = ['green' if status == 'above' else 'red' 
              for status in st.session_state.points['status']]
    
    fig.add_trace(go.Scatter3d(
        x=st.session_state.points['x'],
        y=st.session_state.points['y'],
        z=st.session_state.points['z'],
        mode='markers',
        marker=dict(
            size=6,
            color=colors,
            opacity=0.8
        ),
        name="Input Points"
    ))

# Set plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)  # Initial camera angle
        )
    ),
    width=800,
    height=600,
    margin=dict(r=20, l=20, b=20, t=40)
)

# Display plot
st.plotly_chart(fig)

# Clear button
if st.button("Clear All Points"):
    st.session_state.points = {'x': [], 'y': [], 'z': [], 'status': []}
    st.experimental_rerun()

# Surface equation display
st.markdown("""
**Surface Equation**: z = x² - y²  
**Color Coding**:
- <span style="color:green">Green</span> points are above the surface
- <span style="color:red">Red</span> points are below the surface
""", unsafe_allow_html=True)