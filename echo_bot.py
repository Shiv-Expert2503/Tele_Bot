import logging
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
import os
from google.cloud import dialogflow as df
from gnewsclient import gnewsclient
import pandas as pd
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialising Everything

logger=logging.getLogger(__name__)
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'dialogflow_credentials'


Token='telegram_token'

all_topics=[['World', 'Nation', 'Entertainment'], ['Sports', 'Science', 'Health'],['Business', 'Technology']]


all_languages=['english', 'indonesian', 'czech', 'german', 'spanish', 'french', 'italian', 'latvian', 'lithuanian', 'hungarian', 'dutch', 'norwegian', 'polish', 'portuguese brasil', 'portuguese portugal', 'romanian', 'slovak', 'slovenian', 'swedish', 'vietnamese', 'turkish', 'greek', 'bulgarian', 'russian', 'serbian', 'ukrainian', 'hebrew', 'arabic', 'marathi', 'hindi', 'bengali', 'tamil', 'telugu', 'malyalam', 'thai', 'chinese simplified', 'chinese traditional', 'japanese', 'korean']


all_locations=['Australia', 'Botswana', 'Canada ', 'Ethiopia', 'Ghana', 'India ', 'Indonesia', 'Ireland', 'Israel ', 'Kenya', 'Latvia', 'Malaysia', 'Namibia', 'New Zealand', 'Nigeria', 'Pakistan', 'Philippines', 'Singapore', 'South Africa', 'Tanzania', 'Uganda', 'United Kingdom', 'United States', 'Zimbabwe', 'Czech Republic', 'Germany', 'Austria', 'Switzerland', 'Argentina', 'Chile', 'Colombia', 'Cuba', 'Mexico', 'Peru', 'Venezuela', 'Belgium ', 'France', 'Morocco', 'Senegal', 'Italy', 'Lithuania', 'Hungary', 'Netherlands', 'Norway', 'Poland', 'Brazil', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Sweden', 'Vietnam', 'Turkey', 'Greece', 'Bulgaria', 'Russia', 'Ukraine ', 'Serbia', 'United Arab Emirates', 'Saudi Arabia', 'Lebanon', 'Egypt', 'Bangladesh', 'Thailand', 'China', 'Taiwan', 'Hong Kong', 'Japan', 'Republic of Korea']

li=[]

df_session_client=df.SessionsClient()
project_id='your_dialogflow project id'

#generating data using dialogflow
def detect_intent_from_text(text,session_id,language_code='en'):
    session=df_session_client.session_path(project_id,session_id)

    text_input=df.TextInput(text=text,language_code=language_code)

    query_input=df.QueryInput(text=text_input)

    response=df_session_client.detect_intent(session=session,query_input=query_input)

    return response.query_result

#return data of dialogflow
def get_reply(query,caht_id):
    response=detect_intent_from_text(query,caht_id)

    if response.intent.display_name=='News_queeries':
        return 'News_queeries',dict(response.parameters)
    
    else:
        return 'small_talk',response.fulfillment_messages[0].text.text[0]


#handeling start command
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    author=update.message.from_user.first_name
    reply="🙏HARI OM🙏\n\n Hi! 👋 {}\n\n Let me first give you a breif intrdouction about me!😃\n\n My Aim->To provide News and keep you updated to this world🌍 and some small random talks😅.\n \n Description->I'm a chat bot AI created by Shivansh!❤️ As he is learning ML so he also build me to implement his algorithms and to see where he stands🙃. Currently he is a newbie as he has just started. \n\n --Rules and Regulation--\n\n 1.To get news you have to pass language,location and topics for which you want to get. One argument is compulsory other than language! Default values are 'english','United States'.\n\n Example->show me sports news from india in hindi(while choosing country as India you must also give language ) \n\n 2.Please Don't use curse words😶‍🌫 during conversation as the current algorithm is not programmed for cursed words.😕 Shivansh has restricted them. \n\n 3.Since Shivansh has just started ML so he doesn't know much about it☹️. Hence I can talk up to a limit only. My algorithm can't handle bigger talks 😢. I think it will take atleast 2 to 3 months for Shivansh to make me a complete chat AI🤩.\n\n One more important feature about my algorithm is that if you misspell something then I'll try my best to understand it!!😎 and also other than texts i will try to copy what you do(except poll,files,conatcts and GIFs as they are more than my storage limit). Wanna se? Try sending sticker \n\n Example--> shoe me tech news from indai in hindi. \n\n So stay tuned and let's hope for our best❤️...Let's GO😋(Start by saying Hi🙈) ".format(author)
    await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)
    # li=[]
    li.append(author)
    print(author)


