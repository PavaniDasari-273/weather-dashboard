import streamlit as st 
import requests
import datetime
import matplotlib.pyplot as plt

def get_weather(city,api_key):
    url=f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    response=requests.get(url)
    if response==200:
        return response.json()
    else:
        return None
    
def get_historical_weather(city,api_key,days):
            historical_data={}
            for i in range(days):
                date=(datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                url=f"http://api.weatherstack.com/historical?access_key={api_key}&query={city}&historical_date={date}"
                response=requests.get(url)
                data=response.json()
                if "historical"in data and date in data["historical"]:
                    historical_data[date]=data["historical"][date]["temperature"]
                else:
                    historical_data[date]=20+i
                    print("historical data retrived:",historical_data)
            return historical_data
    
    

def plot_temperature_trend(today_temp,historical_data):
    dates=list(historical_data.keys())[::-1]+["today"]
    temperatures=list(historical_data.values())[::-1]+["today_temp"]
    
    plt.figure(figsize=(8,4))
    plt.plot(dates,temperatures,marker="0",linestyle="_",color='b')
    plt.xlabel("data")
    plt.ylabel("avg temperature(°C)")
    plt.title("temperature trend.last week& today")
    plt.xticks(rotation=45)
    plt.grid()
    st.plyplot(plt)
    def main():
        st.title("REAL TIME WEATHER MONITORING DASHBOARD")
        st.sidebar.header("settings")
        city=st.sidebar.text_input("enter city name","newyork")
        api_key="0e45feb92664671b1a36fd6b918bbb5d"
        if st.sidebar.button("get weather"):
          weather_data=get_weather(city,api_key)
          historical_data=get_weather(city,api_key,7)
          
          if weather_data and "current" in weather_data:
              st.subheader(f"current weather in {city}")
              today_temp=weather_data["current"]["temperature"]
              st.metric(label="temperature(°C)",value=f"{today_temp} °C")
              st.metric(label="humidity(%)",value=f"{weather_data['current']['humidity']} %")
              st.metric(label="wind speed(km/h)",value=f"{weather_data['current']['wind_speed']} km/h")
              st.write(f"**weather condition:** {weather_data['current']['weather_descriptions'][0]}")
              st.write(f"**observation time:** {weather_data['current']['observation_time']}")
              
              st.balloons()
              st.snowflake()
              st.sucess("weather_data retrived sucessfully")
              if historical_data:
                  st.subheader("temperature trend:last week & today")
                  plot_temperature_trend(today_temp, historical_data)
              else:
                st.error("failed to retrive weather data. check city name or api key")
                if __name__=="__main__":
                    main()
  