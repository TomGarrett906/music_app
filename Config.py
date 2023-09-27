import os

class Config:
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = 'Music Rest Api'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_URL = '/'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLDATABASE_URL')
