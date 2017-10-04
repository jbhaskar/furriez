
fb login :

```
curl -X POST \
  http://localhost:5001/login \
  -H 'content-type: application/json' \
  -d '{ 
  "provider" : "facebook",
  "access_token" : "EAACEdEose0cBAPYABxZCAroZBJFcTiZApntaCpObkbZCfD3g65qhchebZCAiKkDjY0pMQjyVq5ZAqk0YlZAHgjZAjMjVKyodfNEKu4IyCcQ266XS1NHo6Yg93eYVDUTLvXj9vKqLAuf03w1ukZCNtbDdVysHxPKJCPuM5vbWj3iUvjGMcqKdUcNn2zZAxcrjRKnIQZD"
}'
```

response : 
```
{"access_token": "<jwt>"}
```

check jwt :
```
curl -X GET \
  http://localhost:5001/protected \
  -H 'authorization: Bearer <jwt>'
```


endpoints : 
```
GET: /article/:id 
GET: /question/:id
POST: /article
POST: /question
```

body for above POST requests should look like 
```{ 
  ...,
  data: {...},
  ...
}```

The data field gets stored in the data key of post(Mongo doc) created on successful insert.
Type of post is decided by the endpoint being hit.
Also each post has a owner associated with it which stores the user doc id.

response of all will be the whole post object
post object : 
```{
  owner_id: <user_id>,
  type: <1: article, 2: question>
  data: <data field from post request paylaod>
}```