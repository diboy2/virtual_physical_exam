from flask import Blueprint, request
request_example_bp = Blueprint('request_example', __name__)

# http://127.0.0.1:5000/query-example?language=Python
@request_example_bp.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)

# allow both GET and POST requests
@request_example_bp.route('/form-example', methods=['GET'])
def form_example():
    return '''
            <form method="POST">
                <div><label>Language: <input type="text" name="language"></label></div>
                <div><label>Framework: <input type="text" name="framework"></label></div>
                <input type="submit" value="Submit">
            </form>'''

# GET requests will be blocked
@request_example_bp.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)