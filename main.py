from flask import Flask, render_template, request,session, jsonify, redirect, url_for
import openai
import json
from bs4 import BeautifulSoup

import requests
json
import re,os,csv
from datetime import datetime


# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')
# from google_bard_api import user_msg
app = Flask(__name__)



# Define a function to process user queries


@app.route('/')
def index():
    return render_template('chat.html')
@app.route('/schools')
def schools():
    return render_template('schools.html')

@app.route('/universities')
def univerities():
    return render_template('universities.html')

def format_text(text):
    # Bold text within double asterisks
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Underline text within double underscores
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
    
    # Replace new lines with '' tags
    text = text.replace('\n', "<br>")
    
    return text


# Define a function to process user queries
@app.route('/universities_cities', methods=['POST'])
def get_universities_cities():
    country = request.form['country']
    print(country)
    # Fetch states from the respective API based on the selected country
    if country == 'India':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/india_university_data.json')
    elif country == 'Pakistan':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/pakistan_university_data.json')
    elif country == 'Saudi-Arabia':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/saudi_arabia_university_data.json')
    elif country == 'UK':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/united_kingdom_university_data.json')
    elif country == 'Australia':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/Australia_university_data.json')
    elif country == 'UAE':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/UAE_university_data.json')
    
    else:
        return jsonify(states=[])  # Return empty list if country is not recognized
    if response.status_code == 200:
        data = response.json()
        
            # Extract states from the API response
        # degree_type = [
        #                 "Master of Science",
        #                 "Master of Arts",
        #                 "Master of Business Administration",
        #                 "Master of Laws",
        #                 "Master of Philosophy",
        #                 "Master of Letters",
        #                 "Master of Research",
        #                 "Master of Education",
        #                 "Master of Engineering",
        #                 "Postgraduate Diploma",
        #                 "Postgraduate Certificate",
        #                 "Pre-Master"
        #             ]
        degree_types= [
                {
                    "option_value": "msc",
                    "text": "Master of Science"
                },
                {
                    "option_value": "ma",
                    "text": "Master of Arts"
                },
                {
                    "option_value": "mba",
                    "text": "Master of Business Administration"
                },
                {
                    "option_value": "llm",
                    "text": "Master of Laws"
                },
                {
                    "option_value": "mphill",
                    "text": "Master of Philosophy"
                },
                {
                    "option_value": "mlitt",
                    "text": "Master of Letters"
                },
                {
                    "option_value": "mres",
                    "text": "Master of Research"
                },
                {
                    "option_value": "med",
                    "text": "Master of Education"
                },
                {
                    "option_value": "meng",
                    "text": "Master of Engineering"
                },
                {
                    "option_value": "postgraddip",
                    "text": "Postgraduate Diploma"
                },
                {
                    "option_value": "postgradcert",
                    "text": "Postgraduate Certificate"
                },
            #     {
            #         "option_value": "premaster",
            #         "text": "Pre-Master"
            #     }
            ]
        

        
        return jsonify(degree_types=degree_types)
    else:
        return jsonify(degree_types=[])
    

@app.route('/universities_search', methods=['POST'])
def uni_search():
    
    country = request.form.get('country')
    degree_type = request.form.get('degree_type')
    print(country)
    print(degree_type)
    if country=='Pakistan':
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-129|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/pakistan_university_data.json')
        data2 = response2.json()
   
    if country=='India':
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-108|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/india_university_data.json')
        data2 = response2.json()
     
    if country=='Australia':
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-202|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/Australia_university_data.json')
        data2 = response2.json()
        
    if country=='UK':
        
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-30|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/united_kingdom_university_data.json')
        data2 = response2.json()
      
    if country=='UAE':
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-140|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/UAE_university_data.json')
        data2 = response2.json()
        # print(data)
        # Filter records based on the city
    
    if country == 'Saudi-Arabia':
        response = requests.get(f'https://search.prtl.co/2023-02-23/?q=en-1546|dg-{degree_type}|ci-132|lv-master|tc-EUR|uc-108&size=100&start=0')
        data = response.json()
        response2 = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/universities/saudi_arabia_university_data.json')
        data2 = response2.json()
        # Filter records based on the city
    # print(data)
    # school_records = [record for record in data if city in record.get('address').split('\n')]
    
    school_records = []
    for entry in data:
        course = entry.get('card').get('func').get('getTitle')  # Extract course title
        
        university_info = entry.get('card').get('func').get('getUniversityLink')
        university_name = university_info.get('func').get('getDescription')  # Extract university name
        
        # Search for university details in data2
        website=None
        for uni_entry in data2:
            if uni_entry.get('title') in university_name:
                website = uni_entry.get('website_url')
                phone = uni_entry.get('phone')
                about = '\n'.join(uni_entry.get('description').split('\n')[:2])
                break  # Once found, no need to continue searching
        if website:
            city = entry.get('card').get('func').get('getLocation').get('func').get('getCity').get('func').get('getDescription')
            try:
                tuition_fee = entry.get('card').get('func').get('getTuitionFees')[0].get('func').get('getAmount')
            except:
                tuition_fee=''
            try:
                getCurrency = entry.get('card').get('func').get('getTuitionFees')[0].get('func').get('getCurrency')
            except:
                getCurrency=''
            record = {
                'course': course,
                'university_name': university_name,
                'website': website,
                'phone': phone,
                'about': about,
                'city': city,
                'tuition_fee': f"{tuition_fee} {getCurrency}"  # Corrected 'tution_fee' to 'tuition_fee'
            }
            
            school_records.append(record)

    # print(school_records)

    
    # for record in data:
    #     # print(city,record.get('address').split('\n')[1])
    #     if city.strip() in record.get('address').split('\n')[1]:
            
    #         school_records.append(record)
    # # school_records = [record for record in data if city.strip().lower() in record.get('address').split('\n')[1].lower()]
    # print(school_records)
    return jsonify({'uni_records': school_records})
   
