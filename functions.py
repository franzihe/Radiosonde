# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from imports import (os, sns, pd, np, plt)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def find_yx(lat, lon, point_lat, point_lon):
    abs_lat = abs(lat - point_lat)
    abs_lon = abs(lon - point_lon)

    c = np.maximum(abs_lat, abs_lon)

    y, x = np.where(c == c.min())
    y = y[0]
    x = x[0]
    
    xx = lat[y, x].x
    yy = lon[y, x].y
    return(xx, yy)


# plot style
def plot_style():
    sns.set_context('paper', font_scale=1.6)

    sns.set(font = 'Serif', font_scale = 1.6, )
    sns.set_style('ticks', 
                      {'font.family':'serif', #'font.serif':'Helvetica'
                       'grid.linestyle': '--',
                       'axes.grid': True,
                      }, 
                       )
    # Set the palette to the "pastel" default palette:
    sns.set_palette("colorblind")
plot_style()


def concat_profile_all_days(df, Date, observation, _pres, _temp, _dwpt, _xwind, _ywind):
    _lev = np.arange(1000,-25, -25)
    _averaged = pd.DataFrame()

    for i in _lev:
        filter1 = np.logical_and(df.PRES > i-25,
                                 df.PRES <= i+25 ) 
                
        _averaged = pd.concat([_averaged, df.where(filter1).mean()], axis = 1)
        _averaged = _averaged.rename(columns = {0:i})

        _averaged = _averaged.T
            
            # concat the pressure, height, temperature, dewpoint, mixing ration, wind direction, wind speed, 
            # potential temperature of all dates 
        _pres = pd.concat([_pres, _averaged.PRES], axis = 1).rename(columns = {'PRES':Date})
        _temp = pd.concat([_temp, _averaged.TEMP], axis = 1).rename(columns = {'TEMP':Date})
        _dwpt = pd.concat([_dwpt, _averaged.DWPT], axis = 1).rename(columns = {'DWPT':Date})
        _xwind = pd.concat([_xwind, _averaged.x_wind], axis = 1).rename(columns = {'x_wind':Date})
        _ywind = pd.concat([_ywind, _averaged.y_wind], axis = 1).rename(columns = {'y_wind':Date})
            
    return(_pres, _temp, _dwpt, _xwind, _ywind)


def plt_skewT(fig, skew, meps_run, p, T, Td, u, v,profile_time):
    cc = [sns.color_palette("colorblind",5)[2], 
          sns.color_palette("colorblind",5)[1],
          sns.color_palette("colorblind",5)[0]]
    
    for meps, k, xloc in zip(meps_run,cc,[0.8, 0.9, 1.]):
        
        skew.plot(p[meps][profile_time], T[meps][profile_time], color= k, label = meps)
        skew.plot(p[meps][profile_time], Td[meps][profile_time], color = k)
        skew.plot_barbs(p[meps][profile_time], u[meps][profile_time], v[meps][profile_time],color=k, xloc=xloc)

    skew.ax.set_ylim(1000, 100)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()

    # Good bounds for aspect ratio
    skew.ax.set_xlim(-35, 40)
    skew.ax.text(0.05, 1, 'Vertical profile mean - Stavanger: {} UTC'.format(profile_time), transform=skew.ax.transAxes,
                 fontsize=14, verticalalignment='bottom',)# bbox='fancy')
    plt.legend(loc = 'lower left', fancybox = True, facecolor = 'white',  title_fontsize = 16)
