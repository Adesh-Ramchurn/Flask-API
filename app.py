import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)

# stores = [
#     {
#         "id": 12,
#         "name": "My Store",
#         "items": [
#             {
#                 "name": "Chair",
#                 "price": "12"
#             },
#             {
#                 "name": "Table",
#                 "price": "200"
#             },
#             {
#                 "name": "Gazebo",
#                 "price": "100"
#             }  
#         ]
        
#     }
# ]



@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")

@app.post("/store")
def create_store():
    store_data = request.get_json()
    
    if "name" not in store_data:
        abort(400, message="Bad request, name must be included")
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message= "store already exists")
    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def create_item():
    item_data = request.json
    
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400, message = "bad request, need price, store_id and name")
      
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="duplicate data")
            
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
        
    item_id = uuid.uuid4().hex
    
    item = {**item_data, "id": item_id}
    items[item_id] =  item
    return {"items": list(items.values())}


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}     


@app.get("/item/<string:item_id>") # using id to add items to the correct store
def get_item(item_id):
    
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")




# @app.post("/store/<int:id>/item") # using id to add items to the correct store
# def add_items(id):
#     request_data = request.get_json() # grab the incoming json
    
#     for store in stores:
#         if store["id"] == id:
#             new_item = {"name": request_data["name"], "price": request_data["price"]}
#             store["items"].append(new_item)
#             return new_item
        
#     return {"message": "Store not found"}, 404

# @app.post("/store/<string:store_id>") # using id to add items to the correct store
# def get_store(store_id):
#     request_data = request.get_json() # grab the incoming json
    
#     try:
#         return stores[store_id]
#     except KeyError:
#         return {"message": "Store not found"}, 404



# @app.post("/store/<string:name>/")
# def create_item(name):
#     request_data = request.get_json()
    
#     for store in stores:
#         if store["name"] == name:
#             add_item = {"name": request_data["name"], "price": request_data["price"]}
#             store["items"].append(add_item)
#             return add_item
    
#     return {"message": "Store not found"}, 404
    
