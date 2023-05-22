import os
from google.cloud import dialogflow as df

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'C:\Users\DELL\OneDrive\Desktop\ML\Telegram_bot\New folder\news-bot-apqs-683b807f6491.json'


df_session_client=df.SessionsClient()
project_id='news-bot-apqs'
def detect_intent_from_text(text,session_id,language_code='en'):
    session=df_session_client.session_path(project_id,session_id)

    text_input=df.TextInput(text=text,language_code=language_code)

    query_input=df.QueryInput(text=text_input)

    response=df_session_client.detect_intent(session=session,query_input=query_input)

    return response.query_result


response=detect_intent_from_text('tech news from delhi',12345)
print(response)