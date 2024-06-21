# candidate-search-poc

### Setup
Run the following command:
    pip install -r requirements.txt

Create a .env file in the root directory and copy and paste these variables:

OPENAI_KEY= 'YOUR_OPENAI_KEY'

BH_CLIENT_ID = 'FROM_POSTMAN_COLLECTION'
BH_USERNAME = 'FROM_POSTMAN_COLLECTION'
BH_PASSWORD = 'FROM_POSTMAN_COLLECTION'
BH_CLIENT_SECRET = 'FROM_POSTMAN_COLLECTION'
BH_REST_TOKEN=''
BH_REST_URL=''

### Running the App
To generate the values for 'BH_REST_TOKEN' and 'BH_REST_URL', run the following command:
    py config.py

To query against a new job description, paste the job description into the file 'data/posting.txt' 
Run the following command:
    py app.py