#handeling help command
async def help(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Can't help at this moment kindley contact Shivansh personally!")
#handeling locations command
async def locations(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text=all_locations)
#handeling languages command
async def languages(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text=all_languages)


#sending text
async def reply_text(update:Update,context : ContextTypes.DEFAULT_TYPE):
    intent,reply=get_reply(update.message.text,update.effective_chat.id)
    # print(intent)
    client=gnewsclient.NewsClient()
    # all_topics=[client.topics[0:3],client.topics[3:6],client.topics[6:9]]
   
    def fetch_news(parameters=reply):

        # getting the desired news

        if (parameters['language']==[]):
            parameters['language']='english'
        if (parameters['test_cases']==[]):
            parameters['test_cases']='Top Stories'
        if(parameters['geo-country']==[]):
            parameters['geo-country']='india'
        if parameters['geo-country']=='india' :
            if parameters['test_cases'][0]=='india' or parameters['test_cases'][0]=='India':
                parameters['test_cases'][0]='Top Stories'

    # getting desired news

        client.language=parameters.get('language')
        client.topic=parameters.get('test_cases')
        client.location=parameters.get('geo-country')

# some of the data is in list (if list then error) so to handle it we do length check agar list nhi h matlab size>1 hence no effect or agar list h to 0th element lenge
        if(len(client.language)>=1):
            client.language=parameters.get('language')[0]
        if(len(client.topic)>=1):
            client.topic=parameters.get('test_cases')[0]
        if(len(client.location)>=1):
            client.location=parameters.get('geo-country')[0]


        # print(len(client.location))
        # print(len(client.topic))
        # print(len(client.language))
        # print("After Changes = ",client.language,client.location,client.topic)

    

        return client.get_news()

    if intent=='News_queeries':
        print(update.message.text)
        # print(reply['language'])
        articles=fetch_news(reply)
        for article in articles:

            await context.bot.send_message(chat_id=update.effective_chat.id,text=article['link'])
    
    # For short talks

    elif intent=='small_talk':
        print(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=reply)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=update.message.text)
    print(reply)


#echoing stickers
async def echo_sticker(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(chat_id=update.effective_chat.id,sticker=update.message.sticker.file_id)

# Showing all news available
async def news(update:Update,context : ContextTypes.DEFAULT_TYPE):
    print(all_topics)
    await context.bot.send_message(chat_id=update.effective_chat.id,text='Choose a Category',reply_markup=ReplyKeyboardMarkup(keyboard=all_topics,one_time_keyboard=True))

#echoing audio
async def echo_audio(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_audio(chat_id=update.effective_chat.id,audio=update.message.audio)

#echoing video
async def echo_video(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video(chat_id=update.effective_chat.id,video=update.message.video.file_id)

#echoing voice
async def echo_voice(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_voice(chat_id=update.effective_chat.id,voice=update.message.voice.file_id)

#echoing photo
async def echo_photo(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id,photo=update.message.photo[-1])

#echoing video note
async def echo_video_note(update:Update,context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video_note(chat_id=update.effective_chat.id,video_note=update.message.video_note.file_id)

#For unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Error handler

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) :
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)


# def error(update:Update,context : ContextTypes.DEFAULT_TYPE):
#     logger.error("Update caused error ")

#Main Function

def main():
    application = ApplicationBuilder().token(Token).build()
    
    #Making command handler for start
    application.add_handler(CommandHandler('start', start))
    #Making command handler for help
    application.add_handler(CommandHandler('help',help))
    #Making command handler for 2-D Keyboard and topic of news available
    application.add_handler(CommandHandler('news',news))
    #Making command handler for 2-D Keyboard and topic of news available
    application.add_handler(CommandHandler('languages',languages))
    #Making command handler for 2-D Keyboard and topic of news available
    application.add_handler(CommandHandler('locations',locations))
    #Making message handler
    application.add_handler(MessageHandler(filters.TEXT ,reply_text))
    #Making sticker handler 
    application.add_handler(MessageHandler(filters.Sticker.ALL,echo_sticker))
    #Making audio handler 
    application.add_handler(MessageHandler(filters.AUDIO,echo_audio))
    #Making video handler
    application.add_handler(MessageHandler(filters.VIDEO,echo_video))
    #Making voice handler
    application.add_handler(MessageHandler(filters.VOICE,echo_voice))
    #Making photo handler
    application.add_handler(MessageHandler(filters.PHOTO,echo_photo))
    #Making video note handler
    application.add_handler(MessageHandler(filters.VIDEO_NOTE,echo_video_note))

    #unknown command handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # application.add_error_handler(error)
    application.add_error_handler(error_handler)
    
    application.run_polling()


if __name__ == '__main__':
    main()

