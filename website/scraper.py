'''
scraper.py scrapes the data and sends it to whoever asked for it.
'''

import requests
from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep, time

headers = {
'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
'Accept-Language' : 'en-GB,en;q=0.5',
'Referer' : 'https://google.com',
'DNT' : '1'
}



def b4s_get_page_links(link, source, page):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Accept-Language' : 'en-GB,en;q=0.5',
    'Referer' : 'https://google.com',
    'DNT' : '1'
    }
    url = link + f'?page={page}'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    
    soup = bs(r.text, 'lxml')
    links = soup.select('article.scholarshipslistcard_scholarshipName__1JExQ h4')
    urls = [source + link.a.get('href') for link in links]
    unique_urls = []
    [unique_urls.append(url) for url in urls if url not in unique_urls]
    return unique_urls


def s4d_get_page_links(link, source, page):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Accept-Language' : 'en-GB,en;q=0.5',
    'Referer' : 'https://google.com',
    'DNT' : '1'
    }
    url = link + f'/page/{page}'

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    

    soup = bs(r.text, 'lxml')
    links = soup.select('div.maincontent2>div.post>div.entry>h2')
    urls = [link.a.get('href') for link in links]
    unique_urls = []
    [unique_urls.append(url) for url in urls if url not in unique_urls]
    return unique_urls


def b4s_schols_data(url, source, category):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Accept-Language' : 'en-GB,en;q=0.5',
    'Referer' : 'https://google.com',
    'DNT' : '1'
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    
    soup = bs(r.text, 'lxml')

    try:

      data = soup.select('article.scholarshipDetails_stripCell__24-Hq span')
      if data:
        title = soup.select_one('article#applybtn>ul>li>h5').text.strip()
        eligibility = data[0].text.strip().replace('Eligibility', '')
        region = data[1].text.strip().replace('Region', '')
        benefits = data[2].text.strip().replace('Award', '')
        deadline = data[3].text.strip().replace('Deadline', '')
        offi_web = 'Too much data! Please refer the given URL.'
        source = source
        category = category
        data_dict = {
            'title' : title,
            'eligibility' : eligibility,
            'region' : region,
            'benefits' : benefits,
            'deadline' : deadline,
            'url' : url,
            'offi_web' : offi_web,
            'source' : source,
            'category' : category
        }

        return data_dict

      else:
        selector = soup.select('article#applybtn>ul>li')
        data_dict_list = []


        for i in range(len(selector)):
            source = source
            category = category
            title = selector[i].h5.text.strip()
            region = 'N/A'
            offi_web = 'Too much data! Please refer the given URL.'
            deadline = selector[i].select_one('span.brandScholarshipDetails_calendarIcon__2-5hX').text.strip().replace('Deadline', '')

            if selector[i].select_one('div.brandScholarshipDetails_overFlowHeight__7M-m1>p'):
              eligibility = selector[i].select_one('div.brandScholarshipDetails_overFlowHeight__7M-m1>p').text.strip()
              benefits = selector[i].select_one('div.brandScholarshipDetails_benefitsDiv__1z_wr>p').text.strip()

            else:
              eligibility = 'Too much data! Please refer the given URL.'
              benefits = 'Too much data! Please refer the given URL.'

            data_dict = {
                'title' : title,
                'eligibility' : eligibility,
                'region' : region,
                'benefits' : benefits,
                'deadline' : deadline,
                'url' : url,
                'offi_web' : offi_web,
                'source' : source,
                'category' : category
            }

            data_dict_list.append(data_dict)

        return data_dict_list
    
    except (IndexError, AttributeError) as e:
      print("Error :- ", e, " occured in url : ", url)
      return




def s4d_schols_data(url, source, category):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Accept-Language' : 'en-GB,en;q=0.5',
    'Referer' : 'https://google.com',
    'DNT' : '1'
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    
    soup = bs(r.text, 'lxml')

    data = soup.select('div.post')

    try:

      if data:
        title = soup.select_one('div.post>h1').text.strip()
        eligibility = 'Too much data! Please refer the given URL.'
        region = soup.select_one('div.entry>div.post_column_1:nth-of-type(2)>p').text.splitlines()[1].replace('Study in: ', '').strip()
        benefits = 'Too much data! Please refer the given URL.'
        deadline = soup.select_one('div.entry>div.post_column_1:nth-of-type(2)>p').text.splitlines()[0].replace('Deadline:', '').replace('(Annual)', '').strip()
        offi_web = soup.select_one('div.entry>p:nth-last-child(2)>a').text.strip()
        source = source
        category = category
        data_dict = {
            'title' : title,
            'eligibility' : eligibility,
            'region' : region,
            'benefits' : benefits,
            'deadline' : deadline,
            'url' : url,
            'offi_web' : offi_web,
            'source' : source,
            'category' : category
        }

        return data_dict
      
      else:
        return
    
    except (IndexError, AttributeError) as e:
      print("Error :- ", e, " occured in url : ", url)
      return


    
