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
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST,GET,DELETE,PATCH,PUT,OPTIONS'),
            ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization'),
            ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
        ])
        print(r.headers)
        raise r
    r = Response("%s Created" % user.name, headerlist=[
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST,GET,DELETE,PATCH,PUT,OPTIONS'),
        ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization'),
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

    return Response(
        '{"token": "%s", "userid": "%s"}' % (token, uname),
        headerlist=[
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST'),
            ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization'),
            ("Content-Type", "application/json; charset=utf-8"),
        ])


# Logout
@view_config(route_name='logout',
             )
def logout(request):
    user = check_auth(request)
    if not user:
        return Response(HTTPOk(), headerlist=[
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST'),
            ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization'),
            ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
        ])
    user.clear_token()
    return Response(HTTPOk(), headerlist=[
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST'),
        ('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, Authorization'),
        ("Content-Type", "application/x-www-form-urlencoded; charset=utf-8"),
    ])
