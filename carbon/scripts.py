from entsoe import EntsoePandasClient
import pandas as pd
from sklearn.externals import joblib
import forecastio as fc
from datetime import timedelta, date, datetime
import datetime 
from .models import Forecasts

today = datetime.date.today()
yesterday = today - datetime.timedelta(days = 1)
tomorrow = today + datetime.timedelta(days = 1) 
aftertomorrow = tomorrow + datetime.timedelta(days = 1) 
api_key = "a7e978b04b8d30ec9f1f52a8e4cd4c5f"
lat = 51.1657
lng = 10.018343

# This class works as a service layer by retrieving the needed data from ENTSOE and DARKSKY APIs and
# applying the needed data engineering steps then forecasts the CO2 emissions using the provided model
class scripts(object):
    """docstring for ClassName"""
    def __init__(self):
        super(scripts, self).__init__()

    # function to multiply all values to 0.25 to make the generation MWh and then to 1000 to get it from MWh to kWh
    def kwh (self, ts):
        #to kwh
        ts_mwh = ts.multiply(0.25)
        ts_kwh = ts_mwh * 1000
        return ts_kwh

    # function to retrieve the electricity generation forecasts for one-day-ahead in Germany
    def entsoe (self):
        client = EntsoePandasClient(api_key='5aa63adb-f9f7-47aa-8053-5cf531a3743f')
        start = pd.Timestamp(tomorrow, tz='Europe/Berlin')
        end = pd.Timestamp(aftertomorrow, tz='Europe/Berlin')
        country_code = 'DE'
        df = client.query_wind_and_solar_forecast(country_code, start=start, end=end, psr_type=None)
        df1 = client.query_generation_forecast(country_code, start=start, end=end )
    
        df = self.kwh(df)
        df['hour']=df.index.hour
        df['date']=df.index.date
        df['weekDay']=df.index.dayofweek
        df['month']=df.index.month
        dfgroup = df.groupby(['date','hour']).agg({ 'Solar':'sum', 'Wind Offshore':'sum' ,'Wind Onshore':'sum' ,'weekDay':'max', 'month':'max'})
    
    
        df2 = pd.DataFrame(data=df1)
        df2['hour']=df2.index.hour
        df2['date']=df2.index.date
        df1group = df2.groupby(['date','hour']).sum()
        df1group = df1group * 1000
        df1group.rename(columns={0:'Generation'}, inplace=True)
    
        result = pd.concat([df1group,dfgroup], axis=1)
        idx = result.index
        result.index = result.index.set_levels([idx.get_level_values('date').astype(str), idx.get_level_values('hour')])
    
        return result
    


    # function to retrieve the weather condition forecasts in Germany
    def weather(self):
        daydf = pd.DataFrame()
        forecast = fc.load_forecast(api_key, lat, lng)
        byHour = forecast.hourly()
        x=0
        for hourlyData in byHour.data:
            weatherdf = pd.DataFrame.from_dict(hourlyData.d, orient='index')
            weatherdf = weatherdf.T
            weatherdf['date'] = '' + str(tomorrow)
            weatherdf['hour'] = x
            daydf = daydf.append(weatherdf,ignore_index=True)
            x = x+1
        daydf = daydf.set_index(['date', 'hour'])
    
        return daydf

    # function that uses the retrieved data to forecast the CO2 emissions in Germany using the provided model.pkl
    def prediction(self):
        allForecasts = Forecasts.objects.all()
        if len(allForecasts) > 1:
            return allForecasts
        try:
            X = self.entsoe()
            Y = self.weather()
        except Exception as err:
            print("Energy Forecasts are not available.")
            return Forecasts.objects.all()
        #print(tomorrow)
        result = pd.concat([X,Y], axis=1)
        final = result[['Solar','Wind Onshore','weekDay','month','Generation','windSpeed']]
        final = final.dropna(axis='index',how ='any')
        ols = joblib.load('model.pkl')
        pred = ols.predict(final)
        i = 0
        for one in pred:
            b = Forecasts(hour=i , co2 =one)
            b.save()
            i=i+1

        return Forecasts.objects.all()
    # function to empty the forecasts table in the data base and it is used by the updater (scheduler)
    def emptyForecasts(self):
        Forecasts.objects.all().delete()





