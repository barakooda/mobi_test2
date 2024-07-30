import plotly.graph_objects as go
import numpy as np


def visualize_lanes(lanes_data):
    fig = go.Figure()
    
    # Colors for different lanes
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'yellow', 'cyan']

    for lane_idx, lane_data in enumerate(lanes_data):
        points = np.array([pt['location'] for pt in lane_data['points']])
        right_vectors = np.array([pt['right_vector'] for pt in lane_data['points']])
        widths = np.array([pt['lane_width'] for pt in lane_data['points']])

        # Calculate the left and right boundary points of the lane
        half_widths = widths / 2
        left_boundary = points - right_vectors * half_widths[:, np.newaxis]
        right_boundary = points + right_vectors * half_widths[:, np.newaxis]

        # Combine the boundary points for the mesh
        vertices_x = np.concatenate([left_boundary[:, 0], right_boundary[:, 0]])
        vertices_y = np.concatenate([left_boundary[:, 1], right_boundary[:, 1]])
        vertices_z = np.concatenate([left_boundary[:, 2], right_boundary[:, 2]])

        # Create indices for the mesh faces
        num_points = len(points)
        i = []
        j = []
        k = []

        for idx in range(num_points - 1):
            i.extend([idx, idx + num_points])
            j.extend([idx + 1, idx + 1 + num_points])
            k.extend([idx + num_points, idx + 1])

        # Create the mesh
        mesh = go.Mesh3d(
            x=vertices_x,
            y=vertices_y,
            z=vertices_z,
            i=i,
            j=j,
            k=k,
            color=colors[lane_idx % len(colors)],
            opacity=0.5,
            name=f"Lane ID: {lane_data.get('id', 'Unknown')}"
        )

        # Add the mesh to the figure
        fig.add_trace(mesh)

    # Update the layout
    fig.update_layout(
        title='3D Visualization of Multiple Lanes',
        scene=dict(
            xaxis=dict(title='X Axis'),
            yaxis=dict(title='Y Axis'),
            zaxis=dict(title='Z Axis')
        ),
        legend_title_text='Lane ID'
    )

    # Show the figure
    fig.show()