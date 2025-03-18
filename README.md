# Roller Coaster Search App
## Description:
A prototype web app that manages a users roller coaster interests. Uses an API from Captian Coaster that allows for real time data on roller coasters. Uses four different microservices to allow searching of coasters, customizing UI and communicating via http.
## Programs:
### General
The main program is run on python using flask for backend, and relies on html and javascript for the pretty UI. The pages are templatized for easy modification. Communicates with each microservice via http requests
![image](https://github.com/user-attachments/assets/96f38124-fb04-46e3-a7d6-21219ddb402d)
![image](https://github.com/user-attachments/assets/3554f485-0d6e-47f0-92a6-8a3c192fc773)
### API Microservice
This handle all interactions with the API. Grabs the data, and serves it to the main Program. Has two three methods
 - /fetch: upon starting the server will fetch all the roller coaster data from Captain Coaster
 - /find/: with a proper coaster ID, will retrieve the coaster detailed info
 - /name/: with name of coaster, will retrieve coaster info
### Customize Microservice
This allows the main program to retireve a random set of colors. Microservice calculates appropriate colors that work well together.
![image](https://github.com/user-attachments/assets/2e52e140-ac25-4e28-a8ed-65f6df84f6a7)
![image](https://github.com/user-attachments/assets/ddcfd5cf-f71c-4d06-8388-34e94e300ca3)
![image](https://github.com/user-attachments/assets/41b87f79-8fc6-4702-a01b-1d28344e2a87)
### String Correction Microservice
Changes the "operating" string to better format on the UI.
### Random Number Microservice
Code provided and made by Eugenia Uvarov. Gives a random number to main program, allowing random population

