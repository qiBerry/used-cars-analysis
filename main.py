# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def get_new_cars_data(df):
    # Use a breakpoint in the code line below to debug your script.
    df_new_cars = df[df['year'] >= 2020]
    df_new_cars.to_csv('new_cars.csv')
    print('New cars selected sucessfully')
    return df_new_cars


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import time
    import pandas as pd

    start = time.time()

    df = pd.read_csv('used_cars_data.csv')
    print('Read sucessfully')

    df = get_new_cars_data(df)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
