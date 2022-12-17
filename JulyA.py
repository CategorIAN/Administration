import pandas as pd
import numpy as np
from People import People

class JulyA:
    def __init__(self, df):
        df = df.rename(self.rename_columns2, axis=1)
        df = df.fillna("")
        df = self.setDF(df)
        df = self.removeDuplicates(df)
        df = df.drop(['Timestamp'], axis=1)
        df = self.addNames(df)
        df = df.sort_values(by='Name')
        df.reset_index(drop=True, inplace=True)

        month = {}
        total = {'Name': 'Total'}
        month['Email'] = df['Email']
        month['Name'] = df['Name']
        for week in ['Week_1', 'Week_2', 'Week_3', 'Week_4']:
            for i in range(len(self.dates[week])):
                t = 0
                a = []
                for j in range(df.shape[0]):
                    if (not pd.isnull(df.at[j, week]) and self.days[i] in df.at[j, week]):
                        a.append(1)
                        t += 1
                    else: a.append(0)
                month[self.dates[week][i]] = a
                total[self.dates[week][i]] = t

        grid = pd.DataFrame(month)
        grid = grid.append(total, ignore_index = True)

        df = self.stringDF(df)
        self.df = df
        self.grid = grid


    def setDF(self, df) -> pd.DataFrame:
        for column in df.columns:
            if (column not in {'Email', 'Name'}):
                df[column] = df[column].apply(lambda x: self.notnull(self.toSet)(x))
        return df

    def notnull(self, f):
        def g(x):
            if (not pd.isnull(x)):
                return f(x)
            else:
                return x
        return g

    def toSet(self, string):
        s = set()
        for e in string.split(","):
            s.add(e.strip())
        return s

    def stringDF(self, df) -> pd.DataFrame:
        for column in df.columns:
            if (column not in {'Email', 'Name'}):
                df[column] = df[column].apply(self.notnull(self.toString))
        return df

    def toString(self, ss):
        string = ""
        for s in ss:
            string = string + s + ", "
        return string.strip(", ")

    def removeDuplicates(self, df):
        emails = set()
        for i in reversed(range(df.shape[0])):
            e = df.at[i, 'Email']
            if e in emails:
                df = df.drop(i)
            else:
                emails.add(e)
        return df

    def addNames(self, df):
        P = People()
        names = []
        for i in range(df.shape[0]):
            names.append(P.lookup[df.at[i, 'Email']])
        df.insert(1, "Name", names)
        return df

    time_stamp = "Timestamp"
    email = "Email Address"
    week1 = "What days are you probably available for PKT events in July? [Week 2 (July 8th - July 10th)]"
    week2 = "What days are you probably available for PKT events in July? [Week 3 (July 15th - July 17th)]"
    week3 = "What days are you probably available for PKT events in July? [Week 4 (July 22nd - July 24th)]"
    week4 = "What days are you probably available for PKT events in July? [Week 5 (July 29th - July 31st)]"
    question = "What days are you probably available for PKT events in July?"
    weeks = ["Week 2 (July 8th - July 10th)", "Week 3 (July 15th - July 17th)", "Week 4 (July 22nd - July 24th)",
             "Week 5 (July 29th - July 31st)"]

    rename_columns2 = {email: 'Email'}
    for i in range(len(weeks)):
        rename_columns2["{} [{}]".format(question, weeks[i])] ="Week_{}".format(i+1)

    rename_columns = {time_stamp: 'Timestamp', email: 'Email', week1: 'Week_1', week2: 'Week_2', week3: 'Week_3',
                      week4: 'Week_4'}

    dates = {'Week_1':['July 8th', 'July 9th', 'July 10th'], 'Week_2':['July 15th', 'July 16th', 'July 17th'],
             'Week_3':['July 22nd', 'July 23rd', 'July 24th'], 'Week_4':['July 29th', 'July 30th', 'July 31st']}


    week1_dates = ['June 3rd', 'June 4th', 'June 5th']
    week2_dates = ['June 10th', 'June 11th', 'June 12th']
    week3_dates = ['June 17th', 'June 18th', 'June 19th']
    week4_dates = ['June 24th', 'June 25th', 'June 26th']
    days = ['Friday', 'Saturday', 'Sunday']

