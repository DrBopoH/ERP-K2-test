from flask import Flask

from app.models import db


def create_app() -> Flask:
	app = Flask(__name__)
	
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/erp.db"
	
	db.init_app(app)
	
	with app.app_context():
		db.create_all()
		
	from app.routes import api_bp
	app.register_blueprint(api_bp, url_prefix="/api")
	
	return app

if __name__ == "__main__":
	app: Flask = create_app()
	
	app.run(debug=True)