from flask import request, redirect, url_for
from sqlalchemy import exc, func, select, desc
from snep_ai.database import session
from snep_ai.models.PromptLog import PromptLog

def countPromptLog(user_id):
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(func.count()).select_from(PromptLog).filter_by(user_id=user_id)
        count_users = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return count_users, error

def createPromptLog(user_id, information_category_id, title, content, date, status, probability, reason):
    error = ''
    if user_id:
        try:
            promptLog = PromptLog(user_id=user_id, information_category_id=information_category_id, title=title, content=content, date=date, status=status, probability=probability, reason=reason)
            session.add(promptLog)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def getPromptLog(user_id):
    error = ''
    if user_id:
        try:
            stmt = select(PromptLog).filter_by(user_id=user_id)
            promptLog = session.execute(statement=stmt).scalars().all()
        except exc.IntegrityError as e:
            error = e

        return promptLog, error

def get_by_id(id):
    error = ''
    if id:
        try:
            user = session.get(PromptLog, id)
        except exc.NoResultFound as e:
            error = e

        return user, error

def getPromptLog_limit5(user_id):
    error = ''
    if user_id:
        try:
            stmt = select(PromptLog).filter_by(user_id=user_id).order_by(desc(PromptLog.id)).limit(5)
            promptLog = session.execute(statement=stmt).scalars().all()
        except exc.IntegrityError as e:
            error = e

        return promptLog, error