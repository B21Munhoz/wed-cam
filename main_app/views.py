from pyramid.view import view_config
from main_app.models import Photo, Album, User
from boto.s3.connection import S3Connection, Key
import os
import uuid
import shutil
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.security import remember, forget


@view_config(route_name='register',
             request_method='POST',
             renderer='json')
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


@view_config(route_name='login',
             request_method='POST',
             renderer='json')
def login(request):
    session = request.db
    username = request.json_body['username']
    password = request.json_body['password']
    user = session.query(User).filter(User.username == username).first()
    try:
        if user.verify_password(password):
            headers = remember(request, userid=user.username)
        else:
            headers = forget(request)
    except Exception as e:
        headers = forget(request)
        print(e.args)
    return HTTPFound(location=request.route_url('home_test'), headers=headers)


# View de teste utilizando um template de formulário
@view_config(route_name='upload_test_form', renderer='templates/form-test.pt',)
def upload_test_form(request):
    return {}


@view_config(route_name='home_test', renderer='templates/home.pt',)
def home_test(request):
    return {}


@view_config(route_name='upload',
             request_method='POST')
def upload_image(request):
    try:
        # input_file recebe o arquivo da minha POST request.
        input_file = request['image'].file
        # gero um novo nome com o uuid, para que o arquivo tenha um nome único
        file_name = uuid.uuid4()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 'wedding-files', '%s.jpg' % file_name))
        # gero um arquivo temporário para evitar que o programa utilize um arquivo incompleto
        temp_file_path = file_path + '~'
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # Com o arquivo totalmente salvo, eu renomeio ele para o nome original
        os.rename(temp_file_path, file_path)

        # Agora faço o upload para o meu bucket da S3
        conn = S3Connection('AKIAQRVSZSONUQDINTQ6', '1WO6fELhpH73dl9523C8rjIBVJtzppx/Km2vjLN0')
        bucket = conn.get_bucket('wed-cam')
        k = Key(bucket)
        k.key = '%s.jpg' % file_name
        k.set_contents_from_filename(file_path)

        # session = request.db
        # photo = Photo()
        # photo.author = request.POST['author']
        # photo.album = session.query(Album).filter_by(id=request.POST['album_id'])
        # photo.file = '%s.jpg' % file_name
        # photo.save()

        # Deleto o arquivo
        os.remove(file_path)
        return Response('OK')
    except Exception as e:
        print(e.args)
        return Response('FAILED')
