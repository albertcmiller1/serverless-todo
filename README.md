# serverless-todo
this repo will act as a boiler plate for a full stack serverless app using create-react-app frontend and API Gateway, Lambda, and DynamoDB AWS backend


## frontend 
```
cd serverless-todo-frontend && npm start
```


## backend 
```
sam build
sam deploy --guided
sam delete --stack-name <stack-name>
```



export URL="https://xgrmbxql1h.execute-api.us-east-1.amazonaws.com/Prod"

* post a product 
curl -X POST ${URL}/product -H "Content-Type: application/json" -d '{"productId": "001", "name": "lucky_charms"}'  


* get all products 
curl -X GET ${URL}/products    
