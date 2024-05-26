from flask import Blueprint, request, render_template, flash
import snep_ai.services.PromptLogService as svc_promptLog
import snep_ai.services.InformationCategoryService as svc_informationCategory
from flask_login import current_user, login_required
import os
import openai
import re
from bs4 import BeautifulSoup
import requests

informationValidation = Blueprint('informationValidation', __name__)

@informationValidation.route('/news-validation', methods=['GET'])
@login_required
def newsvalidation():
    user_histories, error = svc_promptLog.getPromptLog(current_user.id)
    count_promptLog, error = svc_promptLog.countPromptLog(current_user.id)

    if error:
        flash(error, "error")
        
    return render_template('newsvalidation/newsvalidation.html', active_menu='newsvalidation', count_promptLog=count_promptLog[0], user_histories=user_histories)

@informationValidation.route('/news-validation/<int:id>', methods=['GET'])
@login_required
def detail(id):
    detail, error = svc_promptLog.get_by_id(id)

    if error:
        flash(error, "error")
        
    return render_template('newsvalidation/detail.html', active_menu='newsvalidation', detail=detail)

@informationValidation.route('/newscan', methods=['GET'])
@login_required
def scan():
    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    return render_template('newsvalidation/text.html', active_menu='text', categories=categories, countCategories=count_categories[0])

@informationValidation.route("/informationValidation", methods=['POST'])
@login_required
def prompt():
    if request.method == 'POST':

        requestData = request.json
        title = requestData['title']
        content = requestData['content']
        date = requestData['date']
        informationType = int(requestData['informationType'])
        prompt = "Title: " + title + "\nContent: " + content+"\n Date: "+ date+ "\n informationType: " + str(informationType)

        openai.api_key = os.environ.get('API_KEY')

        # openai api
        completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
                {   
                    "role": "system", 
                    "content": "Your job is to analyze the given information and decide if the information is valid or hoax, you will also have to give reasoning on your decision and how confidence you are with your answer. You should include how relevant you think the data based on the date of information written and how credible it is. Answer with the format of 'Decision: true/false (true = valid, false = hoax) <br> Accuracy: how confidence you are with your answer in percent without the percent symbol <br> Reasoning: Your reasoning behind your decision (The reasoning will be in the language that the user asked you with)' (the '<br>' must be included for regular expression reasoning).If you cannot understand what the given prompt is or if the given description doesn't seem to be from any news information, only return 'ERROR:INCOMPREHENSIBLE'"
                },
                {   
                    "role": "user", 
                    "content": content+" Date of information writeen: " + str(date)
                }
            ]
        )

        # get resposne
        openaiResponse = completion.choices[0].message.content
        print(openaiResponse)
        isSuccess = not re.findall(r"\bERROR\b", openaiResponse)

        if isSuccess:

            responseList = openaiResponse.partition(' <br> ')
            response1 = responseList[0]
            response2 = responseList[2].partition(' <br> ')[0]
            response3 = responseList[2].partition(' <br> ')[2]

            decision = response1.partition(': ')[2]
            if decision == True:
                decision = "Valid"
            elif decision == False:
                decision = "Invalid"
            print(decision)
            accuracy = int(response2.partition(': ')[2])
            print(accuracy)
            reason = response3.partition(': ')[2]
            print(reason)

            openaiResponse = "Decision : " + str(decision) +" <br> Accuracy : " + str(accuracy) +"% <br> Reason : " + str(reason)

            # scraping
            key = os.environ.get('SCRAPING_KEY')

            split = title.split(" ")
            out = ""

            for s in split:
                out = out + s + "+"
                
            print(out)

            isFound = False
            sources = ""

            while not isFound:
            
                url = "https://api.scrapingdog.com/scrape?api_key="+key+"&dynamic=false&url=https://www.bing.com/search?q="+out
                headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
                resp = requests.get(url,headers=headers)
                s = BeautifulSoup(resp.text, 'html.parser')

                o = {}

                results = s.find_all("li",{"class":"b_algo"})

                for i in range(0, len(results)):
                    o["link"]=results[i].find("a").get("href")
                    sources += "<a href=" + o["link"] + ">" + o["link"] + "</a><br>"
                    print(o["link"])

                if sources == "":
                    isFound = False
                else:
                    isFound = True

            openaiResponse += "<br>Here are several information that may be relevant: <br>"+sources

            # save log to db
            # _, error = svc_promptLog.createPromptLog(current_user.id, str(informationType), prompt, openaiResponse)
            # _, error = svc_promptLog.createPromptLog(current_user.id, informationType, title, content, date, decision, accuracy, reason)
            # if error:
            #     print(error)
        
        # pass response back
        response =  {
                        "response": openaiResponse,
                        "isSuccess": isSuccess
                    }

        return response
 
    return render_template('chatbot/chatbot.html')


