import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


chromedriver = './chromedriver'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.918 Yowser/2.5 Safari/537.36'

class ParseMagazine():
    def __init__(self, url):
        self.url = url

    def parse(self, page_fields):

        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument('window-size=800x600')

        if page_fields.get('settings') == 'selenium':
            with webdriver.Chrome(executable_path=chromedriver, chrome_options=options) as browser:
                browser.implicitly_wait(10)
                browser.get(self.url)
                for field in page_fields['fields']:
                    if field[2].get('class'):
                        try:
                            browser.find_element_by_css_selector(f".{field[2]['class']}")
                        except Exception as e:
                            print(e)
                requiredhtml = browser.page_source
        else:
            response = requests.get(self.url, headers={'User-Agent':UserAgent().chrome})
            print(response)
            requiredhtml = response.text

        soup = bs(requiredhtml, "html.parser")
        output = {}
        for field in page_fields['fields']:
            if field[2].get('class'):
                value = soup.find(field[1], class_=field[2]['class'])
            else:
                value = soup.find(field[1], attrs=field[2])
            if value:
                value = value.text.strip()
            output[field[0]] = value
        # with open(f'{output["Название"]}.html', 'w') as f_out:
        #     f_out.write(requiredhtml)
        return output

DNS = {'settings':'selenium',
        'fields':
            (('Название', 'h1', {'class':'page-title'}),
             ('Цена', 'span', {'class':'product-card-price__current'}),
             ('Наличие', 'a', {'class':'avail-text__link'}),
             ('Descr', 'div', {'itemprop':'description'}))}

MVIDEO = {'fields':
            (('Название', 'h1', {'class':'fl-h1'}),
            ('Цена', 'div', {'class':'fl-pdp-price__current'}),
            ('Наличие', 'div', {'class':'c-delivery__text'}),
            ('Descr', 'div', {'class':'collapse-text-initial'}))}

dns_shop = ParseMagazine('https://www.dns-shop.ru/product/47ec304de1691b80/nabor-skovorod-aceline-kw-3m-multicook/')
dns_shop2 = ParseMagazine('https://www.dns-shop.ru/product/b3b9a97aac493330/elektriceskaa-plita-mecta-15m-cernyj/')
mvideo1 = ParseMagazine('https://www.mvideo.ru/products/naushniki-true-wireless-jbl-tune-220-tws-green-50134465')

print(dns_shop2.parse(DNS))
print(dns_shop.parse(DNS))
print(mvideo1.parse(MVIDEO))

