from flask import Blueprint, render_template
from flask_login import login_required, current_user

import snep_ai.services.PromptLogService as svc_promptLog
import snep_ai.services.InformationListService as svc_informationList

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
@login_required
def index():
    promptLogs, error = svc_promptLog.getPromptLog_limit5(current_user.id)
    count_promptLog, error = svc_promptLog.countPromptLog(current_user.id)
    informationLists, error = svc_informationList.get_all_limit5()

    if error:
        flash(error, "error")

    return render_template('dashboard.html', active_menu='home', count_promptLog=int(count_promptLog[0]), promptLogs=promptLogs, informationLists=informationLists)

@dashboard.route('/chatbot', methods=['GET'])
@login_required
def chatbot():
    return render_template('chatbot/chatbot.html', active_menu='chatbot')

@dashboard.route('/history', methods=['GET'])
@login_required
def history():
    return render_template('history/history.html', active_menu='history')

@dashboard.route('/credit', methods=['GET'])
@login_required
def credit():
    return render_template('credit/credit.html', active_menu='credit')