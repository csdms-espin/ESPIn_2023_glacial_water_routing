from landlab.components import FlowDirectorD8, FlowAccumulator, SinkFillerBarnes
from landlab import RasterModelGrid
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from bmi_topography import Topography
<<<<<<< HEAD
=======

>>>>>>> bd3150af5c5e983fa0a4b95b2dc83a3a0dfd3606

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
            
        if case == 'Andes':
            self.case = case
            self.topo = Topography(
                dem_type="SRTMGL1",
                south=-1.540602,
                north=-1.424255,
                west=-78.9056896,
                east=-78.753253,
                output_format="GTiff",
                cache_dir=".",
<<<<<<< HEAD
                api_key='6031740f5ac334c30f3a24fac6cce268'
=======
                api_key = '6031740f5ac334c30f3a24fac6cce268',
>>>>>>> bd3150af5c5e983fa0a4b95b2dc83a3a0dfd3606
            )
            self.fname = self.topo.fetch()
            self.da = self.topo.load()
            self.grid = RasterModelGrid((self.da.shape[1:3]),xy_spacing=(30,30)) 
            self.grid.set_closed_boundaries_at_grid_edges(True, True, True, False)
            self.da = self.da.astype(np.float64) # type casting to float64, float32 will not work
            self.grid.add_field("topographic__elevation", np.flip(self.da,1), at="node"); # don't forget to flip image, because of ASCII indeces
            self.sfb = SinkFillerBarnes(self.grid, method='D8', fill_flat=False)
            self.sfb.run_one_step()
        
        if case == 'Manual':
            self.case = case
            self.topo = Topography(
                dem_type="SRTMGL1",
                south=args[0],
                north=args[1],
                west=args[2],
                east=args[3],
                output_format="GTiff",
                cache_dir=".",
                api_key = '6031740f5ac334c30f3a24fac6cce268',
            )
            self.fname = self.topo.fetch()
            self.da = self.topo.load()
            self.grid = RasterModelGrid((self.da.shape[1:3]),xy_spacing=(30,30)) 
            self.grid.set_closed_boundaries_at_grid_edges(True, True, True, False)
            self.da = self.da.astype(np.float64) # type casting to float64, float32 will not work
            self.grid.add_field("topographic__elevation", np.flip(self.da,1), at="node"); # don't forget to flip image, because of ASCII indeces
            self.sfb = SinkFillerBarnes(self.grid, method='D8', fill_flat=False)
            self.sfb.run_one_step()
        
            
        
    def create_flow_acc(self,flow_director='FlowDirectorD8',runoff_rate=None):
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