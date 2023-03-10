# #%%
# import time

# import numpy as np
# import matplotlib.pyplot as plt


# def tellme(s):
#     print(s)
#     plt.title(s, fontsize=16)
#     plt.draw()


# plt.figure()
# plt.xlim(0, 1)
# plt.ylim(0, 1)

# tellme('You will define a triangle, click to begin')

# plt.waitforbuttonpress()

# while True:
#     pts = []
#     while len(pts) < 3:
#         tellme('Select 3 corners with mouse')
#         pts = np.asarray(plt.ginput(3, timeout=-1))
#         if len(pts) < 3:
#             tellme('Too few points, starting over')
#             time.sleep(1)  # Wait a second

#     ph = plt.fill(pts[:, 0], pts[:, 1], 'r', lw=2)

#     tellme('Happy? Key click for yes, mouse click for no')

#     if plt.waitforbuttonpress():
#         break

#     # Get rid of fill
#     for p in ph:
#         p.remove()

#%%[markdown]
# this is an example that select a point and plots another data set associated with that point
#
#%%

import numpy as np


class PointBrowser:
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'n'
    and 'p' keys to browse through the next and previous points
    """

    def __init__(self, axs):
        """_summary_

        Args:
            axs (list of axes objects): axis for points and for data
        """        
        self.ax = axs[0]
        self.ax2 = axs[1]
        self.lastind = 0

        self.text = self.ax.text(0.05, 0.95, 'selected: none',
                            transform=self.ax.transAxes, va='top')
        self.selected, = self.ax.plot([xs[0]], [ys[0]], 'o', ms=12, alpha=0.4,
                                 color='yellow', visible=False)

    def on_press(self, event):
        if self.lastind is None:
            return
        if event.key not in ('n', 'p'):
            return
        if event.key == 'n':
            inc = 1
        else:
            inc = -1

        self.lastind += inc
        self.lastind = np.clip(self.lastind, 0, len(xs) - 1)
        self.update()

    def on_pick(self, event):

        if event.artist != line:
            return True

        N = len(event.ind)
        if not N:
            return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata

        distances = np.hypot(x - xs[event.ind], y - ys[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None:
            return

        dataind = self.lastind

        self.ax2.clear()
        self.ax2.plot(X[dataind])

        self.ax2.text(0.05, 0.9, f'mu={xs[dataind]:1.3f}\nsigma={ys[dataind]:1.3f}',
                 transform=self.ax2.transAxes, va='top')
        self.ax2.set_ylim(-0.5, 1.5)
        self.selected.set_visible(True)
        self.selected.set_data(xs[dataind], ys[dataind])

        self.text.set_text('selected: %d' % dataind)
        fig.canvas.draw()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    X = np.random.rand(100, 200)
    xs = np.mean(X, axis=1)
    ys = np.std(X, axis=1)

    fig, (ax, ax2) = plt.subplots(2, 1)
    ax.set_title('click on point to plot time series')
    line, = ax.plot(xs, ys, 'o', picker=True, pickradius=5)

    browser = PointBrowser(axs=(ax, ax2))

    fig.canvas.mpl_connect('pick_event', browser.on_pick)
    fig.canvas.mpl_connect('key_press_event', browser.on_press)

    plt.show()