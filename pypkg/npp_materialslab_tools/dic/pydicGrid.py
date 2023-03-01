import math
import os

import cv2
import numpy as np
import scipy.interpolate
from matplotlib import pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider
from scipy.interpolate import Rbf, griddata


class Plot:
    def __init__(self, image, grid, data, title):
        self.data = np.ma.masked_invalid(data)
        self.data_copy = np.copy(self.data)
        self.grid_x = grid.grid_x
        self.grid_y = grid.grid_y
        self.data = np.ma.array(self.data, mask=self.data == np.nan)
        self.title = title
        self.image = image

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.25, bottom=0.25)

        self.ax.imshow(image, cmap=plt.cm.binary)
        #ax.contour(grid_x, grid_y, g, 10, linewidths=0.5, colors='k', alpha=0.7)

        
        self.im = self.ax.contourf(grid.grid_x, grid.grid_y, self.data, 10, cmap=plt.cm.rainbow,
                         vmax=self.data.max(), vmin=self.data.min(), alpha=0.7)
        self.contour_axis = plt.gca()

        self.ax.set_title(title)
        self.cb = self.fig.colorbar(self.im)

        axmin = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
        axmax = self.fig.add_axes([0.25, 0.15, 0.65, 0.03])
        self.smin = Slider(axmin, 'set min value', self.data.min(), self.data.max(), valinit=self.data.min(),valfmt='%1.6f')
        self.smax = Slider(axmax, 'set max value', self.data.min(), self.data.max(), valinit=self.data.max(),valfmt='%1.6f')
        
        self.smax.on_changed(self.update)
        self.smin.on_changed(self.update)
        

    def update(self, val):
        self.contour_axis.clear()
        self.ax.imshow(self.image, cmap=plt.cm.binary)
        self.data = np.copy(self.data_copy)
        self.data = np.ma.masked_where(self.data > self.smax.val, self.data)
        self.data = np.ma.masked_where(self.data < self.smin.val, self.data)
        self.data = np.ma.masked_invalid(self.data)

        self.im = self.contour_axis.contourf(self.grid_x, self.grid_y, self.data, 10, cmap=plt.cm.rainbow, alpha=0.7)

        
        self.cb.update_bruteforce(self.im)
        self.cb.set_clim(self.smin.val, self.smax.val)
        self.cb.set_ticks(np.linspace(self.smin.val, self.smax.val, num=10))


        # # self.cb = self.figure.colorbar(self.im)


        # self.cb.set_clim(self.smin.val, self.smax.val)
        # self.cb.on_mappable_changed(self.im)
        # self.cb.draw_all() 
        # self.cb.update_normal(self.im)
        # self.cb.update_bruteforce(self.im)
        #plt.colorbar(self.im)


