import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)



@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")

@app.post("/store") # we first need  to create a store, we we must include a name of the store in the payload eg { "name" : "Kingsavers"}
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

@app.post("/item") # In order to create an item, we need a store id, which would be generated from the /post/store. we must pass in the store id the body of the payload eg {"name" : "", "price": "", "store_id": ""}
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
        

@app.delete("/item/<string:item_id>") # using id to delete items to the correct store
def del_item(item_id):
    
    try:
        del items[item_id]
        return {"message": "Item  has been deleted"}
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/store/<string:store_id>")
def del_store(store_id):
    
    try:
        del stores[store_id]
        return {"message": "store has been deleted  has been deleted"}
    except KeyError:
        abort(404, message="Store not found")
        
        



# app.put("/item/<string:item_id>")
# def edit_item(item_id):
#     item_data = request.get_json()
#     if "price" not in item_data or "name" not in item_data:
#         abort(400, message="Bad request. Ensure 'price', and'name' are included in the request")
    
#     try:
#         item = items[item_id]
#         item.update(item_data)  # Use update method for dictionaries
        
#         return item
#     except KeyError:
#         abort(404, message="Item not found")


@app.route("/item/<string:item_id>", methods=['PUT']) # new route for put as end url is the same as delete
def edit_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, description="Bad request. Ensure 'price' and 'name' are included in the request.")
    
    try:
        item = items[item_id]
        item.update(item_data)  # Use update method for dictionaries
        
        return item  # Return as JSON response
    except KeyError:
        abort(404, description="Item not found")
        
    
    


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
    
