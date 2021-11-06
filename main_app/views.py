from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk, HTTPError
from main_app import get_tm_session
from main_app.models import Photo, Album
from boto.s3.connection import S3Connection, Key
import os
import uuid
import shutil
from pyramid.response import Response


@view_config(route_name='upload_test_form', renderer='templates/form-test.pt',)
def upload_test_form(request):
    return {}


@view_config(route_name='upload',
             request_method='POST')
def upload_image(request):
    try:
        # input_file recebe o arquivo da minha POST request.
        input_file = request.POST['image'].file
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


def view_image(request):
    session = get_tm_session()
    conn = S3Connection('AKIAQRVSZSONUQDINTQ6', '1WO6fELhpH73dl9523C8rjIBVJtzppx/Km2vjLN0')
    bucket = conn.get_bucket('wed-cam')
    k = Key(bucket)
    try:
        img = request.storage.save(request.POST['my_file'], randomize=True)
        photo = Photo()
        photo.author = request.POST['author']
        photo.album = session.query(Album).filter_by(id=request.POST['album_id'])
        photo.file = img
        photo.save()
        return HTTPOk
    except Exception as e:
        print(e.args)
        return HTTPError
