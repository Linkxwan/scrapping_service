import codecs
import requests

from bs4 import BeautifulSoup as BS

__all__ = ('work',)

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}


def work(url, city=None, language=None):
    jobs = []
    errors = []

    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=HEADER)
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://www.work.ua/ru/jobs-python/'
    jobs, errors = work(url)
    h = codecs.open('../work11.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
