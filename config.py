class Config:
    SECRET_KEY = 'clave_secreta_segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventario.db'  # luego puedes cambiar a MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False