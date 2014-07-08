# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from dbfunctions import dbFunctions
import urllib2
import re

# def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class GetAmazonCharts():

    def getAllAmazonKindleTops(self):

        proxy = urllib2.ProxyHandler({'http': 'http://myproxy:80'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)

        url_art = []
        url_bio = []
        url_biz = []
        url_child = []
        url_comic = []
        url_computer = []
        url_crime = []
            # Best Sellers in Kindle eBooks
        #     url="http://www.amazon.co.uk/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/341689031/ref=zg_bs_341689031_pg_"+str(i)+"?_encoding=UTF8&pg="+str(i)+"&ajax=3"
            # Best Sellers in Arts & Photography
        for i in range(1, 6):
            url_art.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Arts-Photography/zgbs/digital-text/362167031/ref=zg_bs_362167031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_bio.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Biography-True-Accounts/zgbs/digital-text/362181031/ref=zg_bs_341689031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_biz.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Business-Finance/zgbs/digital-text/362191031/ref=zg_bs_362191031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_child.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Childrens-eBooks/zgbs/digital-text/362219031/ref=zg_bs_362219031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_comic.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Comics-Graphic-Novels/zgbs/digital-text/362230031/ref=zg_bs_362230031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_computer.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Computing/zgbs/digital-text/362234031/ref=zg_bs_362234031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")
            url_crime.append("http://www.amazon.co.uk/Best-Sellers-Kindle-Store-Crime-Thriller-Mystery/zgbs/digital-text/362247031/ref=zg_bs_362247031_pg_" + str(i) + "?_encoding=UTF8&pg=" + str(i) + "&ajax=3")

        mongo = dbFunctions()

        # url_all = [url_art , url_bio, url_biz, url_child, url_comic, url_computer, url_crime]
        url_all = {'Art' : url_art,
                   'Biography' : url_bio,
                   'Business' : url_biz,
                   'Children' : url_child,
                   'Comic': url_comic,
                   'Computer' : url_computer,
                   'Crime': url_crime}

        for url_section in url_all.keys():
            print 20 * '-' + url_section + 20 * '-'
            for url in url_all[url_section]:
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page.read())
                best_sellers = soup.findAll('div', {'class':'zg_itemImmersion'})
                for bs in best_sellers:
                    rank = bs.find('div', {'class':'zg_rankDiv'}).span.string.replace('.', '')
        #             print rank
                    try:
                        title_short = bs.find('div', {'class':'zg_title'}).a.string
                        title_link = re.sub('\s+', ' ', bs.find('div', {'class':'zg_title'}).a['href'])
                        page_title = urllib2.urlopen(title_link)
#                         soup_title = BeautifulSoup(page_title.read())
#                         title_full = re.sub('\s+', ' ', soup_title.find('span', {'id' : 'btAsinTitle'}).span.contents[0])
                    except:
                        title_short = 'Unknown title'
#                         title_full = 'Unknown title'
                    try:
                        author_unf = bs.find('div', {'class':'zg_byline'}).string.replace('by ', '')[:-1]
                        author = re.sub('\s+', ' ', author_unf)
        #                 print author
                    except:
                        author = 'Unknown author'
                    try:
                        rate = bs.find('span', {'class' : 'asinReviewsSummary'}).span['title']
        #                 print rate
                    except:
                        rate = 'No rating'
                    try:
                        price = bs.find('div', {'class':'zg_price'}).strong.string
        #                 print price
                    except:
                        price = 'Unknown price'
                    try:
                        image_link = bs.find('div', {'class' : 'zg_itemImageImmersion'}).img['src']
                    except:
                        image_link = 'Not Found'
                    entry ={ 'rank' : rank , 
                            'short_title': title_short,
                            'title_link': title_link,
                            'author': author,
                            'rate': rate,
                            'price' : price,
                            'image_link' : image_link}
                    print entry
                    mongo.insertItemtoCharts(entry)
                    
if __name__ == '__main__':
    ch = GetAmazonCharts()
    ch.getAllAmazonKindleTops()

