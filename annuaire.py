import requests
from bs4 import BeautifulSoup as bs
import string
import csv

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
            #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': 'gzip, deflate, br',
            "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            'Content-Type':'application/x-www-form-urlencoded'
            }


    
b=0      
letter = list(string.ascii_lowercase) 
with open('annuaire-scraper.csv','w', newline='') as f:
    for x in letter: 
        print('now starting with names beginning with ' + x + '...') 
        for p in range(0,50):
            r1 = requests.get('https://www.pages-annuaire.net/particuliers/ville/Nanterre/' + x + '?p=' + str(p), headers=headers)
            if r1.ok == True:       
                soup1 = bs(r1.content,features="lxml")
                anchors = soup1.select('div.col-md-3 ul li a')
                for i in anchors:
                    link = 'https://www.pages-annuaire.net' + i['href']
                    r2 = requests.get(link, headers=headers, allow_redirects=True)
                    if r2.ok == False:
                        print('error with link: ' + link)
                        print(r2)
                    else:
                        soup2 = bs(r2.content, features="lxml")
                        name = soup2.find('h1').text
                        adres = str(soup2.find('h2'))
                        print(adres)
                        adres = adres.replace('<h2>', '')
                        adres = adres.replace('</h2>', '')
                        adres = adres.replace('<br/>', ' ')
                        print(adres)
                        #phoneid = soup2.select("h2 ~ div.MER_block div")
                        #phoneid = phoneid[0]["data"].replace('=','')
                        #phonelink = 'https://www.pages-annuaire.net/ajax/getMERNumber?tag=F_RES_DSK_SEO&encodeData=' + phoneid + '%3D%3D'
                        #data = "tag=F_RES_DSK_SEO&encodeData=" + phoneid +  "%3D%3D"
                        #print(phonelink)
                        #print(data)
                        #r3 = requests.get(link, headers=headers, data=data)
                        #soup3 = bs(r3.content,features="lxml")
                        #print(r3.content)
                        #print('hoi')
                        w = csv.writer(f)
                        if b == 0:
                            w.writerow(['name', 'adress'])
                            b = 1
                        w.writerow([name,adres])

#https://www.pages-annuaire.net/ajax/getMERNumber?tag=F_RES_DSK_SEO&encodeData=MDE0Njk3MDQzNCMjWmFoaWEgQWFiYmFkaQ%3D%3D
#https://www.pages-annuaire.net/ajax/getMERNumber?tag=F_RES_DSK_SEO&encodeData=MDE0Njk3MDQzNCMjWmFoaWEgQWFiYmFkaQ%3D%3D

#tag=F_RES_DSK_SEO&encodeData=MDE0Njk3MDQzNCMjWmFoaWEgQWFiYmFkaQ%3D%3D
#tag=F_RES_DSK_SEO&encodeData=MDE0Njk3MDQzNCMjWmFoaWEgQWFiYmFkaQ%3D%3D