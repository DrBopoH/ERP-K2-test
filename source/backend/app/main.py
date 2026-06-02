"""
Головний модуль запуску Flask-додатку.
Ініціалізує екземпляр додатку, налаштовує базу даних за допомогою конфігів 
та реєструє всі доступні Blueprint маршрути.
"""

from flask import Flask

from app.core.config import DATABASE_URL
from app.models import db


def create_app() -> Flask:
	"""
    Фабрика додатку (Application Factory) для створення та конфігурації екземпляра Flask.
    
    Виконує:
	    - Ініціалізацію базових налаштувань та URI бази даних.
    	- Прив'язку ORM SQLAlchemy до поточного контексту додатку.
    	- Автоматичну генерацію таблиць в БД (якщо вони відсутні).
    	- Реєстрацію Blueprint модулів з префіксом маршрутизації '/api'.
    
    Повертає:
    	- Flask: Повністю налаштований та готовий до роботи екземпляр додатку.
    """
	app = Flask(__name__)
	
	app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	
	db.init_app(app)
	
	with app.app_context():
		db.create_all()
		
	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix="/api")
	
	return app

if __name__ == "__main__":
	"""
	Точка входу програми.
	"""
	app: Flask = create_app()
	
	app.run(debug=True)