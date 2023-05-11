from unittest import TestCase
from app import app, home_page, create_user_form, create_user_submit, edit_user_form, edit_user_submit, user_page
from flask import session, request, flash
from models import db, Users

#use test db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()

class RouteTests(TestCase):

    def setUp(self):
        with app.app_context():

            db.drop_all()
            db.create_all()
            
            Users.query.delete()

            john = Users(first_name='John', last_name='Egbert', image_url='https://i.redd.it/twdd6jj3eis41.gif')
            jade = Users(first_name='Jade', last_name='Harley')

            db.session.add(john)
            db.session.add(jade)

            db.session.commit()
        
    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                res = client.get('/users')
                
                self.assertIn('<a href="/users/2">Jade Harley</a>', res.get_data(as_text=True))

    def test_create_form(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                res = client.get('/users/new')
                
                self.assertIn('<label for="first_name">First Name:</label>\n            <input type="text" name="first_name" id="first_name">', res.get_data(as_text=True))

    def test_create_submit(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                
                formdict = {'first_name':'Dave', 'last_name':'Strider','image_url':'https://steamuserimages-a.akamaihd.net/ugc/886510998161702639/A2D0121D2FE457A644ED49766183E77BD13F3E22/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false'}
                res = client.post('/users/new', data=formdict)
                
                self.assertEqual(302, res.status_code)
                self.assertEqual('Dave', Users.query.get(3).first_name)

    def test_edit_form(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:

                res = client.get('/users/edit/2')
                
                self.assertIn('<input type="text" name="first_name" id="first_name" value="Jade">', res.get_data(as_text=True))

    def test_edit_submit(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                
                formdict = {'first_name':'Dave', 'last_name':'Strider','image_url':'https://steamuserimages-a.akamaihd.net/ugc/886510998161702639/A2D0121D2FE457A644ED49766183E77BD13F3E22/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false'}
                res = client.post('/users/edit/2', data=formdict)
                
                self.assertEqual(302, res.status_code)
                self.assertEqual('Dave', Users.query.get(2).first_name)

    def test_root(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                res = client.get('/')

                self.assertEqual(302, res.status_code)


