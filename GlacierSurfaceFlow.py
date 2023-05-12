from landlab.components import FlowDirectorD8, FlowAccumulator, SinkFillerBarnes
from landlab import RasterModelGrid
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


class GlacierSurfaceFlow:
    '''
    Class to create model grid and FlowAccumulator for a glacier. Sets a grid for a given test case, creates a FlowAccumulator using the FlowDirectorD8 and contains graphing functions to visualise the data.
    '''
    
    
    def __init__(self,case= 'Channel', dem = None):        
        if case == 'Parabola':
            self.case = case
            self.grid = RasterModelGrid((10,10)) #create model grid
            self.elev = self.grid.add_field("topographic__elevation", self.grid.y_of_node+ 0.1 * (self.grid.x_of_node-4)**2, at="node") #add sloping parabola as elevation
        
        if case == 'Channel':
            self.case = case
            self.grid = RasterModelGrid((10,10)) #create model grid
            self.elev = self.grid.add_field("topographic__elevation", 1*self.grid.y_of_node, at="node") 
            self.elev[(self.grid.x_of_node > 2) & (self.grid.x_of_node < 4)] -=2 #add channel to topography
            
        if case == 'Nye Dome':
            self.case = case
            self.grid = RasterModelGrid((50,50)) #create model grid
            
            # calculate 
            z2 = 100 - 0.5*((self.grid.y_of_node-25)**2 + (self.grid.x_of_node-25)**2)
            z2[z2 <0]=0.01*np.random.rand(len(z2[z2<0]))
            elev = self.grid.add_field('topographic__elevation',np.sqrt(z2),at='node')
            
        if case == 'Manual':
            self.coord = input('input your coordinates')
            
        
    def create_flow_acc(self,flow_director='FlowDirectorD8'):
        self.fa = FlowAccumulator(self.grid,flow_director=flow_director)
        self.fa.run_one_step()
        self.da,self.q = self.fa.accumulate_flow()
    
    def surf_plot(self,surface='topographic__elevation', title=None):
        if title == None:
            title = f'Topography for {self.case}'
        plt.figure()
        ax=plt.axes(projection='3d')

        # plot the surface
        z = self.grid.at_node[surface].reshape(self.grid.shape)
        color = cm.gray((z - z.min()) / (z.max() - z.min()))
        ax.plot_surface(
            self.grid.x_of_node.reshape(self.grid.shape),
            self.grid.y_of_node.reshape(self.grid.shape),
            z,
            rstride=1,
            cstride=1,
            cmap=cm.gray,
            linewidth=0.0,
            antialiased=False,
        )
        ax.view_init(elev=35,azim=-120)
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_zlabel('elevation')
        plt.title(title)
        plt.show()