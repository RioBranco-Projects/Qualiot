import os

class Config:
    """
    Classe de configuração da aplicação Flask.
    Define as configurações do banco de dados e chaves secretas.
    """

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:396344*gu@localhost:3306/coffeeflow'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'b6f3c17fe92c4b678a9d33e4fabc9c91e4018d81f0e0d41b9f4e8e9ef1c9a0f2ui')
