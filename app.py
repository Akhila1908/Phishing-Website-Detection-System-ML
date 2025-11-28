from flask import Flask, render_template, request
import pickle
import re
import os

app = Flask(__name__)

# Use relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vector = pickle.load(open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'rb'))
model = pickle.load(open(os.path.join(BASE_DIR, 'phishing.pkl'), 'rb'))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        url = request.form['url']
        
        cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
        
        predict = model.predict(vector.transform([cleaned_url]))[0]
        
        if predict == 'bad':
            predict = "This is a Phishing website !!"
        elif predict == 'good':
            predict = "This is healthy and good website !!"
        else:
            predict = "Something went wrong !!"
        
        return render_template("index.html", predict=predict)
    
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
