def includeme(config):
    config.add_route('register', '/api/register')
    config.add_route('login', '/api/login')
    config.add_route('logout', '/api/logout')
    config.add_route('upload', '/api/upload')
    config.add_route('create_event', '/api/create_event')
    config.add_route('upload_test_form', '/test/upload_form')
    config.add_route('home_test', '/home')
