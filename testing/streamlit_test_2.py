import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Initialize session state to store coordinates
if 'points' not in st.session_state:
    st.session_state.points = {'x': [], 'y': [], 'z': []}

st.title("Interactive 3D Coordinate Plotter")

# Input form
with st.form("coord_input"):
    st.subheader("Add New Coordinate")
    col1, col2, col3 = st.columns(3)
    x = col1.number_input("X coordinate", value=0.0)
    y = col2.number_input("Y coordinate", value=0.0)
    z = col3.number_input("Z coordinate", value=0.0)
    
    submitted = st.form_submit_button("Add Point")
    if submitted:
        st.session_state.points['x'].append(x)
        st.session_state.points['y'].append(y)
        st.session_state.points['z'].append(z)
        st.success(f"Added point: ({x}, {y}, {z})")

# Create interactive 3D plot
fig = go.Figure()

# Add scatter plot if we have points
if len(st.session_state.points['x']) > 0:
    fig.add_trace(go.Scatter3d(
        x=st.session_state.points['x'],
        y=st.session_state.points['y'],
        z=st.session_state.points['z'],
        mode='markers+lines',
        marker=dict(
            size=8,
            color='red',
        ),
        line=dict(
            color='blue',
            width=4
        )
    ))

# Set plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        aspectmode='auto'  # Automatically adjust aspect ratio
    ),
    width=800,
    height=600
)

# Display the interactive plot
st.plotly_chart(fig)

# # Clear button
# if st.button("Clear All Points"):
#     st.session_state.points = {'x': [], 'y': [], 'z': []}
#     st.experimental_rerun()