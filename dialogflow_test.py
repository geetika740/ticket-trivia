from google.cloud import dialogflow_v2 as dialogflow
import os
import uuid

# Set credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow_key.json"

# Replace this with your actual project_id from dialogflow_key.json
PROJECT_ID = "ticket-trivia-chatbot"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, str(uuid.uuid4()))

text_input = dialogflow.TextInput(text="Hi", language_code="en")
query_input = dialogflow.QueryInput(text=text_input)

response = session_client.detect_intent(session=session, query_input=query_input)
print("Bot reply:", response.query_result.fulfillment_text)
