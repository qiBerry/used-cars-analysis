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


def calculate_slope(x, y):
    mx = x - x.mean()
    my = y - y.mean()
    return sum(mx * my) / sum(mx ** 2)


def get_params(x, y):
    a = calculate_slope(x, y)
    b = y.mean() - a * x.mean()
    return a, b

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
        temp = np.array([])

        #делим на 1000, чтобы получить значения в тысячах долларов
        for x in self.price:
            temp = np.append(temp, [float(x)/1000.0])
        self.price = temp

        #Кроме того, чтобы избежать излишней волатильности цены, мы ее прологарифмируем
        self.price = np.log(self.price)

        c = np.rec.fromarrays([self.price, self.power])
        c.sort()

        self.price = c.f0
        self.power = c.f1

        a, b = get_params(self.price, self.power)
        equation_str = 'y = ' + str(a) + '*x + ' + str(b)
        equation = a*self.price + b

        fig, ax = plt.subplots()
        plt.xlabel('Price (thousands of $)')
        plt.ylabel('Power (Horsepowers)')
        plt.title(self.name + ' | ' + equation_str)
        #ax.set(xlabel='Price ($)', ylabel='Power (Horsepowers)',
        #       title=self.name + ' | ' + equation_str)
        plt.scatter(self.price, self.power)
        plt.plot(self.price, equation, color='red')

        #plt.fig.set_size_inches(60, 15)
        figure = plt.gcf()
        figure.set_size_inches(20, 8)
        plt.savefig(path + self.name + ".png", dpi=100)
        #plt.show()



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
            horsepowers = float(horsepowers[0:horsepowers.index(' ')])
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
    #make_graphs_price_to_horsepowers('new_cars.csv', 'plots_new_cars_linear_regression/')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
