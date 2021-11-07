from OpenPivParams import OpenPivParams
import pandas as pd
import matplotlib.pyplot as plt

class DataReader():

  def __init__(self):
    self.p = OpenPivParams()

  def load_pandas(self, fname):
      """
          Load files in a pandas data frame.

          On the rider named General, the parameters for loading
          the data frames can be specified.
          No parameters have to be set for image processing.

          Parameters
          ----------
          fname :
              A filename.

          Returns
          -------
          pandas.DataFrame :
              In case of an error, the errormessage is returned (str).
      """
      sep = self.p['sep']
      if sep == 'tab':
          sep = '\t'
      if sep == 'space':
          sep = ' '

      ext = fname.split('.')[-1]
      if ext in ['txt', 'dat', 'jvc', 'vec', 'csv']:
          if self.p['load_settings']:
              print('loaded')
              if self.p['header']:
                  data = pd.read_csv(fname,
                                      decimal=self.p['decimal'],
                                      skiprows=int(self.p['skiprows']),
                                      sep=sep)
              elif not self.p['header']:
                  data = pd.read_csv(fname,
                                      decimal=self.p['decimal'],
                                      skiprows=int(self.p['skiprows']),
                                      sep=sep,
                                      header=0,
                                      names=self.p['header_names'].split(','))
          else:
              print('default')
              data = pd.read_csv(fname,
                                  decimal=',',
                                  skiprows=0,
                                  sep='\t',
                                  names=['x', 'y', 'vx', 'vy', 'sig2noise'])
      else:
          data = 'File could not be read. Possibly it is an image file.'
      return data

def contour(data, parameter, figure):
    '''Display a contour plot
    Parameters
    ----------
    data : pandas.DataFrame
        Data to plot.
    parameter : openpivgui.OpenPivParams.py
        Parameter-object.
    figure : matplotlib.figure.Figure
       An (empty) Figure object.
    '''
    # figure for subplot
    ax = figure.add_subplot(111)
    # iteration to set value types to float
    for i in list(data.columns.values):
        data[i] = data[i].astype(float)
    # choosing velocity for the colormap and add it to an new colummn in data
    if parameter['velocity_color'] == 'vx':
        data['abs'] = data.u
    elif parameter['velocity_color'] == 'vy':
        data['abs'] = data.v
    else:
        data['abs'] = (data.u**2 + data.v**2)**0.5
    # pivot table for contour function
    data_pivot = data.pivot(index='y',
                            columns='x',
                            values='abs')
    # try to get limits, if not possible set to None
    try:
        vmin = float(parameter['vmin'])
    except BaseException:
        vmin = None
    try:
        vmax = float(parameter['vmax'])
    except BaseException:
        vmax = None
    # settings for color scheme of the contour plot
    if vmax is not None and vmin is not None:
        levels = np.linspace(vmin, vmax, int(parameter['color_levels']))
    elif vmax is not None:
        levels = np.linspace(0, vmax, int(parameter['color_levels']))
    elif vmin is not None:
        vmax = data_pivot.max().max()
        levels = np.linspace(vmin, vmax, int(parameter['color_levels']))
    else:
        levels = int(parameter['color_levels'])
    # Choosing the correct colormap
    if parameter['color_map'] == 'short rainbow':
        colormap = short_rainbow
    elif parameter['color_map'] == 'long rainbow':
        colormap = long_rainbow
    else:
        colormap = parameter['color_map']
    # set contour plot to the variable fig to add a colorbar
    if parameter['extend_cbar']:
        extend = 'both'
    else:
        extend = None
    fig = ax.contourf(data_pivot.columns,
                      data_pivot.index,
                      data_pivot.values,
                      levels=levels,
                      cmap=colormap,
                      vmin=vmin,
                      vmax=vmax,
                      extend=extend)

    # set the colorbar to the variable cb to add a description
    cb = plt.colorbar(fig, ax=ax)

    # set origin to top left or bottom left
    if parameter['invert_yaxis']:
        ax.set_ylim(ax.get_ylim()[::-1])

    # description to the contour lines
    cb.ax.set_ylabel('Velocity [m/s]')

    # labels for the axes
    ax.set_xlabel('x-position')
    ax.set_ylabel('y-position')

    # plot title from the GUI
    ax.set_title(parameter['plot_title'])

    figure.savefig('contour.jpeg')
