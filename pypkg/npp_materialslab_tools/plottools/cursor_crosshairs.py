class Cursor():
    def __init__(self, ax, ID, x, y, indx):
        '''
        '''
        self.ID = ID
        self.ax = ax # make cursor aware of the ax that's been plotted to. 
        self.x = x
        self.y = y
        self.indx = indx
        # defaults
        self.col = 'k'
        self._linestyle = 'dashed'

    def __str__(self):
        return "ID:{}, (x:{}, y:{}) @ ind:{}".format(self.ID, self.x, self.y, self.indx)

    def plot_cursor(self, new = True):
        ''' Plots a cursor 
        '''
        if new:
            self.lx = self.ax.axhline(self.y, color=self.col, linestyle=self._linestyle)  # the horiz line
            self.ly = self.ax.axvline(self.x, color=self.col, linestyle=self._linestyle)  # the vert line
        else:
            self.lx.set_ydata(self.y)
            self.ly.set_xdata(self.x)

    def remove_line(self):
            self.ax.lines.remove(self.lx)
            self.ax.lines.remove(self.ly)        
            self.lx = None
            self.ly = None


