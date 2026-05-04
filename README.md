# Assurity - code for API response validation.

## API -  https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false

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
3. 

### How to run the test.

1. clone the repo
2. activate the virtual Env
3. run the assurity.py




