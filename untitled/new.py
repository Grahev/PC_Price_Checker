import  pandas as pd
import requests
from bs4 import  BeautifulSoup
import csv
import time

spec_file = 'spec.csv'
link_list =[]
item_list = []
timestr = time.strftime("output - %Y-%m-%d.csv")



#czyta z pliku spec usowa spacje i dodaje do listy
def get_spec_from_file(file):
    list = []
    df = pd.read_csv(file)
    list = df['spec'].tolist()
    temp_list = []
    for a in list:
        a = a.replace(' ', '+')
        item_list.append(a)
    #print(list)
    #print(temp_list)
    return item_list

#spec_list = get_spec_from_file(spec_file)

#modyfikuje linki i dodaje do link_list
def ebay_link_create(item_list):
    for link in item_list:
        ebay_link = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw='+link+'&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1'
        #print(ebay_link)
        link_list.append(ebay_link)
    return link_list



#ready_links = ebay_link_create(spec_list)


def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print('Server responded:' , response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_detail_data(soup):
    #title
    try:
        title = soup.find('h3', class_= 's-item__title s-item__title--has-tags').text
    except:
        title ='title not found'

    print(title)
    #price
    try:
        price = soup.find('span', class_ = 's-item__price').span.text.replace('£','')
        #float_price = float(price)
    except:
        price = 'price not found'

    print(price)
    #condition
    try:
        condition = soup.find('span', class_ = 'SECONDARY_INFO').text
    except:
        condition = 'condition not found'

    print(condition)
    #bids
    try:
        bids = soup.find('span', class_ = 's-item__bids s-item__bidCount').text
    except:
        bids = '*Buy Now*'

    print(bids)
    #date
    try:
        date = soup.find('span', class_ = 's-item__ended-date s-item__endedDate').text
    except:
        date = 'date not found'

    print(date)
    #postage
    try:
        postage = soup.find('span', class_ = 's-item__shipping s-item__logisticsCost').text.replace('+ £','').split(' ')[0]
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
    listings = soup.find_all('div', class_ = 's-item__wrapper clearfix')
    return listings


def write_csv(data):
    with open(timestr, 'a', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], data['condition'], data['bids'], data['date'], data['postage']]


        writer.writerow(row)

def main():
    #get data from excel sheet to build links
    spec_list = get_spec_from_file(spec_file)
    print(spec_list)
    #build ebay search links
    ready_links = ebay_link_create(spec_list)
    print(ready_links)




    for link in ready_links:
        # build list of listings to get detail data
        listings = get_all_listings(get_page(link))
    #loop for all listings collect data and save to scv file
        for item in listings:
            data = get_detail_data(item)
            write_csv(data)







if __name__ == '__main__':
    main()






