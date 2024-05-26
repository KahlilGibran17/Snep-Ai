from sqlalchemy import exc, func, select, update, delete
from snep_ai.database import session
from snep_ai.models.User import User

def get_all():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(User)
        users = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return users, error

def get_by_username(uname):
    error = ''
    if uname:
        try:
            stmt = select(User).filter_by(username=uname)
            user = session.execute(statement=stmt).scalar_one_or_none()
        except exc.NoResultFound as e:
            error = e

        return user, error

def get_by_id(user_id):
    error = ''
    if user_id:
        try:
            user = session.get(User, user_id)
        except exc.NoResultFound as e:
            error = e

        return user, error

def count():
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        stmt = select(func.count()).select_from(User)
        count_users = session.execute(stmt).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return count_users, error

def create(uname, hash_pass, role=False):
    error = ''
    if (uname and hash_pass) or role:
        try:
            user = User(username=uname, password=hash_pass, is_admin=role)
            session.add(user)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def edit(user_id, uname, hash_pass=None):
    error = ''
    if user_id and uname:
        try:
            user = update(User).where(User.id==user_id).values(
                username=uname
            )
            session.execute(user)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e
    
    if user_id and uname and hash_pass:
        try:
            user = update(User).where(User.id==user_id).values(
                username=uname,
                password=hash_pass
            )
            session.execute(user)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error

def destroy(user_id):
    error = ''
    if id:
        try:
            user = delete(User).where(User.id==user_id)
            session.execute(user)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e
    
    return None, error