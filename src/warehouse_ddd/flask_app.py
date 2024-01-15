from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import gen_salt

from warehouse_ddd import config
from warehouse_ddd import db_tables
from warehouse_ddd import model
from warehouse_ddd.admin.admin import admin
from warehouse_ddd.api.api import api
from warehouse_ddd.auth.auth import auth


engine = create_engine(config.build_db_uri(".env"))
get_session = sessionmaker(bind=engine)

try:
    db_tables.metadata.create_all(bind=engine)
    db_tables.start_mappers()
except Exception:
    pass

login_manager = LoginManager()
login_manager.login_view = "auth.login"

app = Flask(__name__)
app.secret_key = gen_salt(20)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    session = get_session()
    return session.get(model.User, int(user_id))
    # return model.User.get(user_id)


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(api, url_prefix="/api")
