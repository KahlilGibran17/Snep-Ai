from flask import Blueprint, request, render_template, flash
import snep_ai.services.ChatbotService as svc_chatbot
from flask_login import current_user
import os
import openai
import re
import json
from bs4 import BeautifulSoup
import requests

chatbot = Blueprint('chatbot', __name__)

@chatbot.route("/chat", methods=['POST'])
def chat():
    if request.method == 'POST':
        requestData = request.json
        prompt = requestData['prompt']

        openai.api_key = os.environ.get('API_KEY')

        # Scraping
        key = os.environ.get('SCRAPING_KEY')

        split = prompt.split(" ")
        out = ""

        for s in split:
            out = out + s + "+"

        l = []
        o = {}

        while len(l) == 0:

            url = "https://api.scrapingdog.com/scrape?api_key="+key+"&dynamic=false&url=https://www.bing.com/search?q="+out
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
            resp = requests.get(url,headers=headers)
            s = BeautifulSoup(resp.text, 'html.parser')

            results = s.find_all("li",{"class":"b_algo"})

            
            for i in range(0, len(results)):
                o["Title"]=results[i].find("a").text
                o["link"]=results[i].find("a").get("href")
                o["Description"]=results[i].find("div",{"class":"b_caption"}).text
                o["Position"]=i+1
                l.append(o)
                print(o)
                o={}

        # openai api
        completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
                {   
                    "role": "system", 
                    "content": "You are a chatbot that answers normal general questions. You will answer with the language that the user asked you with. Use these sources to answer the question: \n\n"+
                    "\n\n"+str(l)+"If you cannot understand what the given prompt is, output 'ERROR:INCOMPREHENSIBLE'"
                },
                {   
                    "role": "user", 
                    "content": prompt
                }
            ]
        )

        # get resposne
        openaiResponse = completion.choices[0].message.content
        isSuccess = not re.findall(r"\bERROR\b", openaiResponse)
        
        # pass response back
        response =  {
                        "response": openaiResponse,
                        "isSuccess": isSuccess
                    }
        
        if isSuccess:
            # save log to db
            _, error = svc_chatbot.createChatLog(current_user.id, '2024-04-24', requestData['prompt'], openaiResponse)
            if error:
                flash(error)

        return response

    return render_template('chatbot/chatbot.html')

@chatbot.route("/getChatLog", methods=['GET'])
def get_chatlog():
    # fetch from db
    chatLog, error = svc_chatbot.getChatLog(current_user.id)
    if error:
        flash(error)
        isSuccess = False
    else:
        isSuccess = True

    # map list into json
    response = []
    for chat in chatLog:
        response.append({
            "id": chat.id,
            "user_id": chat.user_id,
            "date": chat.date,
            "message": chat.message,
            "response": chat.response
        })

    # return response
    return {
        "isSuccess": isSuccess,
        "chatLog": response
    }