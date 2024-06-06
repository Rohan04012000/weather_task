from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "12345" #For 12345, token will be created.Anything can be put in place of 12345.
jwt = JWTManager(app)

#API_KEY contains the key which was generated after creating account on Oneweather website.
API_KEY = "9fa3f47155541b1123fbbfbb8c0a0f06"
#This was the base url provided by Oneweather website to be used with API_KEY.
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

#List of Indian cities for which weather data to be requested.
list_of_Indian_cities = ["Delhi","Bengaluru", "Lucknow","Gorakhpur","Agra","Nagpur","Patna","Bhopal", "Mumbai", "Jodhpur",
          "Ahmedabad", "Hyderabad", "Pune", "Kanpur", "Kolkata", "Chennai", "Meerut", "Varanasi", "Vadodara", "Srinagar",
          "Coimbatore", "Madurai", "Mysore", "Dehradun", "Siliguri", "Ujjain", "Ranchi", "Vijayawada", "Kochi","Ajmer"]

weather_data_holder = [] #For holding weather data of 30 cities.
#weather_data_lock = threading.Lock()  # Lock for synchronizing access to weather_data_holder


#One user with username and password
One_user = {
        "username" : "user_1",
        "password" : "123456"
}

# Initialize the scheduler
scheduler = BackgroundScheduler()
#Function to load weather data and wait for next 30 minutes to update weather_data_holder.
def load_weather_data():
    global weather_data_holder
    print("Starting data fetch------")
    updated_data = []
    for city in list_of_Indian_cities:
        params = {
            'q': city,  # q stands for query and is used to specify city for which weather data is requested.
            'appid': API_KEY,  # appid is key and the value should be API_KEY created on Oneweather website.
            'units': 'metric'  # making units to metric means that the temperature will be returned in Celsius.
        }
        # Sending the GET request for each city.
        response = requests.get(BASE_URL, params = params)
        # Checking if the request was successful.
        if response.status_code == 200:
            updated_data.append(response.json())  # Appending the details.
        else:
            updated_data.append({'city': city, 'error': 'Could not fetch data'})

    weather_data_holder = updated_data  # Update weather_data_holder atomically
    print("weather data updated = ",weather_data_holder)
    print("Done waiting for 30 min.")

# Schedule the fetch_weather_data function to run every 30 minutes
scheduler.add_job(load_weather_data, 'interval', minutes = 1)
scheduler.start()
# Initial fetch
load_weather_data()


# Login API (creating token for one user based on secret_key "12345")
@app.route('/login_info', methods=['GET','POST'])
def login_info():
    #Login username and password should be sent in string format in POST request using Postman.
    if request.method == 'POST':
        #Checking if request contains JSON data or not.
        #If does not contain it will give error 440 i.e Bad request.
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        #Reading the data from JSON.
        user_name = request.json['username']
        pwd = request.json['password']

        #Validating if the data match with existing user.
        if user_name != One_user['username'] or pwd != One_user["password"]:
            return jsonify({"Error": "Invalid credentials"}), 401

        # Set the expiration time to 1 hour because our weather_data_holder is updating after 30 min.
        expires = timedelta(hours = 1)
        #access token for user_name = user_1 and by default it will be valid for 15 minutes.
        access_token = create_access_token(identity = user_name, expires_delta = expires)
        return jsonify(access_token = access_token, Message = "Copy the generated access_token!.")
    else:
        return jsonify({"Error":"Method should be POST."}), 405 #405 is to show wrong method.


#To return the existing user, through GET request.
@app.route("/current_user", methods=["GET","POST"])
@jwt_required()
def current_user():
    print("current user =  weather data holder",weather_data_holder)
    if request.method == 'GET':
        # Access the identity of the current user with get_jwt_identity
        current_user_name = get_jwt_identity()
        return jsonify(Logged_in_user_is = current_user_name), 200 #200 is to show a successful http requests.
    else:
        return jsonify({"Error":"Method other than GET is not allowed!."}), 405 #405 is for wrong method.


# Logout API (Endpoint for token-based authentication).
@app.route('/user_logout', methods=["GET","POST"])
@jwt_required()
def user_logout():
    if request.method == 'GET':
        logged_user_name = get_jwt_identity()
        return jsonify({"user":logged_user_name, "Message":"User logged off successfully!."})
    else:
        return jsonify({"Error":"Method other than GET is not allowed!."}), 405


#Weather API through API_KEY.
@app.route("/weather_api", methods = ['GET','POST'])
@jwt_required()
def weather_api():
    if request.method == 'GET':
        #This is to get the page number sent in url and by default it will considered the first page.
        page = int(request.args.get('page_no', 1))
        #Cities per page.
        per_page = 10
        #Logic to select 10 or next 10 cities based on page no entered.
        first_city = (page - 1) * per_page
        last_city = first_city + per_page

        paginated_page = weather_data_holder[first_city:last_city] #Slicing the cities as per page number.
        return jsonify({
            'page_no_is': page,
            'cities_per_page': per_page,
            'total_page': '3',
            'total_cities': len(list_of_Indian_cities),
            'weather_data': paginated_page
        })
    else:
        return jsonify({"Error":"Request should be sent using POST."})
#Comment this before deploying on render.com
#if __name__ == '__main__':
    #app.run()
