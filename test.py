from unittest import TestCase
from app import app, User,db, connect_db

class UnitTestCase(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        # connect_db(app)
        db.drop_all()
        db.create_all()
        user_one = User(first_name="Bob",last_name="Trika",image_url="https://images.pexels.com/photos/9304725/pexels-photo-9304725.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
        user_two = User(first_name="Jess",last_name="Trika",image_url="https://media.istockphoto.com/id/183821822/photo/say.webp?b=1&s=170667a&w=0&k=20&c=swQJgX34XSWBCtqou5XITqpOAxukOWX5Lh3PiZh3R18=")
        user_three = User(first_name="Dylan",last_name="Trika",image_url="https://media.istockphoto.com/id/172947045/photo/black-white-and-gray-tiles-full-frame-background.webp?b=1&s=170667a&w=0&k=20&c=cZ60Vs7I9i6yJDDcub9nh-F6caKS-6pVWc8UW2-vRXA=")
        db.session.add(user_one)
        db.session.add(user_two)
        db.session.add(user_three)
        db.session.commit()

    def test_welcome(self):
        with app.test_client() as client:
            resp = client.get('/')
        html = resp.get_data(as_text=True)
        self.assertIn('<h1>Users</h1>', html)
        self.assertEqual(resp.status_code, 302)
    
    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
        html = resp.get_data(as_text=True)
        self.assertIn('<h1>Users</h1>', html)
        self.assertIn('Bob Trika', html)
        self.assertIn('Jess Trika', html)
        self.assertIn('Dylan Trika', html)
        self.assertEqual(resp.status_code, 200)

    def user_form(self):
        with app.test_client() as client:
            resp = client.get('/')
        html = resp.get_data(as_text=True)
        self.assertIn('Create a User', html)
        self.assertEqual(resp.status_code, 200)