from flask import Flask
from flask import jsonify
from contact import contact_bp
from request_example import request_example_bp

app = Flask(__name__)

@app.before_request
def before():
    print("This is executed BEFORE each request.")
    

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/increment/<int:number>/')
def incrementer(number):
    return "Incremented number is " + str(number+1)

@app.route('/hello/<string:name>/')
def hello(name):
    return "Hello " + name

@app.route('/person/')
def person():
    return jsonify({'name':'Jimit',
                    'address':'India'})

@app.route('/numbers/')
def print_list():
    return jsonify(list(range(5)))

@app.route('/home/')
def home():
    return "Home page"

@app.route('/contact')
def contact():
    return "Contact page"

@app.route('/teapot/')
def teapot():
    return "Would you like some tea?", 418


app.register_blueprint(contact_bp, url_prefix='/contact')
app.register_blueprint(request_example_bp, url_prefix='/requestExample')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)