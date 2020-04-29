import datetime, sys, os.path
from matplotlib import pyplot as plt
try:
    import pandas as pd
    ERROR = 0
except:
    ERROR = 1

number = []
dates = []
days = [1]

file_name = 'pullups.txt' # Edit this as given. Sample 'pullups.txt' provided to show CSV style
DATA_TEMPLATE = 'Set 1,Set 2,Set 3,Set 4,Set 5,Set 6,Set 7,Set 8,Set 9,Set 10,Date'

def checkDateFormat(givendate):
    if '/' in givendate and len(givendate) <= 10:
        givendate = givendate.split('/')
        try:
            int(givendate[0])
            int(givendate[1])
            int(givendate[2])
            return True
        except:
            return False


def checkLengths(list1, list2):
    if len(list1) == len(list2):
        return True
    else:
        return False


def sumOfList(supplied_list):
    summation = 0

    for item in supplied_list:
        try:
            summation += int(item)
        except:
            return False

    if summation > 0:
        return True


# Data frame. V imp
if ERROR == 0:
    if os.path.isfile(file_name):
        df = pd.read_csv(file_name)

    else:
        with open(file_name, 'w') as f:
            f.write(DATA_TEMPLATE)
            f.close()

        df = pd.read_csv(file_name)


def addSets(df):
    numbers = []
    loop = 0

    while True:
        numbers.append(input(f'Number of reps in set {loop+1}: '))
        loop +=1


        try:
            int(numbers[loop-1])
        except:
            numbers[loop-1] = '0'


        if loop == 10 or numbers[loop-1] == '0' or not numbers[loop-1]:
            if numbers[loop-1] == '0' or not numbers[loop-1]:
                if not numbers[loop-1]:
                    numbers[loop-1] = '0'

                remaining = 10 - loop
                for i in range(0, remaining):
                    numbers.append('0')
            break
    

    if numbers:
        for i in range(0, len(numbers)):
            try:
                int(numbers[i])
            except ValueError:
                numbers[i] = '0'




    date = input('Date (DD/MM/YYY): ')
    if checkDateFormat(date) and sumOfList(numbers):
        df_add = pd.DataFrame({'Set 1': [numbers[0]],
                               'Set 2': [numbers[1]],
                               'Set 3': [numbers[2]],
                               'Set 4': [numbers[3]],
                               'Set 5': [numbers[4]],
                               'Set 6': [numbers[5]],
                               'Set 7': [numbers[6]],
                               'Set 8': [numbers[7]],
                               'Set 9': [numbers[8]],
                               'Set 10': [numbers[9]],
                               'Date': [date]})

        result = df.append(df_add, ignore_index=True)
        result.to_csv(file_name, index=False)
    
    else:
        print('Improper date format or sets amount to zero.')


def visualization(df):
    number = []
    dates = []
    days = [1]

    ERROR = 0

    for row in df.values:
        try:
            if checkDateFormat(row[10]):
                        number.append(int(row[0]) + int(row[1]) + int(row[2]) + 
                                      int(row[3]) + int(row[4]) + int(row[5]) + 
                                      int(row[6]) + int(row[7]) + int(row[8]) + 
                                      int(row[9]))
                        
                        dates.append(row[10])

        except:
            ERROR = 1

    if not checkLengths(number, dates) and ERROR == 0:
        print('Error in data handling.')
        ERROR = 1


    if ERROR == 0:
        for i in range(0, len(dates)):
            # dates[i][0:2]) # Day
            # dates[i][3:5]) # Month
            # dates[i][6:]) # Year

            if i < len(dates) - 1:
                days.append(days[i] + (datetime.date(int(dates[i+1][6:]), int(dates[i+1][3:5]), int(dates[i+1][0:2])) - 
                                       datetime.date(int(dates[i][6:]), int(dates[i][3:5]), int(dates[i][0:2]))).days)            
    
        for i in range(0, len(days)):
            days[i] = int(days[i])
            number[i] = int(number[i])

    
        plt.plot(days, number)
        plt.ylabel('Pull Up Total')
        plt.xlabel('Days')
        plt.show()


def usage():
    message = """
        Command:           Action:  
        -h, -help          -Print this message
        
        -a, -add           -Add upto 10 sets and a date
                           -Entering sets stops if improper 
                            format supplied
        
        -v, -visualize     -Show a graph of total reps on the
                            Y axis and days since you started
                            on the X axis

        -d, -dataframe     -Show a table of all reps performed
                            on a specific date

        """
    
    return message


def main():
    if len(sys.argv) > 2:
        print(usage())

    elif len(sys.argv) == 1:
        visualization(df)

    else:
        if sys.argv[1] in ['-h', '--help']:
            print(usage())

        elif sys.argv[1] in ['-a', '-add']:
            addSets(df)

        elif sys.argv[1] in ['-v', '-visualize']:
            visualization(df)

        elif sys.argv[1] in ['-d', '-dataframe']:
            print(df)

        else:
            print(usage())


if __name__ == '__main__':
    if ERROR == 0:
        main()
