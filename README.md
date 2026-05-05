# Assurity - code for API response validation.

### API -  https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false

### Validate response for

1. Name = "Carbon credits"
2. CanRelist = true
3. Element Promotion with Name = "Gallery" has the following Description (text) "Good Position in category"


### packages used solution

Requests - interact with the api endpoint, parse the response and vaidate the above 3 conditions with proper exception handling.  
jmespath - Alternativly use a json parser to validate the conditions.
pydantic - A more robust validation method. I the absense of schema, i will assume a sample one.

### Assumptions

1. The code is being run on Windows/Linux/MacOS with python version > 3.10, and pip
2. Has access to internet to downlaod the necessary packages.

### How to run the test.

1. clone the repo
2. If you are using a virtual environment for python, activate it.
3. create a .env file as below
   
   BASE_URL= "https://api.tmsandbox.co.nz/v1"
   
   CATALOGUE= false
   
   CATEGORY_ID= 6327
   
   
5. run python -m pip install -r requirements.txt
6. Run validateapi.py
