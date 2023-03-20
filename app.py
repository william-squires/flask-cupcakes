"""Flask app for Cupcakes"""

import os    # sql-alchemy

from flask import Flask, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension # debug

from models import db, connect_db, Cupcake    # sql-alchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" # debug, session
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(     # sql-alchemy
    "DATABASE_URL", 'postgresql:///cupcakes')             # sql-alchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # sql-alchemy
app.config['SQLALCHEMY_ECHO'] = True                        # sql-alchemy

connect_db(app)     # sql-alchemy

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)  # debug

