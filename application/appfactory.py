"""AppFactory"""
import flask


def create_app():
    """Create an app"""
    app = flask.Flask(__name__)

    with app.app_context():
        # pylint: disable=unused-import
        from . import index  # noqa: E402, F401
        from . import students  # noqa: E402, F401
        from . import teachers  # noqa: E402, F401
        from . import login  # noqa: E402, F401
    return app
