# serverless-todo
this repo will act as a boiler plate for a full stack serverless app using create-react-app frontend and AWS SAM backend. 


# Frontend 
```
npm install 
npm start
```

# Backend 
```
sam build
sam deploy --guided
sam delete --stack-name <stack-name>
```

**set var**
```
export URL="https://xgrmbxql1h.execute-api.us-east-1.amazonaws.com/Prod"
```
**say hello**
```
curl https://8n2raxwpo9.execute-api.us-east-1.amazonaws.com/Prod/hello/ 
```

**post a product**
```
curl -X POST ${URL}/product -H "Content-Type: application/json" -d '{"productId": "001", "name": "lucky_charms"}'  
```

**get a product** 
```
curl -X GET https://1tq1ucacxe.execute-api.us-east-1.amazonaws.com/Prod/product\?productId=002
```

**delete a product** 
```
curl -X DELETE ${URL}/product -H "Content-Type: application/json" -d '{"productId": "002"}'
```

**get all products**
```
curl -X GET ${URL}/products    
```