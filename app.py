from chalice import Chalice
from chalicelib.commands import controller, actions
import json
from flask import Flask, request

localApp = Flask(__name__)
app = Chalice(app_name='CoinStatData-Stat-Lambda')

@app.lambda_function()
def handler(event, context):
	print("########### event ==> " + str(event))
	actionType = event['body']['action']
	if actionType in actions.STAT.values():
		body = controller.stat_process(actionType, event)
		print("Body ==> ", str(body))
		return _get_response(200, body)
	else:
		return _get_response(400, "Invalid action type")
    
def _get_response(status_code, body):
	return {
		'statusCode': status_code,
		'body': json.dumps(body),
		'headers': {
			'Content-Type': 'application/json',
		},
	}

@localApp.route("/api", methods=['POST'])
def process():
  data = request.get_json()
  print("Data ==> ", str(data))
  resp = handler(data['event'], {})
  return resp