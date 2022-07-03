from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
import string

from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config["SECRET_KEY"]='OUSSAMA1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class BookList(db.Model):
    __tablename__ = 'BookList'
    Id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    description=db.Column(db.String(1000))
    def __repr__(self):
        return str(self.Id)+"  "+str(self.author)+"  "+str(self.title)+"  "+str(self.description)

class Clients(db.Model):
    __tablename__ = 'Clients'
    Cin = db.Column(db.String(255), primary_key=True)
    Name = db.Column(db.String(255), nullable=False)


class Rent(db.Model):
    __tablename__ = 'Rent'
    Id = db.Column(db.Integer, primary_key=True)
    RentStart = db.Column(db.Date , nullable=False)
    RentEnd = db.Column(db.Date , nullable=False)
    ClientCin = db.Column(db.String(255))
    ClientName = db.Column(db.String(255))
    NumeroChambre = db.Column(db.Integer)
    bookId = db.Column ( db.Integer , db.ForeignKey('BookList.Id') )
    bookTiltle = db.Column(db.String(255))


    

@app.route('/book_<int:id>_updated_succesfully', methods=['POST','GET'])
def book_updated_succesfully(id):
    if request.method == 'POST':
        book_to_modify=BookList.query.get_or_404(id)
        book_to_modify.author=request.form['Author']
        book_to_modify.title=request.form['Title']
        book_to_modify.description=request.form['Description']            
        book_to_modify.price=request.form['Price']
        book_to_modify.quantity=request.form['Quantity']
        try:
            db.session.commit()
            return render_template('book_updated_succesfully.html')
        except:
            return render_template('error.html')
    else:
        return redirect('/modify/<int:id>')

@app.route('/modify/<int:id>', methods=['POST','GET'])
def select(id):
    book_to_modify=BookList.query.get_or_404(id)
    id=book_to_modify.Id
    return render_template('modify.html', book_to_modify=book_to_modify , id=id)


@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete=BookList.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('error.html')

@app.route("/",methods=["POST","GET"])
def home(): 
    booklist=BookList.query
    return render_template('index.html',booklist=booklist)



@app.route("/addbook",methods=["POST","GET"])
def addbook(): 
    return render_template('addbook.html')





@app.route("/rent/<int:id>",methods=["POST","GET"])
def rentabook_page(id):
    book_to_modify=BookList.query.get_or_404(id)
    id=book_to_modify.Id
    return render_template('rentabook.html',book_to_modify=book_to_modify,id=id)


@app.route("/book_<int:id>_rented_succesfully",methods=["POST","GET"])
def rentabook(id):
    book_to_rent=BookList.query.get_or_404(id)
    bookId = book_to_rent.Id
    RentEnd = datetime.datetime.strptime(request.form.get("RentEnd"),'%Y-%m-%d')
    RentStart = datetime.datetime.strptime(request.form.get("RentStart"),'%Y-%m-%d')
    ClientName = request.form.get("ClientName")
    ClientCin = request.form.get("ClientCin")
    NumeroChambre = request.form.get("NumeroChambre")
    bookTiltle = book_to_rent.title

    if not RentEnd or not RentStart or not ClientName or not ClientCin or not NumeroChambre:
        return render_template('error.html')

    if request.method=="POST":   
        try :
            newclient = Clients( Cin = ClientCin , Name = ClientName)
            newrent = Rent( RentEnd=RentEnd , RentStart=RentStart , ClientName=ClientName , ClientCin=ClientCin , NumeroChambre=NumeroChambre , bookId = bookId , bookTiltle = bookTiltle)
            db.session.add(newrent)
            db.session.add(newclient)
            db.session.commit()
            book_to_rent.quantity-=1
            return render_template("Book_rented_succesfully.html")
        except:
            return render_template("error.html")

        
        





@app.route("/Thanks", methods=["POST"])

def Thanks():

    Author = request.form.get("Author")
    Title = request.form.get("Title")
    Quantity = request.form.get("Quantity")
    Price = request.form.get("Price")

    if not Author or not Title or not Quantity or not Price :
        return render_template('fail.html')

    if request.method=="POST":
        author=request.form['Author']
        title=request.form['Title']
        quantity=(request.form['Quantity'])
        price=(request.form['Price'])
        description=request.form['Description']

        try :
            newbook = BookList( author=author , title=title , quantity=quantity ,price=price , description=description)
            db.session.add(newbook)
            db.session.commit()
            return render_template("Thanks.html")
        except:
            return render_template("fail.html")
    return render_template('fail.html')

@app.route("/rapport",methods=["POST","GET"])
def rapport(): 
    rapport=Rent.query
    return render_template('rapport.html',rapport=rapport)


if __name__=='__main__':
    app.run(debug=True)


    # for i in range(50):
    #     letters = string.ascii_lowercase
    #     letterss = string.ascii_lowercase
    #     descletters = string.ascii_lowercase
    #     title = ''.join(random.choice(letters) for i in range(10))
    #     author = ''.join(random.choice(letterss) for i in range(10))
    #     desc = ''.join(random.choice(descletters) for i in range(10))
    #     quan=random.randint(1,40)
    #     price=random.randint(1,100)
    #     newbook = BookList( author=author , title=title , quantity=quan ,price=price , description=desc)
    #     db.session.add(newbook)
    #     db.session.commit()

# for i in range(50):
#     start_date = datetime.date(2020, 1, 1)
#     end_date = datetime.date(2020, 2, 1)
#     time_between_dates = end_date - start_date
#     days_between_dates = time_between_dates.days
#     random_number_of_days = random.randrange(days_between_dates)
#     random_date = start_date + datetime.timedelta(days=random_number_of_days)
#     random_date1 = start_date + datetime.timedelta(days=random_number_of_days)
#     id = random.randint(1,100)
#     title = BookList.query.get_or_404(id).title
#     nc = random.randint(1,100)
#     letters = string.ascii_lowercase
#     cin = ''.join(random.choice(letters) for i in range(10))
#     letterss = string.ascii_lowercase
#     name = ''.join(random.choice(letterss) for i in range(10))
#     newrent=Rent( RentEnd=random_date , RentStart=random_date1 , ClientName=name , ClientCin=cin , NumeroChambre=nc , bookId = id , bookTiltle = title)
#     db.session.add(newrent)
#     db.session.commit()