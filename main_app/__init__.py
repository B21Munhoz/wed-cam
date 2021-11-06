from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def main(global_config, **settings):
    settings['sqlalchemy.url'] = "postgresql://alvaro:weddinginvite@localhost:5432/weddingdb"
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('.routes')
    config.include('pyramid_tm')
    config.include('pyramid_boto3')
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)

    config.scan()
    return config.make_wsgi_app()
