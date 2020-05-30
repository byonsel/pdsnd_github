import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
CITY_MATCH = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}
MONTH_MATCH = {'jan': [1,'January'], 'feb': [2,'February'], 'mar': [3,'March'], 'apr': [4,'April'], 'may': [5,'May'], 'jun': [6,'Jun'], 'all': [-1,'all']}
DAY_MATCH = {'mon': [0,'Monday'], 'tue': [1,'Tuesday'], 'wed': [2,'Wednesday'], 'thu': [3,'Thursday'], 'fri': [4,'Friday'], 'sat': [5,'Saturday'], 'sun': [6,'Sunday'], 'all': [-1,'all']}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please specify a city to analyze.')
    city_init = input('Enter n for New York, c for Chicago, w for Washington DC:\n').lower()
    while city_init not in CITY_MATCH:
        print('\nPlease enter a valid input')
        city_init = input('Enter n for New York, c for Chicago, w for Washington DC:\n').lower()

    city = (CITY_MATCH[city_init])
    print('-'*40)

    # TO DO: get user input for month (all, january, february, ... , june)
    print('\nNow, please specify a month to analyze.')
    month_init = input('Enter "jan" or "feb" or "mar" or "apr" or "may" or "jun" or "all" for all 6 months \n').lower()
    while month_init not in MONTH_MATCH:
        print('\nPlease enter a valid input')
        month_init = input('Enter "jan" or "feb" or "mar" or "apr" or "may" or "jun" or "all" for all 6 months \n').lower()

    month = (MONTH_MATCH[month_init][1])
    print('-'*40)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nLastly, please specify a day to analyze.')
    day_init = input('Enter "mon" or "tue" or "wed" or "thu" or "fri" or "sat" or "sun" or "all" for all the days\n').lower()
    while day_init not in DAY_MATCH:
        print('\nPlease enter a valid input')
        day_init = input('Enter "mon" or "tue" or "wed" or "thu" or "fri" or "sat" or "sun" or "all" for all the days\n').lower()

    day = (DAY_MATCH[day_init][1])

    print('-'*40)
    print('\nResults will be calculated for:\nCity  : {}\nMonth : {}\nDay   : {}'.format(city.title(), month.title(), day.title()))
    print('-'*40)

    return city, month, day

def load_data(city, month, day):

    file_name = CITY_DATA[city]

    df = pd.read_csv(file_name)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        df = df[df['Month'] == MONTH_MATCH[month[0:3].lower()][0]]

    if day != 'all':
        df = df[df['Day_of_Week'] == DAY_MATCH[day[0:3].lower()][0]]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    MONTH_NAMES = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June' }
    DAY_NAMES = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = MONTH_NAMES[df['Month'].mode()[0]]
    print('The most common month is : {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = DAY_NAMES[df['Day_of_Week'].mode()[0]]
    print('The most common day   is : {}'.format(common_day))

    # TO DO: display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('The most common hour  is : {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is : {}'.format(common_start_station))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end   station is : {}'.format(common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    gr = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    station = gr.head(1)
    print('The most common combination   is :')
    print(station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*20)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_secs = df['Trip Duration'].sum()
    total_days = total_secs // 86400
    rem_secs = int(total_secs % 86400)
    rem_time = str(datetime.timedelta(seconds=rem_secs))

    print('The total   trip duration is : {} days and {}'.format(total_days,rem_time))

    # TO DO: display mean travel time
    mean_dur = int(df['Trip Duration'].mean())
    mean_time = str(datetime.timedelta(seconds=mean_dur))
    print('The avarage trip duration is : {} '.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The count of user types :\n{}'.format(df['User Type'].value_counts()))

    if city != 'washington':
        # TO DO: Display counts of gender
        print('\nThe count of gender types :\n{}'.format(df['Gender'].value_counts()))

        # TO DO: Display earliest, most recent, and most common year of birth
        min_by = int(df['Birth Year'].min())
        max_by = int(df['Birth Year'].max())
        com_by = int(df['Birth Year'].mode()[0])

        print('\nThe    earliest year of birth is: {}'.format(min_by))
        print('The most recent year of birth is: {}'.format(max_by))
        print('The most common year of birth is: {}'.format(com_by))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_reply():
    reply = input('\nWould you like to display 5 rows of raw data? Enter yes or no.\n')
    while reply.lower() not in ['yes','no']:
        print('\nPlease answer as yes or no')
        reply = input('Would you like to display 5 rows of raw data? Enter yes or no.\n')

    return reply

def display_raw_data(df, city):
    answer = get_reply()
    i = 0
    j = 5
    while answer == 'yes':
        while i < j and i < len(df):
            print('      Record# : {}'.format(i))
            print('   Start Time : {}'.format(df.iloc[i,1]))
            print('     End Time : {}'.format(df.iloc[i,2]))
            print('Trip Duration : {}'.format(df.iloc[i,3]))
            print('Start Station : {}'.format(df.iloc[i,4]))
            print('  End Station : {}'.format(df.iloc[i,5]))
            print('    User Type : {}'.format(df.iloc[i,6]))
            if city != 'washington':
                print('       Gender : {}'.format(df.iloc[i,7]))
                print('   Birth Year : {}'.format(df.iloc[i,8]))
            print('-'*40)
            i += 1
        j += 5
        answer = get_reply()
    print('-'*20)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