# Define a function to process user queries
@app.route('/school_cities', methods=['POST'])
def get_school_cities():
    country = request.form['country']
    # Fetch states from the respective API based on the selected country
    if country == 'India':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/india_schools.json')
    elif country == 'Pakistan':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/pakistan_schools.json')
    elif country == 'UAE':
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/UAE_schools.json')
    else:
        return jsonify(states=[])  # Return empty list if country is not recognized
    if response.status_code == 200:
        data = response.json()
        
            # Extract states from the API response
        city = list(set([school['city'] for school in data]))
        print(city)
        return jsonify(city=city)
    else:
        return jsonify(city=[])
    
@app.route('/school_search', methods=['POST'])
def school_search():
    
    country = request.form.get('country')
    city = request.form.get('city')
    print(country)
    print(city)
    if country=='Pakistan':
        city = request.form.get('city')
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/pakistan_schools.json')
        data = response.json()
        # print(data)
        # Filter records based on the city
        school_records = [record for record in data if record.get('city') in city]
        print(school_records)
        return jsonify({'school_records': school_records})
    if country=='India':
        city = request.form.get('city')
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/india_schools.json')
        data = response.json()
        # print(data)
        # Filter records based on the city
        school_records = [record for record in data if record.get('city') in city]
        print(school_records)
        return jsonify({'school_records': school_records})
    if country=='UAE':
        city = request.form.get('city')
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/schools/UAE_schools.json')
        data = response.json()
        # print(data)
        # Filter records based on the city
        school_records = [record for record in data if record.get('city') in city]
        # print(school_records)
        return jsonify({'school_records': school_records})
    # Perform further actions based on the selected category, country, and city
    # Dummy response data for demonstration
    search_results = [{'name': 'Result 1'}, {'name': 'Result 2'}, {'name': 'Result 3'}]
    return jsonify({'search_results': search_results})

@app.route("/store_data", methods=["POST"])
def store_data():
    # Get form data
    print(request.form)
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    message = request.form.get("message")
    universities = request.form.getlist("universities[]")  # Get universities as a comma-separated string
    print(universities)
    # universities = universities_string.split(',') if universities_string else []  # Convert string to list
    # print(universities)
    # Store data in CSV file
    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, email, message] +  ", ".join(universities))

    return "Data stored successfully"

@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    
    section=request.get_json().get('section')
    # Save section in session
    if section:
        session['section'] = section
    print('session',session['section'])
    user_message1 = request.get_json().get('userMessage')
    print(user_message1)

    log_data = {'user_query': section}
    
    
    if session['section']=='China MBBS Courses':
        
          
        response = requests.get('https://myeducation001.s3.eu-north-1.amazonaws.com/courses/china_MBBS_courses.json')
        # Log the AI response
        if response.status_code == 200:
            courses_data = response.json()

            course_cards = []

        for course in courses_data:
            course_title = course['Course']
            university = course['university']
            course_url = course['url']
            description = course['Description']
            application_fee = course['application_fee']
            application_deadline = course['application_deadline']
            
            card_html = f"""
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title"><strong>{course_title}</strong></h5>
                    <h6 class="card-subtitle mb-2 text-muted">{university}</h6>
                    <p class="card-text">{description}</p>
                    <p class="card-text">Application Fee: {application_fee}</p>
                    <p class="card-text">Application Deadline: {application_deadline}</p>
                    <a href="{course_url}" class="btn btn-primary">Apply Now</a>
                </div>
            </div>
            """
            
            course_cards.append(card_html)
        if course_cards:
            output = "".join(course_cards)
        else:
            output = 'Something Wrong'
    
        return jsonify({'aiResponse': output})
        
          
    
    if session['section']=='Support a Student':
    #     print('data')
        if user_message1:
            output='Your response is recieved. Consern team will reply soon'
        else:
            output='Please write down your consern in one note'
        return jsonify({'aiResponse': output})
if __name__ == '__main__':
    
    app.secret_key = os.urandom(24)  # Use a more secure method to generate a secret key
    app.config['SESSION_TYPE'] = 'filesystem'  # Choose an appropriate session type
    # app.run(debug=True,port=5000)
    app.run(host='0.0.0.0', port=3000,debug=True)










