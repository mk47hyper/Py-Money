from pymoney import create_app, db

app = create_app()

# Used to create new tables if models.py is changed
# def init_db():
#      with app.app_context():
#          db.create_all()
#          db.session.commit()


# init_db()

if __name__ == '__main__':
    app.run(debug=True)
