def includeme(config):
    # User Routes
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login')
    config.add_route('logout', '/api/logout')
    # Album Routes
    config.add_route('upload', '/api/upload/{event_id}')
    config.add_route('approved_image_list', '/api/approved_image_list')
    config.add_route('image_list', '/api/image_list')
    config.add_route('approve_disapprove_image', '/api/approve_disapprove_image')
    # Wedding/Event Routes
    config.add_route('create_event', '/api/create_event')
    config.add_route('add_guest', '/api/add_guest')
    config.add_route('view_guests_list', '/api/view_guests_list')
    config.add_route('open_close_event', '/api/open_close_event')
    config.add_route('get_hosted_events', '/api/get_hosted_events')
    config.add_route('get_guest_at', '/api/get_guest_at')
    # Test Template Routes
    config.add_route('upload_test_form', '/test/upload_form')
    config.add_route('home_test', '/home')
