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

# +
# supress warnings
import warnings
warnings.filterwarnings('ignore') # don't output warnings

# import packages
from imports import (pd, np, xr, units, SkewT, mpcalc, plt,  fct)

# reload imports
# %load_ext autoreload
# %autoreload 2


# plotting cosmetics
fct.plot_style()
# -

savefig = 0
if savefig == 1:
    figdir = '/home/franzihe/Documents/Figures/Weathermast_MEPS_Retrieval/Haukeliseter/MEPS_CTRL_ICET/' 
    fct.createFolder('%s/' %figdir)
    form = 'png'

m = ['12','01', '02']
h = ['00', '12']
meps_run = [ 'CTRL', 'ICE-T', ]
meps_run.insert(0, 'OBS')

# Select col_names to be importet for the sounding plot
col_names = ['PRES', 'HGHT', 'TEMP', 'DWPT', 'MIXR', 'DRCT', 'SKNT', 'THTA']
header = np.arange(0,6)

# +
p = dict()
T = dict()
Td = dict()
u = dict()
v = dict()


_pres_meps = dict()
_temp_meps = dict()
_dwpt_meps = dict()
_xwind_meps = dict()
_ywind_meps = dict()
# -

for meps in meps_run:
    p[meps] = dict()
    T[meps] = dict()
    Td[meps] = dict()
    u[meps] = dict()
    v[meps] = dict()

