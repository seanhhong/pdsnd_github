#bike share project for udacity nano degree program

import time
import pandas as pd
import numpy as np
pd.options.display.max_columns = None
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Please enter the name of city you would like to explore (chicago, new york city, washington): ')
            CITY_DATA[city.lower()]
            break
        except:
            print('please enter a vaild city from following: chicago, new york city, washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please enter a month of interest from January to June (or all to see all the months): ')
            month = months.index(month.lower())
            break
        except:
            print('Please enter a vaild month from January to June (ex. january)')

    while True:
    # get user input for day of week (all, monday, tuesday, ... sunday)
        try:
            day = input('Please enter a day of week of interest (or all to see all the days): ')
            day = days.index(day.lower())
            break
        except:
            print('Please enter a valid day of week (ex. monday)')


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    if month != 0:
        df = df[df['month'] == month]

    if day != 7:
        df = df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    print('Most popular month is {}'.format(months[pop_month].title()))

    # display the most common day of week
    pop_dow = df['day_of_week'].mode()[0]
    print('Most popular day is {}'.format(days[pop_dow].title()))

    # display the most common start hour
    pop_hour = df['hour'].mode()[0]
    print('Most popular hour is {}:00'.format(pop_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station is {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most popular end station is {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    start_end = []
    for start, end in zip(df['Start Station'], df['End Station']):
        start_end.append(start + ' to ' + end)
    df['Start End'] = start_end
    print('Most popular trip is {}'.format(df['Start End'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def sec_to_minute_hour(sec):
    if sec//60 != 0:
        min = int(sec//60)
        sec = int(sec%60)
        if min//60 != 0:
            hour = int(min//60)
            min = min%60
            return '{} hours {} minutes {} seconds'.format(hour, min, sec)
        else:
            return '{} minutes {} seconds'.format(min, sec)
    else:
        return '{} seconds'.format(sec)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time is ' + sec_to_minute_hour(df['Trip Duration'].sum()))

    # display mean travel time
    print('average travel time is ' + sec_to_minute_hour(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Following is the list of user type: ')
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    print('\nFollowing is the list of gender: ')
    try:
        print(df['Gender'].value_counts().to_string())
    except KeyError:
        print('There is no Gender information.')

    # Display earliest, most recent, and most common year of birth
    print('\nFollowing is birth year information: ')
    try:
        bd_count_max = df['Birth Year'].value_counts().idxmax()
        bd_sort = df['Birth Year'].value_counts().sort_index().index
        print('Most common birth year is {}'.format(int(bd_count_max)))
        print('Oldest birth year is {}'.format(int(bd_sort[0])))
        print('Youngest birth year is {}'.format(int(bd_sort[-1])))
    except KeyError:
        print('There is no birth year information.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw(df):
    n = 5 #multiple factor
    flag = input('Would you like to see raw data? Enter yes or no.\n')
    if flag.lower() != 'yes':
        return
    i = n
    while i <= len(df.index):
        print(df.iloc[i-n:i])
        i = i + n
        flag = input('Would you like to see {} more lines of raw data? Enter yes or no.\n'.format(n))
        if flag.lower () != 'yes':
            return
    if i != len(df.index) + n:
        print(df.iloc[i-n:])
        print('End of raw data.')
    else:
        print('End of raw data.')

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head(10))
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
