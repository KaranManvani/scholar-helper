from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


from sqlalchemy.sql import func



#  DB creds
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")


db = SQLAlchemy()


class Scholarships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(150), nullable=False, unique=True)
    # title = db.Column(db.String(150), nullable=False)
    benefits = db.Column(db.String(250))
    eligibility = db.Column(db.String(250))
    region = db.Column(db.String(50))
    deadline = db.Column(db.String(50), nullable=False)
    # offi_web = db.Column(db.String(150), nullable=False)




def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # dialect://username:password@host:port/database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    # app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "connect_args" : {"ssl" : {"ca": "/etc/ssl/cert.pem"}}}
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = { "connect_args" : {"ssl" : {"ca": "website\cacert-2023-05-30.pem"}}}
    db.init_app(app)


    

    @app.route("/")
    @app.route("/index")
    def index():
        return render_template('index.html')


    @app.route("/about")
    def about():
        return render_template('about.html')


    @app.route("/contact_us")
    def contact_us():
        return render_template('contact_us.html')

    @app.route("/scholarships")
    def scholarships():
        cat = request.args.get('category', 'no_cat')
        page_num = request.args.get('page', 1, type=int)
        sort = request.args.get('sort', 'no_sort')
        print(cat)
        print(sort)
        print(page_num)
        data = get_data(cat, sort, page_num)
        return render_template('scholarships.html', Data = data, Cat=cat, Sort=sort)
    

    @app.route("/search")
    def search():
        keyword = request.args.get('keyword')
        cat = request.args.get('category', 'no_cat')
        page_num = request.args.get('page', 1, type=int)
        sort = request.args.get('sort', 'no_sort')
        print(cat)
        print(sort)
        print(page_num)
        print(keyword)
        if type(keyword) != type(None):
            data = search_data(keyword, cat, sort, page_num)
        else:
            data = None
        return render_template('search.html', Keyword=keyword, Data = data, Cat=cat, Sort=sort)
    
    @app.route("/government_funded")
    def government_funded():
        cat = request.args.get('category', 'no_cat')
        page_num = request.args.get('page', 1, type=int)
        sort = request.args.get('sort', 'no_sort')
        print(cat)
        print(sort)
        print(page_num)
        data = get_data(cat, sort, page_num)
        return render_template('government_funded.html', Data = data, Cat=cat, Sort=sort)


    @app.route("/private_funded")
    def private_funded():
        return render_template('private_funded.html')


    @app.route("/international_scholarships")
    def international_scholarships():
        cat = 'international'
        data = get_data(cat)
        return render_template('international_scholarships.html', Data = data)


    @app.route("/scholarships_for_women")
    def scholarships_for_women():
        cat = 'girls'
        data = get_data(cat)
        return render_template('scholarships_for_women.html', Data = data)


    with app.app_context():
        db.create_all()
    print('Created Database!')

    return app

app = create_app()


def search_data(keyword, cat, sort, page_num):
    with app.app_context():
        kw = '%' + '%'.join(keyword.split()) + '%'
        q = db.select(Scholarships).where(Scholarships.title.ilike(kw))

        if cat == 'no_cat':

            if sort == 'title_ascending':
                query = q.order_by(Scholarships.title.asc())
            elif sort == 'title_descending':
                query = q.order_by(Scholarships.title.desc())
            else:
                query = q
        
        else:

            if sort == 'title_ascending':
                query = db.select(Scholarships).where(Scholarships.title.ilike(kw), Scholarships.category == cat).order_by(Scholarships.title.asc())
            elif sort == 'title_descending':
                query = db.select(Scholarships).where(Scholarships.title.ilike(kw), Scholarships.category == cat).order_by(Scholarships.title.desc())
            else:
                query = db.select(Scholarships).where(Scholarships.title.ilike(kw), Scholarships.category == cat)

        schols = db.paginate(query, per_page=10, page=page_num, error_out=True)
        return schols
    


def get_data(cat, sort, page_num):

    with app.app_context():

        if cat == 'no_cat':

            if sort == 'title_ascending':
                query = db.select(Scholarships).order_by(Scholarships.title.asc())
            elif sort == 'title_descending':
                query = db.select(Scholarships).order_by(Scholarships.title.desc())
            else:
                query = db.select(Scholarships)
        
        else:

            if sort == 'title_ascending':
                query = db.select(Scholarships).where(Scholarships.category == cat).order_by(Scholarships.title.asc())
            elif sort == 'title_descending':
                query = db.select(Scholarships).where(Scholarships.category == cat).order_by(Scholarships.title.desc())
            else:
                query = db.select(Scholarships).where(Scholarships.category == cat)

        schols = db.paginate(query, per_page=10, page=page_num, error_out=True)
    return schols


def insert_data(data):
    print('Importing data')

    print('Initializing data insertion')

    if len(data) != 0:

        with app.app_context():
            db.session.execute(Scholarships.__table__.insert().prefix_with(' IGNORE'), data)
            db.session.commit()

        print('Inserted data successfully')
    
    else:
        print("No data provided to insert")
