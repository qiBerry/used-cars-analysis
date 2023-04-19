# This is a sample Python script.
from collections import UserList
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def get_new_cars(df, year):
    # Use a breakpoint in the code line below to debug your script.
    df_result = df[df['year'] >= year]
    df_result.to_csv('new_cars.csv')
    print('New cars selected sucessfully')
    return df_result
    
    
def get_cars_had_accidents(df, has_accidents):
    df_result = df[df['has_accidents'] == has_accidents]
    name = ''
    if(has_accidents == False):
        name = 'no_'
    df_result.to_csv('had_' + name + 'accidents_cars.csv')
    print('New cars selected sucessfully')
    return df_result

#classs for 3 hypothesis
class brand(object):
    name = ''
    price = np.array([])
    power = np.array([])

    def __init__(self, name):
        self.name = name

    def add_values(self, price, power):
        self.price = np.append(self.price, [price])
        self.power = np.append(self.power, [power])

    def make_plots(self, path):
        c = np.rec.fromarrays([self.price, self.power])
        c.sort()

        self.price = c.f0
        self.power = c.f1

        fig, ax = plt.subplots()
        ax.plot(self.price, self.power)

        ax.set(xlabel='Price ($)', ylabel='Power (Horsepowers)',
               title=self.name + ' - the ratio of horsepowers to price')
        ax.grid()

        fig.set_size_inches(400, 100)
        fig.savefig(path + self.name + ".png", dpi=100)


def process_data(df):
    total_list = []
    brands_in_list = []
    for index, row in df.iterrows():
        brand_name = row['make_name']
        horsepowers = row['power']
        price = row['price']

        print(brand_name, ' - ', horsepowers, ' - ', price)

        if str(horsepowers) != 'nan':
            print('ok data')
            horsepowers = horsepowers[0:horsepowers.index(' ')]
            if not brand_name in brands_in_list:
                print(brand_name)
                total_list.append(brand(brand_name))
                brands_in_list.append(brand_name)

            total_list[brands_in_list.index(brand_name)].add_values(price, horsepowers)

        print(' ')
    return total_list


def make_graphs_price_to_horsepowers(filename_open, result_path):
    df = pd.read_csv(filename_open)
    print('Read sucessfully')
    df = df.reset_index()
    total_list = process_data(df)
    print('total list ready')

    for object in total_list:
        object.make_plots(result_path)
        # print(object.price)

    print('finished')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    make_graphs_price_to_horsepowers('had_no_accidents_cars.csv', 'plots_new_cars_no_accidents/')
    make_graphs_price_to_horsepowers('new_cars.csv', 'plots_new_cars/')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
