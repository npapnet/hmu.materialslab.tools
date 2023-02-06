import numpy as np
import matplotlib.pyplot as plt

import logging

logging.basicConfig(level=logging.DEBUG)

class PointSelector:
    """
    Select one point  and highlight it.
    Use the 'n' and 'p' keys to browse through the next and previous points
    """

    def __init__(self, fig:plt.figure, ax:plt.Axes, attach_event_callbacks:bool=True):
        """constructs the object

        Args:
            ax (ax object): it assumes that there is one line in it
        """      
        self._fig = fig   
        self._ax = ax

        #select the line and get the xy data from the 
        self._line = self._ax.lines[0]
        self.xs = self._line.get_xdata()
        self.ys = self._line.get_ydata()


        self.lastind = 0

        self.text = self._ax.text(0.05, 0.95, 'selected: none',
                            transform=self._ax.transAxes, va='top')
        self.selected, = self._ax.plot([self.xs[0]], [self.ys[0]], 'o', ms=12, alpha=0.4,
                                 color='yellow', visible=False)

        if attach_event_callbacks:
            self.attach_event_callbacks()

    @property
    def x_selected(self)->float:
        """returns x coordinate

        Returns:
            float: x coordinate
        """        
        return self.xs[self.lastind]

    @property
    def y_selected(self)->float:
        """returns y coordinate

        Returns:
            float: y coordinate
        """        
        return self.ys[self.lastind]
    
    @property
    def xy_selected(self)->tuple:
        """returns (x,y) tuple

        Returns:
            tuple: xy data
        """        
        return (self.xs[self.lastind], self.ys[self.lastind])

    @property
    def selected_index(self)->int:
        """returns selected index

        Returns:
            int: select index
        """        
        return self.lastind


    def attach_event_callbacks(self):
        """attaches the event callback on the figure object
        """        
        self._fig.canvas.mpl_connect('pick_event', self.on_pick)
        self._fig.canvas.mpl_connect('key_press_event', self.on_keypress)

    def on_keypress(self, event):
        if self.lastind is None:
            return
        if event.key not in ('n', 'p'):
            return
        if event.key == 'n':
            inc = 1
        else:
            inc = -1

        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(self.xs) - 1)
        self.update()

    def on_pick(self, event):

        if event.artist != self._line:
            return True

        N = len(event.ind)
        if not N:
            return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        distances = np.hypot(x - self.xs[event.ind], y - self.ys[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None:
            return

        dataind = self.lastind

        self.selected.set_visible(True)
        self.selected.set_data(self.xs[dataind], self.ys[dataind])
        logging.debug(f'x:{self.xs[dataind]}, y:{ self.ys[dataind]}')
        self.text.set_text(f'selected: {dataind}' )
        self._fig.canvas.draw()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # Fixing random state for reproducibility

    xs = np.linspace(0, 2*np.pi,100)
    ys = np.sin(xs)

    fig2, ax = plt.subplots(1, 1)
    ax.set_title('click on point to plot time series')
    line, = ax.plot(xs, ys, 'o', picker=True, pickradius=5)

    browser = PointSelector(fig=fig2, ax=(ax))

    plt.show()