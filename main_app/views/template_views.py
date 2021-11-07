from pyramid.view import view_config


# View de teste utilizando um template de formulário
@view_config(route_name='upload_test_form', renderer='templates/form-test.pt',
             check_csrf=False)
def upload_test_form():
    return {}


@view_config(route_name='home_test', renderer='templates/home.pt',
             check_csrf=False)
def home_test():
    return {}