# +
for hour in h:
    
    _temp = pd.DataFrame()
    _pres = pd.DataFrame()
    _hght = pd.DataFrame()
    _temp = pd.DataFrame()
    _dwpt = pd.DataFrame()
    _mixr = pd.DataFrame()
    _drct = pd.DataFrame()
    _sknt = pd.DataFrame()
    _thta = pd.DataFrame()
    _xwind = pd.DataFrame()
    _ywind = pd.DataFrame()

    for meps in meps_run:
        _pres_meps[meps] = pd.DataFrame()
        _temp_meps[meps] = pd.DataFrame()
        _dwpt_meps[meps] = pd.DataFrame()
        _xwind_meps[meps] = pd.DataFrame()
        _ywind_meps[meps] = pd.DataFrame()
    for month in m:
        if month == '12':
            t = np.array([8, 9, 10, 12, 15, 20, 21, 22, 23, 24, 25, 26, 29, 31])
        if month == '01':
            t = np.array([2, 3, 5, 6, 8, 9, 10, 11, 12, 28])
        if month == '02':
            t = np.array([2, 3, 4])    
        if month == '12':
            year = '2016'
        if month == '01' or month == '02':
            year = '2017'
        for day in t:
            if day < 10:
                day = '0%s' %day
            Date = year+month+str(day)

            stn = '01415' #1415 is ID for Stavanger
            Sounding_filename = '/home/franzihe/Documents/Data/Sounding/{}/{}{}{}_{}.txt'.format(stn,year,month,str(day),hour)


            df = pd.read_table(Sounding_filename, delim_whitespace=True, skiprows = header, \
                               usecols=[0, 1, 2, 3, 5, 6, 7, 8], names=col_names)

            ### the footer changes depending on how high the sound measured --> lines change from Radiosonde to Radiosonde
            # 1. find idx of first value matching the name 'Station'
            lines = df.index[df['PRES'].str.match('Station')]
            if len(lines) == 0:
                print('no file found: %s%s%s_%s' %(year,month,day,hour))
            else:
                # read in the Sounding files
                idx = lines[0]
                footer = np.arange((idx+header.size),220)
                skiprow = np.append(header,footer)
                df = pd.read_table(Sounding_filename, delim_whitespace=True,  skiprows = skiprow, \
                               usecols=[0, 1, 2, 3, 5, 6, 7, 8], names=col_names)
                df['x_wind'], df['y_wind'] = mpcalc.wind_components(df.SKNT.values *units.knots, df.DRCT.values*units.degrees)


                _pres, _temp, _dwpt, _xwind, _ywind = fct.concat_profile_all_days(df, Date, 'RS', _pres, _temp, _dwpt, _xwind, _ywind)



                # read in the MEPS runs
                for meps in meps_run[1:]:
                    stn = 'Stavanger'
                    meps_dirnc = '/home/franzihe/Documents/Data/MEPS/%s/%s/%s_00.nc' %(stn,meps,Date)
                    meps_f = xr.open_dataset(meps_dirnc, drop_variables ={'air_temperature_0m','liquid_water_content_of_surface_snow','rainfall_amount', 'snowfall_amount', 'graupelfall_amount', 'surface_air_pressure', 'surface_geopotential',
                                                              'precipitation_amount_acc', 'integral_of_snowfall_amount_wrt_time', 'integral_of_rainfall_amount_wrt_time',
                                                             'integral_of_graupelfall_amount_wrt_time', 'surface_snow_sublimation_amount_acc', 'air_temperature_2m','relative_humidity_2m',
                                                             'specific_humidity_2m', 'x_wind_10m', 'y_wind_10m', 'air_pressure_at_sea_level', 
                                                             'atmosphere_cloud_condensed_water_content_ml', 'atmosphere_cloud_ice_content_ml', 'atmosphere_cloud_snow_content_ml','atmosphere_cloud_rain_content_ml', 'atmosphere_cloud_graupel_content_ml',
                                                             'pressure_departure', 'layer_thickness', 'geop_layer_thickness'},
                                            ).reset_index(dims_or_levels = ['height0', 'height1', 'height3', 'height_above_msl', ], drop=True).sortby('hybrid', ascending = False)
                    # pressuer into hPa
                    meps_f['pressure_ml'] = meps_f.pressure_ml/100
                    # air temperature has to be flipped, something was wrong when reading the data from Stavanger
                    meps_f['air_temperature_ml'] = (('time', 'hybrid',),meps_f.air_temperature_ml.values[:,::-1] - 273.15)
                    meps_f['specific_humidity_ml'] = (('time', 'hybrid',),meps_f.specific_humidity_ml.values[:,::-1])
                    meps_f['x_wind_ml'] = (('time', 'hybrid',), meps_f.x_wind_ml.values[:,::-1])
                    meps_f['y_wind_ml'] = (('time', 'hybrid',), meps_f.y_wind_ml.values[:,::-1])

                    # calculate the dewpoint by first calculating the relative humidity from the specific humidity
                    meps_f['relative_humidity'] = (('time', 'hybrid', ), mpcalc.relative_humidity_from_specific_humidity(meps_f.pressure_ml.values * units.hPa, 
                                                                                      meps_f.air_temperature_ml.values * units.degC, 
                                                                                      meps_f.specific_humidity_ml.values * units('kg/kg')))

                    meps_f['DWPT'] = (('time', 'hybrid',), mpcalc.dewpoint_from_relative_humidity(meps_f.air_temperature_ml.values * units.degC, meps_f.relative_humidity))

                    if hour == '12':
                        meps_f = meps_f.isel(time = 11).to_dataframe()
                    elif hour == '00':
                        meps_f = meps_f.isel(time = 23).to_dataframe()

                    meps_f = meps_f.rename(columns = {'x_wind_ml':'x_wind', 'y_wind_ml':'y_wind', 'pressure_ml':'PRES', 'air_temperature_ml':'TEMP'})

                    _pres_meps[meps], _temp_meps[meps], _dwpt_meps[meps], _xwind_meps[meps], _ywind_meps[meps] = fct.concat_profile_all_days(meps_f, Date, 'MEPS',
                                                                                                          _pres_meps[meps], _temp_meps[meps], _dwpt_meps[meps], _xwind_meps[meps], _ywind_meps[meps])
                
                    

    ## average pressure, height, temperature, dewpoint, mixing ration, wind direction, wind speed, 
    # potential temperature over time to get seasonal mean and assign units.
    p['OBS'][hour] = _pres.mean(axis = 1, skipna=True).values * units.hPa
    T['OBS'][hour] = _temp.mean(axis = 1, skipna=True).values * units.degC
    Td['OBS'][hour] = _dwpt.mean(axis = 1, skipna=True).values * units.degC
    u['OBS'][hour] = _xwind.mean(axis = 1, skipna = True)
    v['OBS'][hour] = _ywind.mean(axis = 1, skipna = True)

    for meps in meps_run[1:]:
        p[meps][hour] = _pres_meps[meps].mean(axis = 1, skipna=True).values * units.hPa
        T[meps][hour] = _temp_meps[meps].mean(axis = 1, skipna=True).values * units.degC
        Td[meps][hour] = _dwpt_meps[meps].mean(axis = 1, skipna=True).values * units.degC
        u[meps][hour] = _xwind_meps[meps].mean(axis = 1, skipna = True)
        v[meps][hour] = _ywind_meps[meps].mean(axis = 1, skipna = True)


# -

fig_label = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)', 'g)', 'h)', 'i)', 'j)', 'k)', 'l)', 'm)']

# +
fig = plt.figure(figsize=(18, 9))

#plot skewT for 00UTC 
skew = SkewT(fig, rotation=45,subplot=121)
fct.plt_skewT(fig, skew, meps_run, p, T, Td, u, v,'00')
skew.ax.text(0.03, 0.95,
                    fig_label[0],
                    fontweight='bold',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform = skew.ax.transAxes)


#plot skewT for 12UTC
skew = SkewT(fig, rotation=45,subplot=122)
fct.plt_skewT(fig, skew, meps_run, p, T, Td, u, v,'12')
skew.ax.text(0.03, 0.95,
                    fig_label[1],
                    fontweight='bold',
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform = skew.ax.transAxes)

if savefig == 1:
        fct.createFolder('%s/' %(figdir))
        fig_name = 'winter_16_17_vertical_profile.'+form
        plt.savefig('%s/%s' %(figdir, fig_name), format = form, bbox_inches='tight', transparent=True)
        print('plot saved: %s/%s' %(figdir, fig_name))
        plt.close()
# -


