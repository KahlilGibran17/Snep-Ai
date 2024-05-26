from flask import request, redirect, url_for
from sqlalchemy import exc, func, select, update, delete, desc
from snep_ai.database import session
from snep_ai.models.InformationList import InformationList

def get_all():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(InformationList).order_by(desc(InformationList.id))
        informationLists = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return informationLists, error


def get_all_limit5():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(InformationList).order_by(desc(InformationList.id)).limit(5)
        informationLists = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return informationLists, error

def count():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(func.count()).select_from(InformationList)
        count_informationLists = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return count_informationLists, error

def getPromptLog(user_id):
    error = ''
    if user_id:
        try:
            stmt = select(InformationList).filter_by(user_id=user_id)
            InformationList = session.execute(statement=stmt).scalars().all()
        except exc.IntegrityError as e:
            error = e

        return InformationList, error


def get_by_title(title):
    error = ''
    if title:
        try:
            stmt = select(InformationList).filter_by(title=title)
            informationList = session.execute(statement=stmt).scalar_one_or_none()
        except exc.IntegrityError as e:
            error = e

        return informationList, error

def get_by_id(list_id):
    error = ''
    if list_id:
        try:
            informationList = session.get(InformationList, list_id)
        except exc.NoResultFound as e:
            error = e

        return informationList, error

def create(title, content, information_category_id, image, time_relevancy):
    error = ''
    if title and content and information_category_id and image and time_relevancy:
        try:
            informationList = InformationList(title=title, content=content, information_category_id= information_category_id, image=image, timerelevancy=time_relevancy)
            session.add(informationList)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def edit(list_id, title, content, information_category_id, time_relevancy, image=''):
    error = ''
    if list_id and title and image:
        try:
            informationList = update(InformationList).where(InformationList.id==list_id).values(
                title=title, content=content, information_category_id= information_category_id, image=image, timerelevancy=time_relevancy
            )
            session.execute(informationList)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e
    
    if list_id and title or image:
        try:
            informationList = update(InformationList).where(InformationList.id==list_id).values(
                title=title, content=content, information_category_id= information_category_id, timerelevancy=time_relevancy
            )
            session.execute(informationList)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def destroy(list_id):
    error = ''
    if id:
        try:
            informationList = delete(InformationList).where(InformationList.id==list_id)
            session.execute(informationList)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e
    
    return None, error