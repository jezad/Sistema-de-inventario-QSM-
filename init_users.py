from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Verificar si ya existen usuarios para evitar duplicados
    if User.query.first():
        print("⚠️ Ya existen usuarios en la base de datos")
    else:
        # Crear usuario administrador
        admin = User(
            username="adam",
            password=generate_password_hash("29916823"),
            role="admin"
        )

        # Crear usuario gerente
        gerente = User(
            username="gerente",
            password=generate_password_hash("Ricardopzos"),
            role="gerente"
        )

        db.session.add_all([admin, gerente])
        db.session.commit()

        print("✅ Usuarios internos creados correctamente")