import plotly.graph_objects as go
import numpy as np


def visualize_lanes(lanes_data):
    fig = go.Figure()
    
    # Colors for different lanes
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'yellow', 'cyan', 'magenta', 'lime', 'navy', 'maroon']

    for lane_data in lanes_data:
        
        points = np.array([pt['location'] for pt in lane_data['points']])
        right_vectors = np.array([pt['right_vector'] for pt in lane_data['points']])
        widths = np.array([pt['lane_width'] for pt in lane_data['points']])

        new_points= []
        for point, right_vector, width in zip(points, right_vectors, widths):
            # Calculate the left and right points
            left_point = point + right_vector * width*0.5
            right_point = point - right_vector * width * 0.5

            #print (f"left_point : {left_point}")
            #print (f"right_point : {right_point}")

            # Append the points to the list alternately
            new_points.append(left_point)
            new_points.append(right_point)
        
        
        print(f" lane id : {lane_data.get('id')}")
        print(f"number of points : {len(new_points)}")
        #print(new_points)
        

        # Prepare the mesh data
        new_points = np.array(new_points)

        # Extract x, y, z coordinates
        x = new_points[:, 0]
        y = new_points[:, 1]
        z = new_points[:, 2]

        poly_corners = []
        for i in range(0,len(new_points)-2,2):
            poly_corners.append([i, i+1, i+3])
            poly_corners.append([i, i+3, i+2])
        
        poly_corners = np.array(poly_corners)
        #transpose the array
        #poly_corners = poly_corners.T

        i = poly_corners[:, 0]
        j = poly_corners[:, 1]
        k = poly_corners[:, 2]

        go_mesh = go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5, color=colors[lane_data.get('id')%len(colors)])
        fig.add_trace(go_mesh)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', range=[-250, 250]),
            yaxis=dict(title='Y', range=[-500, 500]),
            zaxis=dict(title='Z', range=[-250, 250])
        ),
        title='Lane Mesh Visualization'
    )
    fig.show()

   

            