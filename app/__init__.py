import os
from flask import Flask, session


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'cocktails.sqlite'),
        MAIL_SMTP_HOST=os.environ.get('MAIL_SMTP_HOST', 'smtp.gmail.com'),
        MAIL_SMTP_PORT=os.environ.get('MAIL_SMTP_PORT', '587'),
        MAIL_SMTP_USER=os.environ.get('MAIL_SMTP_USER', ''),
        MAIL_SMTP_PASS=os.environ.get('MAIL_SMTP_PASS', ''),
        MAIL_SENDER=os.environ.get('MAIL_SENDER', ''),
    )

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from . import auth, main
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    @app.context_processor
    def inject_user_context():
        from app.repositories import favorite_repository, user_repository
        user_id = session.get('user_id')
        if user_id:
            user = user_repository.get_user_by_id(user_id)
            fav_ids = favorite_repository.get_favorite_ids(user_id)
            return {'current_user': user, 'favorite_ids': fav_ids}
        return {'current_user': None, 'favorite_ids': set()}

    return app
