import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Initialize session state with sample points
if 'points' not in st.session_state:
    # Sample data points (on the surface z = x² - y²)
    sample_points = [
        {'x': 2, 'y': 0, 'z': 4, 'label': 'Point A (Surface)'},
        {'x': 0, 'y': 2, 'z': -4, 'label': 'Point B (Surface)'},
        {'x': 3, 'y': 1, 'z': 8, 'label': 'Above Example'},
        {'x': 1, 'y': 3, 'z': -8, 'label': 'Below Example'}
    ]
    
    st.session_state.points = {
        'x': [p['x'] for p in sample_points],
        'y': [p['y'] for p in sample_points],
        'z': [p['z'] for p in sample_points],
        'status': ['above' if p['z'] > (p['x']**2 - p['y']**2) else 'below' for p in sample_points],
        'labels': [p['label'] for p in sample_points]
    }

st.title("3D Surface Analysis Tool")

# Create reference surface (z = x² - y²)
x_range = np.linspace(-5, 5, 50)
y_range = np.linspace(-5, 5, 50)
x_grid, y_grid = np.meshgrid(x_range, y_range)
z_surface = x_grid**2 - y_grid**2

# Input form for new points
with st.form("point_input"):
    st.subheader("Add New Point")
    col1, col2, col3, col4 = st.columns(4)
    x = col1.number_input("X", value=0.0)
    y = col2.number_input("Y", value=0.0)
    z = col3.number_input("Z", value=0.0)
    label = col4.text_input("Label", value="P-")
    
    submitted = st.form_submit_button("Add Point")
    if submitted:
        surface_z = x**2 - y**2
        status = "above" if z > surface_z else "below"
        
        st.session_state.points['x'].append(x)
        st.session_state.points['y'].append(y)
        st.session_state.points['z'].append(z)
        st.session_state.points['status'].append(status)
        st.session_state.points['labels'].append(label)
        
        st.success(f"{label} ({x}, {y}, {z}) is {status} surface (surface Z: {surface_z:.2f})")

# Create plot
fig = go.Figure()

# Add reference surface
fig.add_trace(go.Surface(
    x=x_grid,
    y=y_grid,
    z=z_surface,
    colorscale='Blues',
    opacity=0.5,
    name="Reference Surface",
    showscale=False
))

# Add all points with labels
if st.session_state.points['x']:
    colors = ['green' if s == 'above' else 'red' for s in st.session_state.points['status']]
    
    fig.add_trace(go.Scatter3d(
        x=st.session_state.points['x'],
        y=st.session_state.points['y'],
        z=st.session_state.points['z'],
        mode='markers+text',
        text=st.session_state.points['labels'],
        textposition="top center",
        marker=dict(
            size=6,
            color=colors,
            opacity=0.9
        ),
        textfont=dict(
            size=14,
            color="black"
        ),
        name="Data Points"
    ))

# Configure plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        camera=dict(eye=dict(x=1.8, y=1.8, z=0.8))
    ),
    width=1000,
    height=800,
    margin=dict(l=0, r=0, b=0, t=30)
)

# Display plot
st.plotly_chart(fig, use_container_width=True)

# Control panel
with st.expander("Controls"):
    if st.button("Clear All User Points"):
        # Keep the original sample points
        st.session_state.points = {
            'x': [2, 0, 3, 1],
            'y': [0, 2, 1, 3],
            'z': [4, -4, 8, -8],
            'status': ['above', 'below', 'above', 'below'],
            'labels': ['Point A (Surface)', 'Point B (Surface)', 'Above Example', 'Below Example']
        }
        st.experimental_rerun()
    
    st.markdown("""
    **Predefined Points**:
    - Green points are above the surface
    - Red points are below the surface
    - Surface equation: z = x² - y²
    - Sample points demonstrate different positions
    """)

st.write("Rotate the plot with mouse drag, zoom with scroll wheel!")