from config import Config, db
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)