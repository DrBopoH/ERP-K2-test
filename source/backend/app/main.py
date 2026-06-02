"""
Головний модуль запуску Flask-додатку.
Ініціалізує екземпляр додатку, налаштовує базу даних за допомогою конфігів 
та реєструє всі доступні Blueprint маршрути.
"""

from flask import Flask

from app.core.config import DATABASE_URL
from app.models import db


def create_app(test_config: dict | None = None) -> Flask:
	"""
	Фабрика додатку (Application Factory) для створення та конфігурації екземпляра Flask.
	Приймає опціональний test_config для перевизначення налаштувань під час тестів.
	
	Виконує:
		- Ініціалізацію базових налаштувань та URI бази даних.
		- Прив'язку ORM SQLAlchemy до поточного контексту додатку.
		- Автоматичну генерацію таблиць в БД (якщо вони відсутні).
		- Реєстрацію Blueprint модулів з префіксом маршрутизації '/api'.
	
	Повертає:
		- Flask: Повністю налаштований та готовий до роботи екземпляр додатку.
	"""
	app = Flask(__name__)
	
	if test_config is None: # pragma: no cover
		app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL 
	else:
		app.config.update(test_config)
	
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db.init_app(app)
	
	with app.app_context():
		db.create_all()
		
	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix="/api")
	
	return app

if __name__ == "__main__": # pragma: no cover
	"""
	Точка входу програми.
	"""
	app: Flask = create_app()
	
	app.run(debug=True)