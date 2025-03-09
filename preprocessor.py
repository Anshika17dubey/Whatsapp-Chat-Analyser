import re
import pandas as pd
def preprocess(data):
    # regex pattern to extract date, time, user name, and message
    pattern = r'(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}\s?[APap][Mm]) - (.*?): (.*)'

    # Extract matching entries
    matches = re.findall(pattern, data)

    # If matches are empty, print a message and exit
    if not matches:
        print("\nNo chat messages found. Check input format or regex pattern.")
        exit()

    # Convert matches into a DataFrame
    df = pd.DataFrame(matches, columns=['date', 'time', 'user', 'msg'])

    # Convert date and time to a single datetime column
    df['date'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%y %I:%M %p')

    # Keep only required columns
    df = df[['date', 'user', 'msg']]

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()  # Extracts day of the week
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
