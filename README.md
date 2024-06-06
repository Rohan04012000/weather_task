# weather_task
1. Python and Flask framework is used.
2. A standard user detail is encoded in the code. As,
   {
     "username":"user_1",
     "password::"123456"
   }
user_1 and 123456 are the values already encoded in the code.

# Endpoint Login API, To test the Login API where the app is live, send a ['POST'] request with the username and password using Postman.
https://weather-task-3e22.onrender.com/login_info

Note: The method should be ['POST'], and in the body, use JSON format. Like below,
{
  "username":"user_1",
  "password":"123456"
}
Send the request, and authentication will be handled. 
Important: copy the generated access_token (excluding the double quotes).

# Endpoint for logout API, To test Logout API send request using copied access_token using Postman.
https://weather-task-3e22.onrender.com/user_logout

STEPS: 1.Remove the content of the Body.
      2. Change POST to GET, and change the endpoint to the logout endpoint. 
Most importantly, click on Authorization, select Bearer Token from the Auth Type dropdown, and paste the copied access_token into the Token field on the right side. Then, send the request.

# Endpoint for Get weather information API.
https://weather-task-3e22.onrender.com/weather_api

STEPS: 1. Remove any content in the Body. 
       2. Change the endpoint to weather_api.
       3. Click on Params. Under Key, write page_no (in lowercase), and in Value, enter the page number you want to see. Then, send the             request.
eg:  Key    Value
    page_no   1

This request will give the first page with 10 cities and their details. Value can be 1,2, or 3. 

# Additional Endpoint for checking the logged user, follow same steps as Logout API, but change the Endpoint.
https://weather-task-3e22.onrender.com/current_user

# NOTE:
The generated access_token remains valid for 1 hour, after which it expires. The data is updated automatically every 30 minutes, without calling the weather_api.



