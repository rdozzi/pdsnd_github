import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    city_count = 0
    month_count = 0
    day_count = 0
    
    city_list = ['','chicago', 'new_york_city', 'washington']
    month_list = ['','january','february','march','april','may','june','all']
    day_list = ['', 'monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday','all']
    
    print('\n1 - Chicago\n2 - New York City\n3 - Washington\n')
    while city_count not in range(1,4):
        try: 
            city_count = eval(input('Please enter a number for the city: '))
        except (NameError, SyntaxError):
            print('\nNot a number!')

    # get user input for month (january, february, ... , all)
    print('\n1 - January\n2 - February \n3 - March\n4 - April \
          \n5 - May\n6 - June\n7 - All Months\n')
    while month_count not in range(1,8):
        try:
            month_count = eval(input('Please enter a number for the month: '))
        except (NameError, SyntaxError):
            print('\nNot a number!')
        
    # get user input for day of week (monday, tuesday, ... sunday, all)
    print('\n1 - Monday\n2 - Tuesday\n3 - Wednesday\n4 - Thursday \
          \n5 - Friday\n6 - Saturday\n7 - Sunday\n8 - All Days\n')
    while day_count not in range(1,9):
        try:
            day_count = eval(input('Please enter a number for the day: '))
        except (NameError, SyntaxError):
            print('\nNot a number!')

    print('-'*40)
    return city_list[city_count], month_list[month_count], day_list[day_count]

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

    #Create a variable to load the city specific data
    selected_city = city + '.csv'

    #Load the list from the local machine
    df = pd.read_csv('~/documents/Udacity_intro_python_ds/bikeshare-2/' + selected_city)

    #Convert 'Start Time' 
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create new columns to filter data by month and day (w/ other columns)
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.weekday
    df['Hour'] = df['Start Time'].dt.hour

    #Filter by month if applicable
    if month != 'all':
        month_list = ['january', 'february', 'march', 
                      'april', 'may', 'june']
        month = month_list.index(month) + 1
        df = df[df['Month'] == month]
    
    #Filter by day
    if day != 'all':
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 
                    'friday', 'saturday', 'sunday']
        day = day_list.index(day)
        df = df[df['Day'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month unless a month was selected
    month_list = ['january', 'february', 'march', 
                  'april', 'may', 'june']
    # Provide different speech output when user selects either 'all' or a specific month
    if 1 in df['Month'].values and 2 in df['Month'].values:
        month_number = df['Month'].mode()[0]
        most_common_month = month_list[month_number-1].capitalize()
        most_common_month_speech = 'The most common month is: '
    else:
        month_number = df['Month'].reset_index().drop(columns = 'index')
        month_number = month_number.loc[0,'Month']
        most_common_month = month_list[month_number-1].capitalize()
        most_common_month_speech = 'The month you selected is: '

    # Display the most common day of week unless a specific day was selected
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 
                'friday', 'saturday', 'sunday']
    # Provide different speech output when user selects either 'all' or a specific day
    if 1 in df['Day'].values and 2 in df['Day'].values:
        day_number = df['Day'].mode()[0]
        most_common_day = day_list[day_number].capitalize()
        most_common_day_speech = 'The most common day is: '
    else:
        day_number = df['Day'].reset_index().drop(columns = 'index')
        day_number = day_number.loc[0,'Day']
        most_common_day = day_list[day_number].capitalize()
        most_common_day_speech = 'The day you selected is: '

    # display the most common start hour range
    start_hour_int = df['Hour'].mode()[0]
    most_common_start_range = str(int(start_hour_int)) + ':00-' + \
                              str(int(start_hour_int+1)) + ':00'
    most_common_start_speech = 'The most common start time range is: '

    # tl = "time list" to abbreviate return statement
    tl =[most_common_month_speech, most_common_month, most_common_day_speech, \
    most_common_day, most_common_start_speech, most_common_start_range]

    return(tl[0] + tl[1] + '\n' + tl[2] + tl[3] + '\n' + tl[4] + tl[5] + '\n'
           '\nThis took %s seconds.' % '{:02.3f}'.format(time.time() - \
           start_time) + '\n' + '-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    group_df = df.groupby(['Start Station','End Station']).size().reset_index(name='Count')
    group_df = group_df.sort_values(by=['Count'], ascending=False)
    group_df = group_df.reset_index()
    group_df = group_df.drop(labels = ['index'], axis = 1)


    return('The most common start station is: {}\nThe most common end station '\
           'is: {}\nThe most frequent Start and End Station trip is from ' \
           '{} to {}\n'.format(most_common_start_station, most_common_end_station, 
           group_df.loc[0]['Start Station'], group_df.loc[0]['End Station']) +
           '\nThis took %s seconds.' % '{:02.3f}'.format(time.time() - start_time) + 
           '\n' + '-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_trip_duration = df['Trip Duration'].sum() / 60 / 60
    total_days = int(sum_trip_duration / 24)
    remainder_duration = float(sum_trip_duration % 24)
    remainder_hours = int(remainder_duration)
    remainder_minutes = int(round((remainder_duration - remainder_hours)*60,0))
    total_travel_time = '{} Days, {} Hours, {} Minutes'.format(total_days, 
                        remainder_hours, remainder_minutes)

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean() / 60 / 60
    #mean_days = int(mean_trip_duration / 24)
    remainder_mean = float(mean_trip_duration % 24)
    mean_hours = int(remainder_mean)
    mean_minutes = int(round((remainder_mean - mean_hours)*60,0))
    mean_travel_time = '{} Hours, {} Minutes'.format(mean_hours, mean_minutes)

   # return mean_travel_time

    return('The total travel time for the period selected is: {}\n' \
           'The average travel time for the period selected is: {}\n'.format
           (total_travel_time, mean_travel_time) + '\nThis took %s seconds.'
           % '{:02.3f}'.format(time.time() - start_time) + '\n' + '-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_type_count = df.groupby(['User Type']).size().reset_index(name='Count')
    count_customer = df_type_count['Count'][0]
    count_subscriber = df_type_count['Count'][1]

    # Display counts of gender; WA has no gender data
    if 'Gender' in df.columns:
        df_gender_count = df.groupby(['Gender']).size().reset_index(name='Count')
        count_female = df_gender_count['Count'][0]
        count_male = df_gender_count['Count'][1]
    else:
        count_female = 'N/A'
        count_male = 'N/A'

    # Display earliest, most recent, and most common year of birth; WA has no Birth Year Data
    if 'Birth Year' in df.columns:
        df_yob = df['Birth Year'].dropna(axis = 0)
        df_yob = pd.to_datetime(df_yob, format = '%Y')
        df_yob = df_yob.dt.year
        df_yob = df_yob.reset_index().drop(columns = 'index')
        #Remove birth years that are less than 1930. Beyond that seems erroneous
        df_yob = df_yob[(df_yob['Birth Year'] >= 1930) & (df_yob['Birth Year'] <= 2010)]
        df_yob = df_yob.sort_values(by = 'Birth Year', ascending=False)
        df_yob = df_yob.reset_index().drop(columns = 'index')
        earliest_yob = df_yob.at[df_yob.index.max(),'Birth Year']
        most_recent_yob = df_yob.at[0,'Birth Year']
        most_common_yob = df_yob.mode().at[0,'Birth Year']
    else:
        earliest_yob = 'N/A'
        most_recent_yob = 'N/A'
        most_common_yob = 'N/A'

    #ul = 'User List" to abbreviate return statement
    ul = [count_customer, count_subscriber, count_female, \
    count_male, earliest_yob, most_recent_yob, most_common_yob]

    return('User Type Count:\n\nCustomer: {}\nSubscriber: {}\n\n' \
           'Gender:\n\nFemale: {}\nMale: {}\n\n' \
           'Age Data:\n\nEarliest Birth Year: {}\nMost Recent Birth Year: {}\n' \
           'Most Common Birth Year: {}\n\n' \
           .format(ul[0], ul[1], ul[2], ul[3], ul[4], ul[5], ul[6]) +\
           'This took %s seconds.' % '{:02.3f}'.format(time.time() - \
           start_time) + '\n' + '-' * 40)

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print(time_stats(df))
        print(station_stats(df))
        print(trip_duration_stats(df))
        print(user_stats(df))

        restart = input('\nSelect "r" to restart or type any other key to exit: ')
        if restart != 'r':
            break

if __name__ == "__main__":
	main()