def bud4stud(headers, link, source, category):
    
    init = time()
    results = []
    
    r = requests.get(link, headers=headers)
    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    

    soup = bs(r.text, 'lxml')

    if soup.select_one('ul.rc-pagination'):
      print('Success! Pagination div found. Multiple pages available.')

      total_pages = int(soup.select_one('ul.rc-pagination>li:nth-last-child(3) a').text)
    else:
      total_pages = 1
      print('Pagination div not found')
    
    print('Total main pages available :- ', total_pages)

    for page in range(1, total_pages + 1):
        count = 0
        print('Getting main page ', page)
        urls = b4s_get_page_links(link, source, page)

        if type(urls) == type(None):
          print(f'Page - {page} returned no urls, Thus skipping to next page.')
          continue

        print(f'Total pages/urls available to crawl on main page {page} :- ', len(urls))
        
        
        for url in urls:
          count += 1
          print("Crawling data - Page : ", count, "Page URL :- ", url)
          data_received = b4s_schols_data(url, source, category)

          
          if (type(data_received) == dict):
            results.append(data_received)

          
          elif(type(data_received) == list):
            results.extend(data_received)
          
          elif(type(data_received) == type(None)):
            print(f'URL - {url} returned no scholarship data, Thus skipping to next Scholarship.')
            continue

          sleep(randint(2,10))

            
        print(f'Total results in page - {page} : ', len(results))

    print('Total results: ', len(results))
    
    print('Overall time : ', time() - init )
    return results



def schol4dev(headers, link, source, category):
    
    init = time()
    results = []
    
    r = requests.get(link, headers=headers)
    if r.status_code == 200:
      Status_OK = True
      print('Success! Page Reachable!')
    else:
      Status_OK = False
      print('Failure! Page Unreachable!')
      return
    

    soup = bs(r.text, 'lxml')

    if soup.select_one('div.wp-pagenavi'):
      print('Success! Pagination div found. Multiple pages available.')
      total_pages = int(soup.select_one('div.wp-pagenavi>span.pages').text.strip().rsplit(' ', 1)[1].strip())
    else:
      total_pages = 1
      print('Pagination div not found')
    
    print('Total main pages available :- ', total_pages)

    for page in range(1, total_pages + 1):
        count = 0
        print('Getting main page ', page)
        urls = s4d_get_page_links(link, source, page)

        if type(urls) == type(None):
          print(f'Page - {page} returned no urls, Thus skipping to next page.')
          continue

        print(f'Total pages/urls available to crawl on main page {page} :- ', len(urls))
        
        
        for url in urls:
          count += 1
          print("Crawling data - Page : ", count, "Page URL :- ", url)
          data_received = s4d_schols_data(url, source, category)

          
          if (type(data_received) == dict):
            results.append(data_received)

          
          elif(type(data_received) == type(None)):
            print(f'URL - {url} returned no scholarship data, Thus skipping to next Scholarship.')
            continue
          

          sleep(randint(2,10))

            
        print(f'Total results in page - {page} : ', len(results))
    print('Total results: ', len(results))
    print('Overall time : ', time() - init )
    return results



def main(code):

    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36',
    'Accept-Language' : 'en-GB,en;q=0.5',
    'Referer' : 'https://google.com',
    'DNT' : '1'
    }

    if code == 'b4s_gov_uc':
      link = 'https://www.buddy4study.com/upcoming-scholarships/nsp'
      source = 'https://www.buddy4study.com'
      category = 'government_upcoming'
      results = bud4stud(headers, link, source, category)

    elif code == 'b4s_girls':
      link = 'https://www.buddy4study.com/scholarships/girls'
      source = 'https://www.buddy4study.com'
      category = 'girls'
      results = bud4stud(headers, link, source, category)

    elif code == 'b4s_girls_ao':
      link = 'https://www.buddy4study.com/open-scholarships/girls'
      source = 'https://www.buddy4study.com'
      category = 'girls_always_open'
      results = bud4stud(headers, link, source, category)

    elif code == 'b4s_girls_uc':
      link = 'https://www.buddy4study.com/upcoming-scholarships/girls'
      source = 'https://www.buddy4study.com'
      category = 'girls_upcoming'
      results = bud4stud(headers, link, source, category)

    elif code == 'b4s_international':
      link = 'https://www.buddy4study.com/scholarships/study-abroad'
      source = 'https://www.buddy4study.com'
      category = 'international'
      results = bud4stud(headers, link, source, category)

    elif code == 'b4s_international_ao':
      link = 'https://www.buddy4study.com/open-scholarships/study-abroad'
      source = 'https://www.buddy4study.com'
      category = 'international_always_open'
      results = bud4stud(headers, link, source, category)

    elif code == 's4d_international':
      link = 'https://www.scholars4dev.com'
      source = 'https://www.scholars4dev.com'
      category = 'international'
      results = schol4dev(headers, link, source, category)
  
    # link = 'https://www.buddy4study.com/scholarships'
    # link = 'https://www.buddy4study.com/upcoming-scholarships'
    
    
    if (type(results) == type(None)) or (len(results) == 0):
      return
    
    else:
      return results

