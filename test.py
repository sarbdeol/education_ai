from bs4 import BeautifulSoup

import requests
response = requests.get('https://search.prtl.co/2023-02-23/?q=en-1546|dg-msc|ci-30|lv-master|tc-EUR|uc-108&size=100&start=0')
data = response.json()

for i in data:
    course=i.get('card').get('func').get('getTitle')
    # print(course)
    univerity_name=i.get('card').get('func').get('getUniversityLink').get('func').get('getDescription')
    # print(univerity_name)

   
        # print(data)
    city=i.get('card').get('func').get('getLocation').get('func').get('getCity').get('func').get('getDescription')
    print(city)
    
    tution_fee=i.get('card').get('func').get('getTuitionFees').get('func').get('getAmount')
    
    website=''
    contact=''
    about_uni=''


response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/united_kingdom_university_data.json')
