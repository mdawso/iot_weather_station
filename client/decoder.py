def wind_direction(weather_data):
    return int(weather_data[2:5])

def wind_speed_average(weather_data):
    return 0.44704 * int(weather_data[6:9])

def wind_speed_max(weather_data):
    return 0.44704 * int(weather_data[10:13])

def temperature(weather_data):
    temp = int(weather_data[14:17])
    if weather_data[14] == '-':
        temp = -temp
    return (temp - 32) * 5.0 / 9.0

def rainfall_one_hour(weather_data):
    return int(weather_data[18:21]) * 25.40 * 0.01

def rainfall_one_day(weather_data):
    return int(weather_data[22:25]) * 25.40 * 0.01

def humidity(weather_data):
    return int(weather_data[26:28])

def barometric_pressure(weather_data):
    return int(weather_data[29:34]) / 10.0

def debug_print(weather_data):
    print(f"Wind Direction: {wind_direction(weather_data)} °")
    print(f"Average Wind Speed (One Minute): {wind_speed_average(weather_data):.2f} m/s")
    print(f"Max Wind Speed (Five Minutes): {wind_speed_max(weather_data):.2f} m/s")
    print(f"Rainfall (One Hour): {rainfall_one_hour(weather_data):.2f} mm")
    print(f"Rainfall (24 Hours): {rainfall_one_day(weather_data):.2f} mm")
    print(f"Temperature: {temperature(weather_data):.2f} °C")
    print(f"Humidity: {humidity(weather_data)} %")
    print(f"Barometric Pressure: {barometric_pressure(weather_data):.1f} hPa")

