import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Initialize session state to store coordinates
if 'points' not in st.session_state:
    st.session_state.points = {'x': [], 'y': [], 'z': []}

st.title("3D Coordinate Plotter")

# Input form
with st.form("coord_input"):
    st.subheader("Add New Coordinate")
    col1, col2, col3 = st.columns(3)
    x = col1.number_input("X coordinate", value=0.0)
    y = col2.number_input("Y coordinate", value=0.0)
    z = col3.number_input("Z coordinate", value=0.0)
    
    submitted = st.form_submit_button("Add Point")
    if submitted:
        # Add new point to session state
        st.session_state.points['x'].append(x)
        st.session_state.points['y'].append(y)
        st.session_state.points['z'].append(z)
        st.success(f"Added point: ({x}, {y}, {z})")

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot points if we have any
if len(st.session_state.points['x']) > 0:
    xs = st.session_state.points['x']
    ys = st.session_state.points['y']
    zs = st.session_state.points['z']
    
    ax.scatter(xs, ys, zs, c='r', marker='o', s=100)
    ax.plot(xs, ys, zs, color='b')  # Connect points with lines
    
    # Set labels
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    
    # Set dynamic axis limits
    max_range = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)) * 0.5
    mid_x = (max(xs) + min(xs)) * 0.5
    mid_y = (max(ys) + min(ys)) * 0.5
    mid_z = (max(zs) + min(zs)) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

st.pyplot(fig)

# # Optional: Add clear button
# if st.button("Clear All Points"):
#     st.session_state.points = {'x': [], 'y': [], 'z': []}
#     st.experimental_rerun()