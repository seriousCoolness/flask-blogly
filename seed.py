from models import Users, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()


    Users.query.delete()

    row_1 = Users(first_name='John', last_name='Egbert', image_url='https://i.redd.it/twdd6jj3eis41.gif')
    row_2 = Users(first_name='Rose', last_name='Lalonde')

    db.session.add(row_1)
    db.session.add(row_2)

    db.session.commit()