from models import db, Cupcake
from app import app
from unittest import TestCase
import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'


# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

UPDATE_CUPCAKE_DATA = {
    "flavor": "mint-chip",
    "rating": 15
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json.copy()

            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json.copy()

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Tests for updating a cupcake info with Patch request"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            num_cupcakes_before_update = Cupcake.query.count()

            response = client.patch(url, json=UPDATE_CUPCAKE_DATA)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.json, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "mint-chip",
                    "rating": 15,
                    "size": "TestSize",
                    "image": 'http://test.com/cupcake.jpg'
                }
            })
            self.assertEqual(num_cupcakes_before_update, Cupcake.query.count())

    def test_delete_cupcake(self):
        """Tests for deleting cupcake"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            num_cupcakes_before_delete = Cupcake.query.count()

            response = client.delete(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"deleted": [self.cupcake_id]})
            self.assertEqual(
                (num_cupcakes_before_delete - 1),
                Cupcake.query.count()
            )

    def test_create_and_update_cupcake_with_delete(self):
        with app.test_client() as client:
            base_url = "/api/cupcakes"

            starting_num_cupcakes = Cupcake.query.count()

            response = client.post(base_url, json=CUPCAKE_DATA_2)

            self.assertEqual(response.status_code, 201)
            self.assertIsInstance(response.json['cupcake']['id'], int)

            cupcake_id = response.json["cupcake"]["id"]

            response = client.patch(
                f"{base_url}/{cupcake_id}",
                json=UPDATE_CUPCAKE_DATA
            )

            self.assertEqual(
                response.json,
                {"cupcake": {
                    'id': cupcake_id,
                    'flavor': 'mint-chip',
                    'rating': 15,
                    'size': 'TestSize2',
                    'image': "http://test.com/cupcake2.jpg"
                }})

            client.delete(f"{base_url}/{cupcake_id}")

            self.assertEqual(starting_num_cupcakes, Cupcake.query.count())
