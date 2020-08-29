import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import time
import os

spec_file = 'spec.csv'
link_list = []
item_list = []
timestr = time.strftime(" - %Y-%m-%d.csv")


# czyta z pliku spec usowa spacje i dodaje do listy
def get_spec_from_file(file):
    df = pd.read_csv(file)
    list = df['spec'].tolist()
    return list

def create_ebay_link(a):
    link = a.replace(' ', '+')
    ebay_link = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=' + link + '&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1'
    return ebay_link








def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    # title
    try:
        title = soup.find('h3', class_='s-item__title s-item__title--has-tags').text
    except:
        title = 'title not found'

    print(title)
    # price
    try:
        price = soup.find('span', class_='s-item__price').span.text.replace('£', '')
        # float_price = float(price)
    except:
        price = 'price not found'

    print(price)
    # condition
    try:
        condition = soup.find('span', class_='SECONDARY_INFO').text
    except:
        condition = 'condition not found'

    print(condition)
    # bids
    try:
        bids = soup.find('span', class_='s-item__bids s-item__bidCount').text
    except:
        bids = '*Buy Now*'

    print(bids)
    # date
    try:
        date = soup.find('span', class_='s-item__ended-date s-item__endedDate').text
    except:
        date = 'date not found'

    print(date)
    # postage
    try:
        postage = soup.find('span', class_='s-item__shipping s-item__logisticsCost').text.replace('+ £', '').split(' ')[
            0]
    except:
        postage = 'postage not found'

    print(postage)

    data = {
        'title': title,
        'price': price,
        'condition': condition,
        'bids': bids,
        'date': date,
        'postage': postage
    }
    print(data)
    return data


def get_all_listings(soup):
    listings = soup.find_all('div', class_='s-item__wrapper clearfix')
    return listings


def write_csv(data,id):

    with open(f'output/{id}/'+id + timestr, 'a', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], data['condition'], data['bids'], data['date'], data['postage']]

        writer.writerow(row)


#create subfolder to save csv file
def create_sub_folder(id):
    folder = f'output/{id}'
    if not os.path.exists(folder):
        os.makedirs(folder)


#scan output folder and make file list
def folder_scan(id):
    file_list = []
    for root, dirs, files in os.walk(f"output/{id}"):
        for filename in files:
            file_list.append(filename)
            print(filename)
        return file_list



#clean output file
def clean_data(id):
    file_list = folder_scan(id)
    output_df = pd.DataFrame()
    for file in file_list:

        df = pd.read_csv(f'output/{id}/{file}', names = ['title', 'price', 'condition', 'bids', 'sold date' , 'postage'])
        remove = df[df['condition'] == "Parts only"].index
        df.set_index('sold date')
        df.drop(remove, inplace = True)
        #print(df.describe()['price'])
        output_df = output_df.append(df)
    output_df.drop_duplicates(inplace=True)
    output_df.sort_values("sold date",ascending=False, inplace=True)
    output_df.to_csv(f'{id}.csv')



def main():
    item_list = get_spec_from_file(spec_file)
    print(item_list)
    for item in item_list:
        id = item
        ebay_link = create_ebay_link(item)
        listings = get_all_listings(get_page(ebay_link))
        for item in listings:
            data = get_detail_data(item)
            create_sub_folder(id)
            write_csv(data, id)
        clean_data(id)






if __name__ == '__main__':
   main()






