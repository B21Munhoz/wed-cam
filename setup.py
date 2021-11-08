from setuptools import setup, find_packages

requires = [
    'alembic',
    'boto',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_boto3',
    'plaster_pastedeploy',
    'pyramid-ipython',
    'sqlalchemy',
    'psycopg2',
    'pyramid_tm',
    'pyramid_storage',
    'pyramid_default_cors',
    'pyramid_debugtoolbar',
    'transaction',
    'waitress',
    'zope.sqlalchemy'
]

setup(
    name='wed-cam',
    version='0.0',
    description='Help the bride making a fantastic wedding album!',
    author='Alvaro Munhoz Mota',
    author_email='munhoz-alvaro@hotmail.com',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = main_app:main',
        ],
        'console_scripts': [
            'initdb = main_app.scripts.initializedb:main',
        ],
    }
)
