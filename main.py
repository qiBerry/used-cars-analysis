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


def get_cars_had_accidents_not_nan(df):
    df_true = get_cars_had_accidents(df, True)
    df_false = get_cars_had_accidents(df, False)
    frames = [df_true, df_false]
    result = pd.concat(frames)
    result.to_csv('cars_had_accidents_not_nan.csv')
    return result
    
    
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
    middle_price = 0
    power = np.array([])
    days_on_market = np.array([])
    middle_days_on_market = 0
    has_accidents = np.array([])
    has_accidents_percent = 0

    def __init__(self, name):
        self.name = name

    def calculate_params(self):
        self.middle_price = np.sum(self.price)/self.price.size
        self.middle_days_on_market = np.sum(self.days_on_market)/self.days_on_market.size
        self.has_accidents_percent = np.count_nonzero(self.has_accidents == True)/self.has_accidents.size
        print(self.name, ',' , self.middle_price, ',', self.middle_days_on_market, ',', self.has_accidents_percent)

    def add_values_price_power(self, price, power):
        self.price = np.append(self.price, [price])
        self.power = np.append(self.power, [power])

    def add_values_price(self, price):
        self.price = np.append(self.price, [price])

    def add_values_has_accidents(self, has_accidents):
        self.has_accidents = np.append(self.has_accidents, [has_accidents])
    def add_values_days_on_market(self, days_on_market):
        self.days_on_market = np.append(self.days_on_market, [days_on_market])

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

        temp_pd = pd.DataFrame({'price':self.price, 'power':self.power})
        temp_pd.to_csv(path + self.name + ".csv")

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

#def process_data_brand_days_on_market(df):
#    total_list[]


def process_data_price_horsepowers_relation(df):
    total_list = []
    brands_in_list = []
    for index, row in df.iterrows():
        brand_name = row['make_name']
        horsepowers = row['power']
        price = row['price']

        print(brand_name, ' - ', horsepowers, ' - ', price)

        if str(horsepowers) != 'None':
            print('ok data')
            horsepowers = float(horsepowers[0:horsepowers.index(' ')])
            if not brand_name in brands_in_list:
                print(brand_name)
                total_list.append(brand(brand_name))
                brands_in_list.append(brand_name)

            total_list[brands_in_list.index(brand_name)].add_values_price_power(price, horsepowers)

        print(' ')
    return total_list


def process_data_brand_info(df):
    total_list = []
    brands_in_list = []
    for index, row in df.iterrows():
        brand_name = row['make_name']
        days_on_market = float(row['daysonmarket'])
        has_accidents = bool(row['has_accidents'])
        price = float(row['price'])
        print(str(index),',',brand_name,',', price, ",", days_on_market, ",", has_accidents)
        #if pd.isna(days_on_market) and pd.isna(has_accidents) and pd.isna(price):

        if not brand_name in brands_in_list:
            total_list.append(brand(brand_name))
            brands_in_list.append(brand_name)

        total_list[brands_in_list.index(brand_name)].add_values_has_accidents(has_accidents)
        total_list[brands_in_list.index(brand_name)].add_values_price(price)
        total_list[brands_in_list.index(brand_name)].add_values_days_on_market(days_on_market)

    print('brand , middle_price , middle_days_on_market , has_accidents_percent')
    for x in total_list:
        x.calculate_params()

    return total_list



def make_graphs_price_to_horsepowers(df, result_path):
    df = df.reset_index()
    total_list = process_data_price_horsepowers_relation(df)
    print('total list ready')

    for object in total_list:
        object.make_plots(result_path)
        # print(object.price)

    print('finished')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from sqlalchemy import create_engine
    import sys

    engine = create_engine('postgresql://admin:pgpwd4project@localhost:5432/main')
    np.set_printoptions(threshold=sys.maxsize)

    #make_graphs_price_to_horsepowers('had_no_accidents_cars.csv', 'plots_new_cars_no_accidents/')
    #make_graphs_price_to_horsepowers('new_cars.csv', 'plots_new_cars_linear_regression/')
    df = pd.read_csv('cars_had_accidents_not_nan.csv')
    df = pd.read_sql_query('select * from "cars"',con=engine)
    print('Read sucessfully')
    #new_df = df.filter(['id','make_name','power','price','daysonmarket','has_accidents'], axis=1)
    #new_df.to_csv('export2.csv')
    #process_data_brand_info(df)
    df_no_accidents = get_cars_had_accidents(df, False)
    make_graphs_price_to_horsepowers(df_no_accidents, 'new_output/')
    #process_data_brand_info(df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
