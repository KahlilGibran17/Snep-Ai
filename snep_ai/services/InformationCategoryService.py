from flask import request, redirect, url_for
from sqlalchemy import exc, func, select, update, delete
from snep_ai.database import session
from snep_ai.models.InformationCategory import InformationCategory

def get_all():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(InformationCategory)
        informationCategory = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return informationCategory, error


def get_by_id(id):
    error = ''
    if id:
        try:
            informationCategory = session.get(InformationCategory, id)
        except exc.NoResultFound as e:
            error = e

        return informationCategory, error
        
def get_by_name(label):
    error = ''
    if id:
        try:
            stmt = select(InformationCategory).filter_by(label=label)
            informationCategory = session.execute(statement=stmt).scalar_one_or_none()
        except exc.IntegrityError as e:
            error = e

        return informationCategory, error

def count():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(func.count()).select_from(InformationCategory)
        count_informationCategory = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return count_informationCategory, error

def create(label):
    error = ''
    if label:
        try:
            informationCategory = InformationCategory(label=label)
            session.add(informationCategory)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def edit(id, label):
    error = ''
    if label:
        try:
            informationCategory = update(InformationCategory).where(InformationCategory.id==id).values(
                label=label
            )
            session.execute(informationCategory)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def destroy(id):
    error = ''
    if id:
        try:
            informationCategory = delete(InformationCategory).where(InformationCategory.id==id)
            session.execute(informationCategory)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e
    
    return None, error

def getInformationCategory(id):
    error = ''
    if id:
        try:
            stmt = select(InformationCategory).filter_by(id=id)
            informationCategory = session.execute(statement=stmt).scalars().all()
        except exc.IntegrityError as e:
            error = e

        return informationCategory, error