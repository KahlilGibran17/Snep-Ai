from flask import request, redirect, url_for
from sqlalchemy import exc, func, select
from snep_ai.database import session
from snep_ai.models.ChatLog import ChatLog

def createChatLog(user_id, date, message, response):
    error = ''
    if user_id:
        try:
            chatLog = ChatLog(user_id=user_id, date=date, message=message, response=response)
            session.add(chatLog)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def getChatLog(user_id):
    error = ''
    if user_id:
        try:
            stmt = select(ChatLog).filter_by(user_id=user_id)
            chatLog = session.execute(statement=stmt).scalars().all()
        except exc.IntegrityError as e:
            error = e

        return chatLog, error