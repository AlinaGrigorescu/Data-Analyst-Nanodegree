import time
import pandas as pd
import numpy as np

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #Define lists for user input alternatives
    cities=['washington','chicago','new york']
    months_list=['jan','feb','apr','may','jun','jul','aug','sep','oct','nov','dec','all']
    days_list=['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
          city=input('\nInput one of these cities: Chicago, Washington, New York:\n')
          if city.lower() in cities:
              break
          else:
              print('\nPlease enter a valid city!\n')
              continue

    # get user input for month (all, january, february, ... , june)
    while True:
         month=input('\nInput one of these months: Jan, Feb, Mar, Apr, May, Jun, ALL:\n')
         if month.lower() in months_list:
            break
         else:
             print('\nPlease input a Month name from the list!\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
         day=input('\nInput one of these weekdays: Monday, Tuesday, Wednesay, Thursady, Friday, Saturday, Sunday, ALL:\n')
         if day.lower() in days_list:
            break
         else:
             print('\nPlease insert a valid DAY name!\n')

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
    if city.lower()== 'Chicago'.lower():
        df=pd.read_csv('chicago.csv')
    elif city.lower()=='New York'.lower():
        df=pd.read_csv('new_york_city.csv')
    else: df=pd.read_csv('washington.csv')
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
    month_list=['jan','feb','mar','apr','may','jun','all']
    monthno=month_list.index(month.lower())+1

    #Filtering dataframe by day, month
    if day.lower()!='all' and month.lower()!='all':
       df=df[(df['month']==monthno) & (df['day_of_week']==day.title())]
    elif day.lower()=='all' and month.lower()!='all':
        df=df[df['month']==monthno]
    elif day.lower()!='all' and month.lower()=='all':
        df=df[df['day_of_week'==day.title()]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['month'].mode()[0]
    print('Most frequent Month of travel for is ',common_month)

    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print('Most frequent Weekday of travel for is ',common_day)

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    common_hour=df['hour'].mode()[0]
    print('Most frequent Hour of travel for is ',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start=df['Start Station'].mode()[0]
    print('\nMost frequent START STATION of travel is: ',common_start)

    # display most commonly used end station
    common_end=df['End Station'].mode()[0]
    print('\nMost frequent END STATION of travel is: ',common_end)

    # display most frequent combination of start station and end station trip
    df['route']="("+df['Start Station'] + ") TO (" + df['End Station']+")"
    common_route=df['route'].mode()[0]
    print('\nMost common ROUTE is: ',common_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Duration']=df['Trip Duration'].astype(float)

    # display total travel time
    total_tt=df['Trip Duration'].sum()
    print('Total travel time: ',total_tt)

    # display mean travel time
    total_mt=df['Trip Duration'].mean()
    print('Mean travel time: ',total_mt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts().reset_index()
    print('\nNo. of USER types:\n',user_types.to_string(index=False, header=['User Type','Count']))

    # Display counts of gender
    gender_types=df['Gender'].value_counts().reset_index()
    print('\nNo. of GENDER types:\n',gender_types.to_string(index=False, header=['Gender','Count']))

    # Display earliest, most recent, and most common year of birth
    df['Birth Year']=df['Birth Year'].astype(float)
    print('\nOldest customer Year of birth:',df['Birth Year'].min())
    print('\nYoungest customer Year of birth:',df['Birth Year'].max())
    print('\nMost frequent Year of birth customer:',df['Birth Year'].mode())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #Display sample of data
        display=input('\nWould you like to see a sample of 5 lines[YES/NO]?\n')
        nrrows=5
        while True:
            if display.lower()=='yes':
               if nrrows>df.shape[0]:
                  print('\nThose were all the records for the filters you set!\n')
                  break
               print(df[:nrrows])
               display=input('\nWould you like to see more[YES/NO]?\n')
               if display.lower()=='yes':
                   nrrows=nrrows+5
            else:
                break
        #Display time statistics
        time_stats(df)

        #Display route statistics
        station_stats(df)

        #Display trip duration statistics
        trip_duration_stats(df)

        #Display USER statistics depending on the city chosen
        if city.lower()!='washington':
           user_stats(df)
        else:
           print('\nNo. of USER types:\n',df['User Type'].value_counts())
           print('\nNo other User Statics available for Washington!\n')

        #Repeat the input and statistics
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