@informationValidation.route('/newscan/image', methods=['GET'])
@login_required
def newscan_image():
    count_categories, _ = svc_informationCategory.count()
    categories, error = svc_informationCategory.get_all()

    return render_template('newsvalidation/image.html', active_menu='image', categories=categories, countCategories=count_categories[0])

@informationValidation.route("/informationValidation_Picture", methods=['POST'])
@login_required
def prompt_Picture():
    if request.method == 'POST':

        requestData = request.json
        title = requestData['title']
        content = requestData['content']
        date = requestData['date']
        informationType = int(requestData['informationType'])

        openai.api_key = os.environ.get('API_KEY')

        # prompt
        completion = openai.ChatCompletion.create(
            model="gpt-4-vision-preview", 
            messages=[{"role": "user", 
                    "content":[
                            {"type": "text",
                            "text": "Can you please tell me what is displayed on this image?"},
                            {"type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{content}"}]
                        }])

        pictureResponse = completion.choices[0].message.content
        print(pictureResponse)

        completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
                {   
                    "role": "system", 
                    "content": "You will be given a description of a picture to analyze and decide if the information description is valid or hoax, you will also have to give reasoning on your decision and how confidence you are with your answer. You should include how relevant you think the data based on the date of information written and how credible it is. Answer with the format of 'Decision: true/false (true = valid, false = hoax) <br> Accuracy: how confidence you are with your answer in percent without the percent symbol <br> Reasoning: Your reasoning behind your decision' (the '<br>' must be included for regular expression reasoning).If you cannot understand what the given prompt is or if the given description doesn't seem to be from any news information, only return 'ERROR:INCOMPREHENSIBLE'"
                },
                {   
                    "role": "user", 
                    "content": pictureResponse
                }
            ]
        )

        # get resposne
        openaiResponse = completion.choices[0].message.content
        print(openaiResponse)
        isSuccess = not re.findall(r"\bERROR\b", openaiResponse)

        if isSuccess:

            responseList = openaiResponse.partition(' <br> ')
            response1 = responseList[0]
            response2 = responseList[2].partition(' <br> ')[0]
            response3 = responseList[2].partition(' <br> ')[2]

            decision = response1.partition(': ')[2]
            if decision == True:
                decision = "Valid"
            elif decision == False:
                decision = "Invalid"
            print(decision)
            accuracy = int(response2.partition(': ')[2])
            print(accuracy)
            reason = response3.partition(': ')[2]
            print(reason)

            openaiResponse = "Decision : " + str(decision) +" <br> Accuracy : " + str(accuracy)+"% <br> Reason : " +str(reason)

            # scraping
            key = os.environ.get('SCRAPING_KEY')

            split = title.split(" ")
            out = ""

            for s in split:
                out = out + s + "+"
                
            print(out)
            
            url = "https://api.scrapingdog.com/scrape?api_key="+key+"&dynamic=false&url=https://www.bing.com/search?q="+out
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
            resp = requests.get(url,headers=headers)
            s = BeautifulSoup(resp.text, 'html.parser')

            o = {}

            results = s.find_all("li",{"class":"b_algo"})

            openaiResponse += "<br>Here are several information that may be relevant: <br>"

            for i in range(0, len(results)):
                o["link"]=results[i].find("a").get("href")
                openaiResponse += "<a href=" + o["link"] + ">" + o["link"] + "</a><br>"
                print(o["link"])

            # save log to db
            # _, error = svc_promptLog.createPromptLog(current_user.id, str(informationType), prompt, openaiResponse)
            # _, error = svc_promptLog.createPromptLog(current_user.id, informationType, title, content, date, decision, accuracy, reason)
            # if error:
            #     print(error)
        
        # pass response back
        response =  {
                        "response": openaiResponse,
                        "isSuccess": isSuccess
                    }

        return response
 
    return render_template('chatbot/chatbot.html')

@informationValidation.route("/getPromptLog", methods=['GET'])
@login_required
def get_PromptLog():
    # fetch from db

    promptLog, error = svc_promptLog.getPromptLog(current_user.id)
    if error:
        flash(error)
        isSuccess = False
    else:
        isSuccess = True

    # map list into json
    response = []
    for prompt in promptLog:
        response.append({
            "id": prompt.id,
            "user_id": prompt.user_id,
            "information_category_id": prompt.information_category_id,
            "title": prompt.title,
            "content": prompt.content,
            "date": prompt.date,
            "status": prompt.status,
            "probability": prompt.probability
        })

    # return response
    return {
        "isSuccess": isSuccess,
        "promptLog": response
    }