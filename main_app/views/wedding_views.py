from pyramid.view import view_config
from main_app.models import Event
from pyramid.response import Response
from pyramid.httpexceptions import (HTTPBadRequest, HTTPUnauthorized)
from main_app.models import check_auth


@view_config(route_name='create_event',
             request_method='POST',
             renderer='json',
             check_csrf=False
             )
def create_event(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event = Event()
    event.name = request.json_body['name']
    event.host = user
    session.add(event)
    try:
        session.commit()
    except Exception as e:
        raise HTTPBadRequest(e.args)
    return {"invitation": event.invitation}


@view_config(route_name='view_guests_list',
             request_method='POST',
             renderer='json',
             check_csrf=False
             )
def view_guests_list(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event_id = request.json_body['event_id']
    event = session.query(Event).filter(Event.id == event_id).first()
    if (not event) or (user != event.host):
        raise HTTPBadRequest()
    guests = event.guests
    guests_list = []
    for g in guests:
        guests_list.append(g.name)
    return {"guests_list": guests_list}


@view_config(route_name='add_guest',
             request_method='POST',
             check_csrf=False
             )
def add_guest(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    invitation = request.json_body['invitation']
    event = session.query(Event).filter(Event.invitation == invitation).first()
    if not event:
        raise HTTPBadRequest()
    event.add_guest(user)
    session.add(event)
    try:
        session.commit()
    except Exception as e:
        raise HTTPBadRequest(e.args)
    return Response("OK")


@view_config(route_name='open_close_event',
             request_method='POST',
             check_csrf=False
             )
def open_close_event(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    session = request.db
    event_id = request.json_body['event_id']
    event = session.query(Event).filter(Event.id == event_id).first()
    if (not event) or (user != event.host):
        raise HTTPUnauthorized()
    event.open_close_event()
    session.add(event)
    try:
        session.commit()
    except Exception as e:
        raise HTTPBadRequest(e.args)
    return Response("OK")


@view_config(route_name='get_hosted_events',
             renderer='json',
             check_csrf=False)
def get_hosted_events(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    events_list = []
    for e in user.hosted_events:
        events_list.append(
            {
                "event_id": e.id,
                "event_name": e.name,
                "event_open": e.started,
                "invitation": e.invitation
            }
        )
    return {"hosting_events": events_list}


@view_config(route_name='get_guest_at',
             renderer='json',
             check_csrf=False)
def get_guest_at(request):
    user = check_auth(request)
    if not user:
        raise HTTPUnauthorized()
    events_list = []
    for e in user.guest_at:
        events_list.append(
            {
                "event_id": e.id,
                "event_name": e.name,
                "event_open": e.started
            }
        )
    return {"guest_at": events_list}
