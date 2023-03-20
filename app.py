"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)  # debug


@app.get("/api/cupcakes")
def get_all_cupcakes():
    """Return JSON for all cupcakes
      {cupcakes: [{id, flavor, size, rating, image}, ...]}
      """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return JSON for a single cupcake
      {cupcake: {id, flavor, size, rating, image}}
      """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def add_cupcake():
    """Adds cupcake to database. If no image is provided, gives a default image.
      Takes JSON {flavor, size, rating, image(optional)}
      Returns JSON {cupcake: {id, flavor, size, rating, image}}
      """

    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json.get("image") or None
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake using the id.
    Takes JSON {flavor, size, rating, image} - All fields optional.
    Returns JSON of updated cupcake {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake by id.
    Returns JSON {deleted: [cupcake-id]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=[cupcake_id])
