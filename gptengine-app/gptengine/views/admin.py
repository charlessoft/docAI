from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
def index():
    return "admin"
    # return render_template(current_app.config['INDEX_TEMPLATE'])