def draw_opencv(image, *args, **kwargs):
    """A function with a lot of named argument to draw opencv image
     - 'point' arg must be an array of (x,y) point
     - 'p_color' arg to choose the color of point in (r,g,b) format
     - 'pointf' to draw lines between point and pointf, pointf 
     must be an array of same lenght than the point array
     - 'l_color' to choose the color of lines
     - 'grid' to display a grid, the grid must be a grid object
     - 'gr_color' to choose the grid color"""
    if type(image) == str :
         image = cv2.imread(image, 0)

    if 'text' in kwargs:
         text = kwargs['text']
         image = cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),4)

         
    frame = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if  'point' in kwargs:
        p_color = (0, 255, 255) if not 'p_color' in kwargs else kwargs['p_color']
        for pt in kwargs['point']:
            if not np.isnan(pt[0]) and not np.isnan(pt[1]):
                 x = int(pt[0])
                 y = int(pt[1])
                 frame = cv2.circle(frame, (x, y), 4, p_color, -1)

    scale = 1. if not 'scale' in kwargs else kwargs['scale']
    if 'pointf' in kwargs and 'point' in kwargs:
        assert len(kwargs['point']) == len(kwargs['pointf']), 'bad size'
        l_color = (255, 120, 255) if not 'l_color' in kwargs else kwargs['l_color']
        for i, pt0 in enumerate(kwargs['point']):
            pt1 = kwargs['pointf'][i]
            if np.isnan(pt0[0])==False and np.isnan(pt0[1])==False and np.isnan(pt1[0])==False and np.isnan(pt1[1])==False :
                 disp_x = (pt1[0]-pt0[0])*scale
                 disp_y = (pt1[1]-pt0[1])*scale
                 frame = cv2.line(frame, (int(pt0[0]), int(pt0[1])), (int(pt0[0]+disp_x), int(pt0[1]+disp_y)), l_color, 2)

    if 'grid' in kwargs:
        gr =  kwargs['grid']
        gr_color = (255, 255, 255) if not 'gr_color' in kwargs else kwargs['gr_color']
        for i in range(gr.size_x):
            for j in range(gr.size_y):
                 if (not math.isnan(gr.grid_x[i,j]) and  
                     not math.isnan(gr.grid_y[i,j]) and
                     not math.isnan(gr.disp_x[i,j]) and  
                     not math.isnan(gr.disp_y[i,j])):
                      x = int(gr.grid_x[i,j]) - int(gr.disp_x[i,j]*scale)
                      y = int(gr.grid_y[i,j]) - int(gr.disp_y[i,j]*scale)
                      
                      if i < (gr.size_x-1):
                           if (not math.isnan(gr.grid_x[i+1,j]) and  
                               not math.isnan(gr.grid_y[i+1,j]) and
                               not math.isnan(gr.disp_x[i+1,j]) and  
                               not math.isnan(gr.disp_y[i+1,j])):
                                x1 = int(gr.grid_x[i+1,j]) - int(gr.disp_x[i+1,j]*scale)
                                y1 = int(gr.grid_y[i+1,j]) - int(gr.disp_y[i+1,j]*scale)
                                frame = cv2.line(frame, (x, y), (x1, y1), gr_color, 2)

                      if j < (gr.size_y-1):
                           if (not math.isnan(gr.grid_x[i,j+1]) and  
                               not math.isnan(gr.grid_y[i,j+1]) and
                               not math.isnan(gr.disp_x[i,j+1]) and  
                               not math.isnan(gr.disp_y[i,j+1])):
                                x1 = int(gr.grid_x[i,j+1]) - int(gr.disp_x[i,j+1]*scale)
                                y1 = int(gr.grid_y[i,j+1]) - int(gr.disp_y[i,j+1]*scale)
                                frame = cv2.line(frame, (x, y), (x1, y1), gr_color, 4)
    if 'filename' in kwargs:
         cv2.imwrite( kwargs['filename'], frame)
         return

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', frame.shape[1], frame.shape[0])
    cv2.imshow('image',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  
class grid:
     """The grid class is the main class of pydic. This class embed a lot of usefull
method to treat and post-treat results"""
     
     def __init__(self, grid_x, grid_y, size_x, size_y):
          """Construct a new grid objet with x coordinate (grid_x), 
y coordinate (grid_y), number of point along x (size_x) and 
number of point along y (size_y)"""
          self.grid_x = grid_x
          self.grid_y = grid_y
          self.size_x = size_x
          self.size_y = size_y
          self.disp_x =  self.grid_x.copy().fill(0.)
          self.disp_y =  self.grid_y.copy().fill(0.)
          self.strain_xx = None
          self.strain_yy = None
          self.strain_xy = None

     def add_raw_data(self, winsize, reference_image, image, reference_point, correlated_point, disp):
          """Save raw data to the current grid object. These raw data are used as initial data 
for digital image correlation"""

          self.winsize = winsize
          self.reference_image = reference_image
          self.image = image
          self.reference_point = reference_point
          self.correlated_point = correlated_point
          self.disp = disp

     def add_meta_info(self, meta_info):
          """Save the related meta info into the current grid object"""
          self.meta_info = meta_info

     def prepare_saved_file(self, prefix, extension):
          """Not documented, for internal use only"""

          folder = os.path.dirname(self.image)
          folder = folder + '/pydic/' + prefix
          if not os.path.exists(folder):os.makedirs(folder)
          base = os.path.basename(self.image)
          name = folder + '/' + os.path.splitext(base)[0] + '_' + prefix + '.' + extension
          print("saving", name, "file...")
          return name

     def draw_marker_img(self):
          """Draw marker image"""
          name = self.prepare_saved_file('marker', 'png')
          draw_opencv(self.image, point=self.correlated_point, l_color=(0,0,255), p_color=(255,255,0), filename=name, text=name)
          
     def draw_disp_img(self, scale):
          """Draw displacement image. A scale value can be passed to amplify the displacement field"""
          name = self.prepare_saved_file('disp', 'png')
          draw_opencv(self.reference_image, point=self.reference_point, pointf=self.correlated_point, l_color=(0,0,255), p_color=(255,255,0), scale=scale, filename=name, text=name)


                    
     def draw_disp_hsv_img(self, *args, **kwargs):
          """Draw displacement image in a hsv view."""
          name = self.prepare_saved_file('disp_hsv', 'png')
          img = self.reference_image
          if type(img) == str :
               img = cv2.imread(img, 0)
          

          disp = self.correlated_point - self.reference_point          
          fx, fy = disp[:,0], disp[:,1]
          v_all = np.sqrt(fx*fx + fy*fy)
          v_max = np.mean(v_all) + 2.*np.std(v_all)

          
          rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
          hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

          if v_max != 0.:
               for i, val in enumerate(self.reference_point):
                    disp = self.correlated_point[i] - val
                    ang = np.arctan2(disp[1], disp[0]) + np.pi
                    v = np.sqrt(disp[0]**2 + disp[1]**2)
                    pt_x = int(val[0])
                    pt_y = int(val[1])

                    hsv[pt_y,pt_x, 0] = int(ang*(180/np.pi/2))
                    hsv[pt_y,pt_x, 1] = 255 if int((v/v_max)*255.) > 255 else int((v/v_max)*255.)
                    hsv[pt_y,pt_x, 2] = 255 if int((v/v_max)*255.) > 255 else int((v/v_max)*255.)


          bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
          bgr = cv2.putText(bgr, name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),4)

          if 'save_img' in kwargs:
               cv2.imwrite(name, bgr)
          if 'show_img' in kwargs:
               cv2.namedWindow('image', cv2.WINDOW_NORMAL)
               cv2.resizeWindow('image', bgr.shape[1], bgr.shape[0])
               cv2.imshow('image', bgr)
               cv2.waitKey(0)
               cv2.destroyAllWindows()




     def draw_grid_img(self, scale):
          """Draw grid image. A scale value can be passed to amplify the displacement field"""
          name = self.prepare_saved_file('grid', 'png')
          draw_opencv(self.reference_image, grid = self, scale=scale, gr_color=(255,255,250), filename=name, text=name)

     def write_result(self):
          """write a raw csv result file. Indeed, you can use your favorite tool to post-treat this file"""
          name = self.prepare_saved_file('result', 'csv')
          f = open(name, 'w')
          f.write("index" + ',' + "index_x" + ',' + "index_y" + ',' + "pos_x"    + ',' + "pos_y"    + ',' + 
                  "disp_x"    + ',' + "disp_y"    + ',' + 
                  "strain_xx" + ',' + "strain_yy" + ',' + "strain_xy" + '\n')
          index = 0
          for i in range(self.size_x):
            for j in range(self.size_y):
                 f.write(str(index)                                                 + ',' +
                         str(i)                   + ',' + str(j)                   + ',' + 
                         str(self.grid_x[i,j])    + ',' + str(self.grid_y[i,j])    + ',' + 
                         str(self.disp_x[i,j])    + ',' + str(self.disp_y[i,j])    + ',' + 
                         str(self.strain_xx[i,j]) + ',' + str(self.strain_yy[i,j]) + ',' + str(self.strain_xy[i,j]) + '\n')
                 index = index + 1
          f.close()


     def plot_field(self, field, title):
          """Plot the chosen field such as strain_xx, disp_xx, etc. in a matplotlib interactive map"""
          image_ref = cv2.imread(self.image, 0)
          Plot(image_ref, self, field, title)
          
     def interpolate_displacement(self, point, disp, *args, **kwargs):
          """Interpolate the displacement field. It allows to (i) construct the displacement grid and to 
(ii) smooth the displacement field thanks to the chosen method (raw, linear, spline,etc.)"""

          x = np.array([p[0] for p in point])
          y = np.array([p[1] for p in point])
          dx = np.array([d[0] for d in disp])
          dy = np.array([d[1] for d in disp])
          method = 'linear' if not 'method' in kwargs else kwargs['method']

          print('interpolate displacement with', method, 'method')
          if method=='delaunay':
               from scipy.interpolate import LinearNDInterpolator
               inter_x = LinearNDInterpolator(point, dx)
               inter_y = LinearNDInterpolator(point, dy)
               self.disp_x = inter_x(self.grid_x, self.grid_y)
               self.disp_y = inter_y(self.grid_x, self.grid_y)
               
          elif method=='raw':
               # need debugging
               self.disp_x = self.grid_x.copy()
               self.disp_y = self.grid_y.copy()

               assert self.disp_x.shape[0] == self.disp_y.shape[0], "bad shape"
               assert self.disp_x.shape[1] == self.disp_y.shape[1], "bad shape"
               assert len(dx) == len(dy), "bad shape"
               assert self.disp_x.shape[1]*self.disp_x.shape[0] == len(dx), "bad shape"
               count = 0
               for i in range(self.disp_x.shape[0]):
                    for j in range(self.disp_x.shape[1]):
                         self.disp_x[i,j] = dx[count]
                         self.disp_y[i,j] = dy[count]
                         count = count + 1
                         
          elif method=='spline':
               tck_x = scipy.interpolate.bisplrep(self.grid_x, self.grid_y, dx, kx=5, ky=5)
               self.disp_x = scipy.interpolate.bisplev(self.grid_x[:,0], self.grid_y[0,:],tck_x)
               
               tck_y = scipy.interpolate.bisplrep(self.grid_x, self.grid_y, dy, kx=5, ky=5)
               self.disp_y = scipy.interpolate.bisplev(self.grid_x[:,0], self.grid_y[0,:],tck_y)
               
          else:
               self.disp_x = griddata((x, y), dx, (self.grid_x, self.grid_y), method=method)
               self.disp_y = griddata((x, y), dy, (self.grid_x, self.grid_y), method=method)



     def compute_strain_field(self):
          """Compute strain field from displacement thanks to numpy"""
          #get strain fields
          dx = self.grid_x[1][0] - self.grid_x[0][0]
          dy = self.grid_y[0][1] - self.grid_y[0][0]

          
          strain_xx, strain_xy = np.gradient(self.disp_x, dx, dy, edge_order=2)
          strain_yx, strain_yy = np.gradient(self.disp_y, dx, dy, edge_order=2)

          self.strain_xx = strain_xx + .5*(np.power(strain_xx,2) + np.power(strain_yy,2))
          self.strain_yy = strain_yy + .5*(np.power(strain_xx,2) + np.power(strain_yy,2))
          self.strain_xy = .5*(strain_xy + strain_yx + strain_xx*strain_xy + strain_yx*strain_yy)
          
          
     def compute_strain_field_DA(self):
          """Compute strain field from displacement field thanks to a custom method for large strain"""
          self.strain_xx = self.disp_x.copy(); self.strain_xx.fill(np.NAN)
          self.strain_xy = self.disp_x.copy(); self.strain_xy.fill(np.NAN)
          self.strain_yy = self.disp_x.copy(); self.strain_yy.fill(np.NAN)
          self.strain_yx = self.disp_x.copy(); self.strain_yx.fill(np.NAN)

          dx = self.grid_x[1][0] - self.grid_x[0][0]
          dy = self.grid_y[0][1] - self.grid_y[0][0]

          for i in range(self.size_x):
            for j in range(self.size_y):
                 du_dx = 0.
                 dv_dy = 0. 
                 du_dy = 0.
                 dv_dx = 0.

                 if i-1 >=0 and i+1< self.size_x:
                      du1 = (self.disp_x[i+1,j] - self.disp_x[i-1,j])/2.
                      du_dx = du1/dx
                      dv2 = (self.disp_y[i+1,j] - self.disp_y[i-1,j])/2.
                      dv_dx = dv2/dx

                 if j-1>=0 and j+1 < self.size_y:
                      dv1 = (self.disp_y[i,j+1] - self.disp_y[i,j-1])/2.
                      dv_dy = dv1/dx
                      du2 = (self.disp_x[i,j+1] - self.disp_x[i,j-1])/2.
                      du_dy = du2/dy

                 self.strain_xx[i,j] = du_dx + .5*(du_dx**2 + dv_dx**2)
                 self.strain_yy[i,j] = dv_dy + .5*(du_dy**2 + dv_dy**2)
                 self.strain_xy[i,j] = .5*(du_dy + dv_dx + du_dx*du_dy + dv_dx*dv_dy)

     def compute_strain_field_log(self):
          """Compute strain field from displacement field for large strain (logarithmic strain)"""
          self.strain_xx = self.disp_x.copy(); self.strain_xx.fill(np.NAN)
          self.strain_xy = self.disp_x.copy(); self.strain_xy.fill(np.NAN)
          self.strain_yy = self.disp_x.copy(); self.strain_yy.fill(np.NAN)
          self.strain_yx = self.disp_x.copy(); self.strain_yx.fill(np.NAN)


          dx = self.grid_x[1][0] - self.grid_x[0][0]
          dy = self.grid_y[0][1] - self.grid_y[0][0]
          for i in range(self.size_x):
            for j in range(self.size_y):
                 du_dx = 0.
                 dv_dy = 0. 
                 du_dy = 0.
                 dv_dx = 0.


                 if i-1 >= 0 and i+1 < self.size_x:
                      du1 = (self.disp_x[i+1,j] - self.disp_x[i-1,j])/2.
                      du_dx = du1/dx
                      dv2 = (self.disp_y[i+1,j] - self.disp_y[i-1,j])/2.
                      dv_dx = dv2/dx
                      
                 if j-1 >= 0 and j+1 < self.size_y:
                      dv1 = (self.disp_y[i,j+1] - self.disp_y[i,j-1])/2.
                      dv_dy = dv1/dx
                      du2 = (self.disp_x[i,j+1] - self.disp_x[i,j-1])/2.
                      du_dy = du2/dy
                 t11=1+2.*du_dx+du_dx**2+dv_dx**2
                 t22=1+2.*dv_dy+dv_dy**2+du_dy**2
                 t12=du_dy+dv_dx+du_dx*du_dy+dv_dx*dv_dy
                 deflog=np.log([[t11,t12],[t12,t22]])

                 self.strain_xx[i,j] = .5*deflog[0,0]
                 self.strain_yy[i,j] = .5*deflog[1,1]
                 self.strain_xy[i,j] = .5*deflog[0,1]

     def average(self, value, x_range, y_range):
          """Get the average value in the specified x,y range of the given field"""
          val = []
          for x in x_range:
               for y in y_range:
                    if np.isnan(value[x,y]) == False:
                         val.append(value[x,y])
          return np.average(val)

     def std(self, value, x_range, y_range):
          """Get the standard deviation value in the specified x,y range of the given field"""
          val = []
          for x in x_range:
               for y in y_range:
                    if np.isnan(value[x,y]) == False:
                         val.append(value[x,y])
          return np.std(val)

