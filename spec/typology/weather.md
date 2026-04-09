# Weather [Data → State, of a Site or area]

[enum] PrecipitationType:
- None
- Rain
- Snow
- Sleet
- Hail
- FreezingRain
- Drizzle

[enum] CloudCover:
- Clear
- Few
- Scattered
- Broken
- Overcast

[enum] IcingIntensity:
- None
- Light
- Moderate
- Severe

[enum] TurbulenceIntensity:
- None
- Light
- Moderate
- Severe
- Extreme

[enum] FlightCategory:
- VFR
- MVFR
- IFR
- LIFR

[enum] WeatherSource:
- METAR
- TAF
- PIREP
- SIGMET
- AIRMET
- Radar
- Satellite
- ModelForecast

[enum] WeatherHazardType:
- Thunderstorm
- Icing
- Turbulence
- Fog
- Dust
- VolcanicAsh
- Windshear
- Sandstorm

WeatherCondition [facets]:
- temperature + unit
- wind (speed, gust, direction)
- pressure + unit
- humidity
- visibility + unit
- precipitation type + rate
- cloud coverage + ceiling + layers
- dew point
- icing intensity + altitude range
- turbulence intensity

