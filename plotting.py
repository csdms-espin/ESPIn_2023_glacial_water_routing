import matplotlib.pyplot as plt
import numpy as np

def flowdir_plot(mg,quiver_d=2,surface='topographic__elevation',surf_cmap='cividis',quiver_c = 'white',title='Drainage Plot',scale=1):
    ''' Graph of Flow direction on topography '''
    #set base parameters:
    fig,ax = plt.subplots(1,1)
    ny,nx = mg.number_of_node_rows, mg.number_of_node_columns
    
    #create 2D numpy arrays:
    node_grid = np.reshape(np.arange(0,len(mg.at_node[surface])),(nx,ny)) #array of node numbers
    receiver_grid = np.reshape(mg.at_node['flow__receiver_node'],(nx,ny)) #array of number of node receiving flow
    grid = np.reshape(mg.at_node[surface],(nx,ny)) #topography array
    
    #find coordinates for quivers to be made:
    quiver_x = [int(i) for i in mg.node_x if i%quiver_d==0 ]
    quiver_y = [int(i) for i in mg.node_y if i%quiver_d==0 ]
    quiver_coords = list(zip(quiver_y,quiver_x))
    x_dir = []
    y_dir = []
    for q in quiver_coords:
        y,x = np.where(node_grid == receiver_grid[q])[1][0], np.where(node_grid == receiver_grid[q])[0][0]
        #create unit vector:
        x_vector = x-q[1]
        y_vector = y-q[0]
        length = np.sqrt((x_vector**2) + (y_vector**2))
        
        if length != 0:
            x_dir.append(x_vector/length)
            y_dir.append(y_vector/length)
        else:
            x_dir.append(0)
            y_dir.append(0)
    #plotting:
    ax.imshow(grid,cmap=surf_cmap)
    ax.quiver(quiver_x,quiver_y,x_dir,y_dir,color=quiver_c)