def trans_char_to_int(data, start, stop):
    result = 0
    for i in range(start, stop + 1):
        result = result * 10 + (ord(data[i]) - ord('0'))
    return result

def trans_char_to_int_t(data):
    # Special conversion for temperatures
    if data[13] == '-':
        return -1 * ((ord(data[14]) - ord('0')) * 10 + (ord(data[15]) - ord('0')))
    else:
        return ((ord(data[13]) - ord('0')) * 100 + (ord(data[14]) - ord('0')) * 10 + (ord(data[15]) - ord('0')))

def wind_direction(data):
    return trans_char_to_int(data, 1, 3)

def wind_speed_average(data):
    return 0.44704 * trans_char_to_int(data, 5, 7)

def wind_speed_max(data):
    return 0.44704 * trans_char_to_int(data, 9, 11)

def temperature(data):
    temp_f = trans_char_to_int_t(data)
    return (temp_f - 32.00) * 5.00 / 9.00

def rainfall_one_hour(data):
    return trans_char_to_int(data, 17, 19) * 25.40 * 0.01

def rainfall_one_day(data):
    return trans_char_to_int(data, 21, 23) * 25.40 * 0.01

def humidity(data):
    return trans_char_to_int(data, 25, 26)

def barometric_pressure(data):
    return trans_char_to_int(data, 28, 32) / 10.0

def debug_print(weather_data):
    print(f"Wind Direction: {wind_direction(weather_data)} °")
    print(f"Average Wind Speed (One Minute): {wind_speed_average(weather_data):.2f} m/s")
    print(f"Max Wind Speed (Five Minutes): {wind_speed_max(weather_data):.2f} m/s")
    print(f"Rainfall (One Hour): {rainfall_one_hour(weather_data):.2f} mm")
    print(f"Rainfall (24 Hours): {rainfall_one_day(weather_data):.2f} mm")
    print(f"Temperature: {temperature(weather_data):.2f} °C")
    print(f"Humidity: {humidity(weather_data)} %")
    print(f"Barometric Pressure: {barometric_pressure(weather_data):.1f} hPa")

