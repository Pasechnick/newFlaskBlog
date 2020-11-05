from flask import Blueprint, render_template

# instance of the Blueprint with "errors" name
errors = Blueprint('errors', __name__)

# the way we create error handlers is similar the way we create routes except we use different decorators
# after we do this, we make html templates for those errors
# after that we need to import and register those blueprints in the "__init__.py" to activate our custom error pages

@errors.app_errorhandler(404) # 404 is whenever page is not found (the page do not exist)
def error_404(error):
    return render_template('errors/404.html'), 404 # we can return a second value (404 in this case) that is a status code, where default is 200


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403 # 403 is permission error, whenever someone tries to do what forbitten


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500 # 500 is just general server error. Some problems with the server.


