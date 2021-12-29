from app import app as application
import views
from app import db
from posts.blueprint import posts

application.register_blueprint(posts, url_prefix='/blog')

# if __name__ == "__main__":
#     app.run()
app = application