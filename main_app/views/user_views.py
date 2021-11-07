from pyramid.view import view_config
from main_app.models import User
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
from main_app.models import check_auth


# Cadastro de novo Usuário
@view_config(route_name='register',
             request_method='POST',
             renderer='json',
             check_csrf=False)
def register_user(request):
    session = request.db
    name = request.json_body['name']
    username = request.json_body['username']
    password = request.json_body['password']
    user = User()
    user.username = username
    user.password = password
    user.name = name
    session.add(user)
    try:
        session.commit()
    except Exception as e:
        raise HTTPBadRequest(e.args)
    return Response("%s Created" % user.name)


# Login
@view_config(route_name='login',
             request_method='POST',
             renderer='json',
             check_csrf=False)
def login(request):
    session = request.db
    username = request.json_body['username']
    password = request.json_body['password']
    user = session.query(User).filter(User.username == username).first()
    token = None
    uname = None
    try:
        if user.verify_password(password):
            token = user.generate_token()
            uname = user.username
        else:
            user.clear_token()
    except Exception as e:
        user.clear_token()
        print(e.args)

    return {"token": token,
            "userid": uname}


# Logout
@view_config(route_name='logout',
             check_csrf=False)
def logout(request):
    user = check_auth(request)
    if not user:
        return HTTPOk()
    user.clear_token()
    return HTTPOk()
