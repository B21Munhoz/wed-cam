from pyramid.view import view_config
from main_app.models import Photo, Album, Event
from boto.s3.connection import S3Connection, Key
import os
import uuid
import shutil
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized
from main_app.models import check_auth


# Upload de Imagem
@view_config(route_name='upload',
             request_method='POST',)
def upload_image(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
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

        # Agora faço o upload para o meu bucket da S3. Mudar as credenciais para uma config file.
        print("Debug: Tentativa de conectar no bucket")
        conn = S3Connection('AKIAQRVSZSONUQDINTQ6', '1WO6fELhpH73dl9523C8rjIBVJtzppx/Km2vjLN0')
        bucket = conn.get_bucket('wed-cam')
        print("Conectou")
        location = bucket.get_bucket_location(Bucket='wed-cam')['LocationConstraint']
        print(location)
        k = Key(bucket)
        k.key = '%s.jpg' % file_name
        k.set_contents_from_filename(file_path)
        print("Setou a imagem na S#")
        # Cria o objeto que armazena as informações da Foto
        session = request.db
        photo = Photo()
        photo.author = user
        photo.album = session.query(Album).filter(Album.id == request.POST['album_id']).first()
        photo.file = '%s.jpg' % file_name
        photo.url = "https://s3-%s.amazonaws.com/%s/%s" % (location, 'wed-cam', photo.file)
        session.add(photo)
        # Deleto o arquivo
        os.remove(file_path)
        try:
            session.commit()
        except Exception as e:
            raise HTTPBadRequest(e.args)
        return Response("Upload Successful")
    except Exception as e:
        print(e.args)
        return Response('FAILED')


# Lista geral de Imagens. Somente o Anfitrião (dono do Casamento) pode ver
@view_config(route_name='image_list',
             request_method='POST',)
def image_list(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event = session.query(Event).filter(Event.id == request.POST['event_id']).first()
    if not event:
        raise HTTPBadRequest()
    if event.host != user:
        raise HTTPUnauthorized()
    photos = event.album.photos
    photo_list = []
    for p in photos:
        photo_list.append(
            {
                "url": p.url,
                "author": p.author.name,
                "approved": p.approved
            }
        )
    return {"photos": photo_list}


# Lista de Imagens Aprovadas. Todos podem ver.
@view_config(route_name='approved_image_list',
             request_method='POST',)
def approved_image_list(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event = session.query(Event).filter(Event.id == request.POST['event_id']).first()
    if not event:
        raise HTTPBadRequest()
    photos = event.album.photos
    photo_list = []
    for p in photos:
        if p.approved:
            photo_list.append(
                {
                    "url": p.url,
                    "author": p.author.name,
                }
            )
    return {"photos": photo_list}


# Aprovar/Desaprovar Imagem
@view_config(route_name='approve_disapprove_image',
             request_method='POST',)
def approve_disapprove_image(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event = session.query(Event).filter(Event.id == request.POST['event_id']).first()
    if not event:
        raise HTTPBadRequest()
    if event.host != user:
        raise HTTPUnauthorized()
    photo = session.query(Photo).filter(Photo.id == request.POST['photo_id']).first()
    if not photo:
        raise HTTPBadRequest()
    photo.approve_disapprove()
    session.add(photo)
    try:
        session.commit()
    except Exception as e:
        raise HTTPBadRequest(e.args)
    Response("OK")
