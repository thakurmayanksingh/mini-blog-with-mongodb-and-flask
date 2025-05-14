from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import datetime

# flask app instance
app = Flask(__name__)

# connecting to my local client
client = MongoClient("mongodb://127.0.0.1:27017")

# setting up db and collection
db = client['miniblog']
collection = db['blogs']

@app.route('/', methods=['GET', 'POST'])

def index():
    # checking for form submission
    if request.method == 'POST':
        # fetching name and thoughts
        name = request.form.get("name")
        thoughts = request.form.get("blog_content")

        # validating input
        if name and thoughts:
            collection.insert_one({"name": name,
                                   "content": thoughts,
                                   "timestamp": datetime.datetime.now()})
            return redirect('/')
    
    return render_template("form.html")

@app.route('/view_blogs')
def view_blogs():
    blogs = collection.find().sort("timestamp", -1)
    return render_template("view_blogs.html", blogs=blogs)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    
    except Exception as e:
        print(f"Error: {e}")