from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

role = input('which roll you looking for (ex:Data Engineer):').strip()
place = input('Give the city or state name (ex:chennai, Tamil Nadu):').strip()
page_number = input('how many pages you want to scrape:(ex:4):').strip()

with sync_playwright() as a:
  browser = a.chromium.launch(headless=False,slow_mo=50)
  page = browser.new_page()
  page.goto('https://in.indeed.com/jobs?q='+role+'&l='+place+'&radius=50&start='+str(page_number*10)+'&vjk=')

  page.is_visible('div.css-jvh80z eu4oa1w0')
  content = page.content() 
 
  with open('content.html' ,'w',encoding='utf-8')as f:
   f.write(content)
   doc=BeautifulSoup(content,'lxml')
   outer = doc.find('div',{'class':'mosaic mosaic-provider-jobcards'})


indeed_posts=[]
for i in outer.find('ul'):

    jobtiitle = i.find('div',{'class':'css-dekpa e37uo190'})
    if jobtiitle !=None:
     jobtiitled = jobtiitle.find('span').text
     link = jobtiitle.find('a',{'class':'jcs-JobTitle css-jspxzf eu4oa1w0'})['href']
     joblink ='https://www.indeed.com'+link
   
    if i.find('div',{'class':'company_location css-17fky0v e37uo190'})!=None:
      location = i.find('div',{'class':'css-1qv0295 e37uo190'}).text
      company_name = i.find('div',{'class':'css-1p0sjhy eu4oa1w0'}).text

    if i.find('div',{'class':'css-1cvvo1b eu4oa1w0'})!=None: 
      salary = i.find('div',{'class':'css-1cvvo1b eu4oa1w0'}).text

    if i.find('div',{'class':'heading6 tapItem-gutter css-1rgici5 eu4oa1w0'})!=None:
      date = i.find('span',{'class':'css-qvloho eu4oa1w0'}).text

    indeed_posts.append({'joblink':joblink,
               'location':location,
               'company_name':company_name,
               'salary':salary,
               'date':date
               })
    job_df = pd.DataFrame(indeed_posts)
    print(job_df)
    df_string =job_df.to_string()
    with open('webscrape_output.txt','w',encoding='utf-8')as s:
      s.write(df_string)




    


 