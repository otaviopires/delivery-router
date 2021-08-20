# Delivery-Router

A Serverless Python Flask API using AWS Lambda, API Gateway and DynamoDB

## Pre requisite

## Usage

### Prerequisites

```bash
python3.8 -m venv ./venv
source ./venv/bin/activate
```

### Deployment
```
$ npm install -g serverless
$ serverless login
$ npm i
$ sls deploy
```

Once the deploy is complete, run `sls info` to get the endpoint:

```
$ sls info
Service Information
<snip>
endpoints:
  ANY - https://0zqktyxmvh.execute-api.sa-east-1.amazonaws.com/dev
  ANY - https://0zqktyxmvh.execute-api.sa-east-1.amazonaws.com/dev/{proxy+}
```

Copy paste into your browser, and _voila_!

### Already deployed on AWS


Just navegate to the URL and enjoy yourself!
```
 https://0zqktyxmvh.execute-api.sa-east-1.amazonaws.com/dev
```

### Local development

To develop locally, create a virtual environment and install your dependencies:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, run your app:

```
sls wsgi serve
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

Navigate to [localhost:5000](http://localhost:5000) to see your app running locally.


---
## Postman collection

Import the contents of postman folder and run the collection using LOCAL and DEV.

Obs.: DEV enviroment is set to a AWS url on my personal account.


---
## Stack

- Serverless Framework
- Python 3.6
- Flask
- AWS Lambda
- AWS API Gateway
- AWS DynamoDB
- Postman