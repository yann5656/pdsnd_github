import time
import pandas as pd
import numpy as np
import calendar

#used bikeshare data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    print('Following cities are available for analysis: ')
    for city in CITY_DATA.keys():
        print('-', city.title())

    while(True):
        city = input('\n>please select a city: ')
        if(CITY_DATA.get(city.lower())):
            break
        else:
            print('oops, no data available for: ',city.title())

    print('ok, {} selected'.format(city.title()))


    # get user input for month (all, january, february, ... , june)
    while(True):
        month = input("\n>please enter a month [1-6] or press [Enter] to select none: ")
        if(len(month)==0):
            print('ok, ALL months selected')
            break
        elif(0 <= int(month) < 7):
                break
        else:
            print('oops, invalid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        day = input(">please enter a day [0-6] or press [Enter] to select none: [0=Monday, 1=Tuesday 2=Wednesday 3=Thursday 4=Friday, 5=Saturday 6=Sunday] ")
        if(len(day)==0):
            print('ok, ALL days selected')
            break
        elif(0 <= int(day) < 8):
            break
        else:
            print('oops, invalid day')

    print('-'*40)
    return city.lower(), month, day


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
    info = 'reading database for \'{}\''.format(city.title())
    if(len(month) or len(day)):
        info += ' filtered by: '
    if(len(month)):
        info += ' month={} ({})'.format(calendar.month_name[int(month)], month)
    if(len(day)):
        info += ' day={} ({})'.format(calendar.day_name[int(day)], day)
    print(info)

    df = pd.read_csv(CITY_DATA[city])

    #add columns (month, day, dayweek) https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['weekday'] = pd.DatetimeIndex(df['Start Time']).weekday
    df['start_hour'] = pd.DatetimeIndex(df['Start Time']).hour

    if(len(month) and len(day)):
        return df[(df['weekday'] == int(day)) & (df['month'] == int(month))]
    elif(len(month)):
        return df[df['month'] == int(month)]
    elif(len(day)):
        return df[df['weekday'] == int(day)]
    else:
        return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel.
    Inputs:
        df      : DataFrame with possibly filtered database
        month   : possible month filter (if avail, do not search for max month)
        day     : possible day filter   (if avail, do not search for day month)
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if(len(month)==0):
        mc_month_maxevts = df.groupby(['month'])['Start Time'].count().max()
        mc_month = df.groupby(['month'])['Start Time'].count().idxmax()
        print('\tThe rentings happen mostly in month: {} ({} events)'.format(mc_month, mc_month_maxevts))


    # display the most common day of week
    if(len(day)==0):
        mc_weekday_maxevts = df.groupby(['weekday'])['Start Time'].count().max()
        mc_weekday = df.groupby(['weekday'])['Start Time'].count().idxmax()
        print('\tThe rentings happen mostly on weekday: {} ({}) ({} events)'.format(mc_weekday, calendar.day_name[int(mc_weekday)], mc_weekday_maxevts))

    # display the most common start hour
    mc_start_hr_maxevts = df.groupby(['start_hour'])['Start Time'].count().max()
    mc_start_hr = df.groupby(['start_hour'])['Start Time'].count().idxmax()
    print('\tThe rentings start mostly between: {}:00 and {}:00 ({} events)'.format(mc_start_hr, mc_start_hr +1, mc_start_hr_maxevts))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('\t The rentings')
    # display most commonly used start station
    mp_start_station_maxevts = df.groupby(['Start Station'])['Start Time'].count().max()
    mp_start_station_name = df.groupby(['Start Station'])['Start Time'].count().idxmax()
    print('\t -start mostly in station: \'{}\' ({} events)'.format(mp_start_station_name, mp_start_station_maxevts))


    # display most commonly used end station
    mp_end_station_maxevts = df.groupby(['End Station'])['Start Time'].count().max()
    mp_end_station_name = df.groupby(['End Station'])['Start Time'].count().idxmax()
    print('\t -end mostly in station: \'{}\' ({} events)'.format(mp_end_station_name, mp_end_station_maxevts))

    # display most frequent combination of start station and end station trip
    mp_trip_maxevts = df.groupby(['Start Station','End Station'])['Start Time'].count().max()
    mp_trip_name = df.groupby(['Start Station','End Station'])['Start Time'].count().idxmax()
    print('\t The most frequent trip is: \'{}\' to \'{}\' ({} times)'.format(mp_trip_name[0],mp_trip_name[1], mp_trip_maxevts))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print('\ttotal travel time: ', display_time(tot_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\tmean travel time: ', display_time(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df['User Type'] = df['User Type'].fillna("<no data avail>")

    user_types = df['User Type'].value_counts()
    user_count = df['User Type'].count()

    print('\t stats on user type if available')
    for type in user_types.index:
            print('\t  - {:15}\t: {} ({:04.2f}%)'.format(type, user_types.loc[type],user_types.loc[type]/user_count*100))

    # Display counts of gender if available
    if('Gender' in df.columns):
        df['Gender'] = df['Gender'].fillna("<no data avail>")
        gender_types = df['Gender'].value_counts()
        gender_count = df['Gender'].count()
        print('\t stats on  user gender if available')
        for type in gender_types.index:
            print('\t  - {:15}\t: {} ({:04.2f}%)'.format(type, gender_types.loc[type],gender_types.loc[type]/gender_count*100))

    # Display earliest, most recent, and most common year of birth
    if(('Birth Year' in df.columns)):
        print('\t stats on  user age')
        birth_years = df['Birth Year'].dropna().sort_values()
        print('\t  - users year of birth variies between <{}> and <{}>'.format(int(birth_years.unique()[-1]), int(birth_years.unique()[0])))

        mc_year = df.groupby(['Birth Year'])['Birth Year'].count().idxmax()
        print('\t  - most users have been born in: ',int(mc_year))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_time(time_in_sec):
    """transform big amount of sec in human-readable time

    Returns:
        (str) time in nb_days, nb_hours, nb_min, nb_sec format
    """
    days        = time_in_sec // 86400
    remainder   = time_in_sec % 86400
    hours       = remainder // 3600
    remainder   = remainder % 3600
    minutes     = remainder // 60
    seconds     = remainder % 60

    return '{} days, {} hours, {} min, {}s'.format(int(days), int(hours), int(minutes), int(seconds))

def show_data(df):
        """ ask user
            display 5 first data rows on user request
        """
        show = input('\n>Would you like to see sample data? Press any key for yes / press [Enter] for no.\n')
        if(len(show)):
            print(df.head(5))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\n>Would you like to restart? Press any key for yes / press [Enter] for no.\n')
        if (len(restart)==0):
            break


if __name__ == "__main__":
	main()
