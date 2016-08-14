from flask import Flask, request
from ranges import RangeDB
import json

app = Flask(__name__)
db = RangeDB()

@app.route('/')
def get_index():
    return json.dumps(str(db),indent=1)

@app.route('/get')
def get_get():
    key = request.args.get('identifier')
    return json.dumps(db.get(key),indent=1)

@app.route('/ranges')
def get_ranges():
    try:
        data = json.loads(request.args.get('range'))
        interval = [int(i) for i in data]
    except Exception as e:
        return json.dumps({"error":"malformed data",
                           "data":request.args.get('range'),
                           "exception": str(e)})
    return json.dumps(db.find_range(interval),indent=1)

@app.route('/write',methods=['POST'])
def post_write():
    try :
        data = json.loads(request.form.keys()[0]) 
        ranges = [[int(i) for i in data["ranges"]]]
        db.update(data['identifier'],ranges)
    except Exception as e:
        return json.dumps({"error":"malformed data",
                           "data":request.form,
                           "exception": str(e)})
    return '{"success":true}'
 
