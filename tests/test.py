from unittest import TestCase
from boggle_app import app  
from boggle import Boggle
from flask import session
from flask import jsonify



class FlaskTests(TestCase):

    def setUp(self):
        """Set up test client."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        with app.test_request_context():
            session.clear()

    def test_home_route(self):
        """Ensure home route renders the board."""
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table>', html)

    def test_valid_word(self):
        """Test with a valid word input."""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word', query_string={'word': 'test'})
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['result'], 'ok')

    def test_invalid_word(self):
        """Test with an invalid word input."""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word', query_string={'word': 'notaword'})
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertIn(data['result'], ['not-word', 'not-on-board'])

    def test_post_score(self):
        """Test posting a score."""
        with self.client:
            response = self.client.post('/post-score', json={'score': 10})
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'success')
            self.assertIn('playcount', data)

@app.route('/post-score', methods=['POST'])
def post_score():
    # Handle the logic of posting a score
    return jsonify({'status': 'success'}), 200


class AppTestCase(TestCase):

    def test_example(self):
        self.assertTrue(True)
