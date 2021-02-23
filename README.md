# Weathermap from MEPS latest runs
... can be adjusted to the archived forecasts:

- MEPS latest: https://thredds.met.no/thredds/catalog/mepslatest/catalog.html
- MEPS archive: https://thredds.met.no/thredds/catalog/meps25epsarchive/catalog.html

- AROME Arctic latest: https://thredds.met.no/thredds/catalog/aromearcticlatest/catalog.html
- AROME Arctic archive: https://thredds.met.no/thredds/catalog/aromearcticarchive/catalog.html

## HOW TO CITE
Hellmuth, Franziska, Hofer, Stefan (2019), Weathermaps from MEPS latest runs, University of Oslo, Oslo, Norway. Contact: franziska.hellmuth@geo.uio.no


## Necessary Python 3.7 packages
- jupyter
- jupyterlab
- numpy
- pandas
- matplotlib
- basemap
- netcdf4
- xarray
- cartopy


## Weathermaps created:
### 700hPa humidity
Needed variables from the Met-NO files:
- geopotential_pl
- air_temperature_pl
- relative_humidity_pl

### Jet-Thickness-MSLP
Needed variables from the Met-NO files:
- x_wind_pl
- y_wind_pl
- air_pressure_at_sea_level
- lwe_thickness_of_atmosphere_mass_content_of_water_vapor

### 850hP-Temperature-Wind
Needed variables from the Met-NO files:
- air_temperature_pl
- x_wind_pl
- y_wind_pl
