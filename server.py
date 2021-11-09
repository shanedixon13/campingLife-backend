from re import DEBUG
from flask import Flask, abort, render_template, request
from mock_data import mock_data
from flask_cors import CORS
from config import db, json_parse
import json
from bson import ObjectId

app = Flask(__name__) #two umderscore(double) (magic methods,functions,variables)
CORS(app) #allow anyone to call the server (**DANGER, ONLY FOR DEVELOPMENT PLEASE REMOVE)


coupon_codes=[
    {
        "code":"qwerty",
        "discount":10
    }
]


me = {
    "firstname":"Shane",
    "lastname":"Dixon",
    "email":"shanedixon13@gmail.com",
    "age":"25",
    "hobbies":[],
    "address":{
        "street":"Bradley Ln.",
        "city":"Lonoke"
    }

}


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    #return the full name 
    return render_template("about.html")


@app.route("/about/email")
def email():
    return me["email"]

@app.route("/about/address")
def address():
    return me["address"]["street"]+" " + me["address"]["city"]

@app.route("/test")
def simple_test():
    return "Hello There"




    ########################################################
    ############## API Methods
    ########################################################


@app.route("/api/catalog") #method by default is get
def get_catalog():
    #returns the catalog as JSON string
    #return json.dumps(mock_data)
    cursor =db.products.find({})#find with no filter = get all the data in the collection
    catalog=[]
    for prod in cursor:
        catalog.append(prod)

    print(len(catalog), "Records obtained from db")

    return json_parse(catalog)#error

@app.route("/api/catalog", methods=["post"])
def save_product():
    # get request paylaod
    #import request
    product=request.get_json()

    #data validation
    #1 title exists and is longer than 5 charactors
    #validate that the title exists in the dictionary, if nor abort 400
    if not "title" in product or len(product["title"])<5:
        return abort(400, "Title is required and should contain at least five charactors")
        #400=bad request

    #validate price exists and is above zero
    if not 'price' in product:
            return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"],int):
        return abort(400, "Price should a valid number")

    if product['price'] <= 0:
        return abort(400,"Price should be greater than 0")


         #save the product
    db.products.insert_one(product)
    
    #return the saved product
    return json_parse(product)
    


    return "testing"

## /api/categories
#return the list (string) of unique catagories
@app.route("/api/categories")
def get_categories():
    cursor =db.products.find({})
    categories=[]
    for product in cursor:
        if  product["category"] not in categories:
            categories.append(product["category"])
    return json_parse(categories)


@app.route("/api/product/<id>")
def get_product(id):
    product =db.products.find_one({"_id":ObjectId(id)})
    if not product:    
        return abort(404)#not found
    
    return json_parse(product)
        


@app.route("/api/catalog/<category>")
def get_category(category):
    cursor =db.products.find({"category":category})
    products=[]
    for prod in cursor:
       products.append(prod)
    return json_parse(products)



    #cheapest product
@app.route("/api/cheapest")
def get_cheapest():
    cursor =db.products.find({})
    cheapest=cursor[0]
    for product in cursor:
        if product["price"] < cheapest["price"]:
            cheapest=product
    return json_parse(cheapest)

    
##################################################################
##################Coupon Codes####################################
##################################################################

#POST to /api/couponCodes
@app.route("/api/couponCodes", methods=["post"])
def save_coupon():
    coupon = request.get_json()
    
    #validations

    #save
    db.couponCodes.insert_one(coupon)
    return json_parse(coupon)





#GET to /api/couponCodes
@app.route("/api/couponCodes")
def get_coupon_codes():
    cursor=db.couponCodes.find({})
    all_coupons=[]
    for cp in cursor:
        all_coupons.append(cp)
    return json_parse(all_coupons)


#get coupon by its code
@app.route("/api/couponCodes/<code>")
def get_coupon(code):
    coupon=db.couponCodes.find_one({"code": code})
    if code is None:
        return abort(404)
    return json_parse(coupon)



#This is to only be ran at the beginning to fill the DB
@app.route("/test/onetime/filldb")
def fill_db():
    #iterate the mock_data
    for prod in mock_data:
        #push every object to db.propducts
        prod.pop("_id")#remove the _id from dict before sending
        db.products.insert_one(prod)
    return "Done!"
    




#start the server
#debug true will restart the server on manipulation
app.run(debug=True)