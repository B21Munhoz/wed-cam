from pyramid.view import view_config
from main_app.models import User
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
from main_app.models import check_auth


# Cadastro de novo Usuário
@view_config(route_name='register',
             renderer='json',
             )
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
        r = HTTPBadRequest(e.args, headerlist=[
            ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
        ])
        print(r.headers)
        raise r
    r = Response("%s Created" % user.name, headerlist=[
        ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
    ])
    print(r.headers)
    return r


# Login
@view_config(route_name='login',
             renderer='json',
             )
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
    r = Response('{"token": "%s", "userid": "%s"}' % (token, uname), headerlist=[
        ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
    ])
    print(r.headers)
    return r


# Logout
@view_config(route_name='logout',
             )
def logout(request):
    user = check_auth(request)
    if user:
        user.clear_token()
    r = HTTPOk("OK", headerlist=[
        ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
    ])
    print(r.headers)
    return r
