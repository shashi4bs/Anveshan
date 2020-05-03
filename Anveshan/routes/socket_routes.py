from app import socketio
from flask_login import current_user
from flask_socketio import emit, send
from utils.query_utils import get_query_recommendation, frequent_search
import json


@socketio.on("connect")
def connect():
	print("connected through Socket")
	#emit("my response", {"data": "connected"})
	if current_user.is_authenticated:
		queries = frequent_search(current_user.username)
	else:
		queries = frequent_search()
	send(json.dumps({"frequent_search": queries}))

@socketio.on("message")
def handle_message(message):
	print(message)
	#expecting message -> {"query" : "ques"}
	try:
		json_message = json.loads(message)
		if json_message["query"]:
			if current_user.is_authenticated:
				queries = get_query_recommendation(json_message["query"], current_user.username)
			else:
				queries = get_query_recommendation(json_message["query"])
		print(queries)
		send(json.dumps({"recommendations" : queries}))
	except Exception as e:
		print(e)

