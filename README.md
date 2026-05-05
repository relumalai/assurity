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
7. or you could run the github action

And seccond approch is also added and the implemetation is under the approach-v2 folder
The apprach implements 
- validation using jmespath (jq equivalent for querying json, especially used for nested json.)
- validation using pydantic. A partial define model is defined and the response is check against this model. Pydantic enforces strict validate of the response againg the model.
- Validation using native python. Same as validateapi.py


├── approach2
│   ├── JmespathValidator.py - jmespath implementation of validations
│   ├── models.py            - pydantic model (partial, generated from response in absense of api schema)
│   ├── nativevalidation.py  - Native implementation of the validation
│   ├── PydanticValidator.py - Pydantic implementation of the validation
│   ├── runvalidation.py    - Simple test calling 
│   └── validateapi_core.py - Core Orchestrating class inheriting native,pydatic and jmespath class
├── LICENSE
├── lintreport.txt
├── README.md
├── requirements.txt
└── validateapi.py    

8. run approach-v2/runvalidations.py

