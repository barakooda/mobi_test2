import plotly.graph_objects as go
import numpy as np


def visualize_lanes(lane_data):
    points = np.array([pt['location'] for pt in lane_data['points']])
    right_vectors = np.array([pt['right_vector'] for pt in lane_data['points']])
    up_vectors = np.array([pt['up_vector'] for pt in lane_data['points']])
    widths = np.array([pt['lane_width'] for pt in lane_data['points']])

    # Normalize vectors (if they are not unit vectors)
    right_vectors /= np.linalg.norm(right_vectors, axis=1, keepdims=True)
    up_vectors /= np.linalg.norm(up_vectors, axis=1, keepdims=True)

    # Calculate left and right boundaries of the lane
    half_width = widths / 2
    left_boundary = points - right_vectors * half_width[:, None] #+ up_vectors * 0.1  # Offset slightly by up_vector for visibility
    right_boundary = points + right_vectors * half_width[:, None] #+ up_vectors * 0.1

    # Concatenate vertices for the mesh
    vertices_x = np.concatenate([left_boundary[:, 0], right_boundary[:, 0]])
    vertices_y = np.concatenate([left_boundary[:, 1], right_boundary[:, 1]])
    vertices_z = np.concatenate([left_boundary[:, 2], right_boundary[:, 2]])

    # Create indices for the mesh faces
    indices = []
    num_points = len(points)
    for i in range(num_points - 1):
        indices.append([i, i + num_points, i + 1])
        indices.append([i + num_points, i + num_points + 1, i + 1])

    indices = np.array(indices).flatten()

    # Create a Mesh3d object
    mesh = go.Mesh3d(
        x=vertices_x,
        y=vertices_y,
        z=vertices_z,
        i=indices[::3],
        j=indices[1::3],
        k=indices[2::3],
        color='blue',
        opacity=0.5,
        name=f"Lane ID: {lane_data.get('id', 'Unknown')}"
    )

    # Create a Plotly figure and add the mesh
    fig = go.Figure(data=[mesh])

    # Update the layout
    fig.update_layout(
        title='3D Visualization of a Single Lane',
        scene=dict(
            xaxis=dict(title='X Axis'),
            yaxis=dict(title='Y Axis'),
            zaxis=dict(title='Z Axis')
        ),
        legend_title_text='Lane ID'
    )

    # Show the figure
    fig.show()