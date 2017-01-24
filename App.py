from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drivers_records.sqlite3'
app.config['SECRET_KEY'] = "secret"

db = SQLAlchemy(app)

class Driver_records(db.Model):

    __tablename__ = 'driver'
    id = db.Column('DriverID', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    orderPickup = relationship("Order_Table_Pickup")
    orderDel = relationship("Order_Table_Del")

    def __init__(self, name, address, city):

        self.name = name
        self.address = address
        self.city = city

class Order_Table_Pickup(db.Model):

    __tablename__ = 'orderPickup'
    id = db.Column('OrderNum', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    driverID = db.Column(db.Integer, ForeignKey('driver.DriverID'))

    def __init__(self, FromName, FromAddress, FromCity, driverAssign):

        self.FromName = FromName
        self.FromAddress = FromAddress
        self.FromCity = FromCity
        self.driverAssign = driverAssign


class Order_Table_Del(db.Model):

    __tablename__ = 'orderDel'
    id = db.Column('OrderNum', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    driverID = db.Column(db.Integer, ForeignKey('driver.DriverID'))

    def __init__(self, ToName, ToAddress, ToCity, driverAssign):

        self.ToName = ToName
        self.ToAddress = ToAddress
        self.ToCity = ToCity
        self.driverAssign = driverAssign


@app.route('/')
def home_page():
    return render_template('home_page.html', driver_records = Driver_records.query.all())


@app.route('/new_driver', methods = ['GET', 'POST'])
def new_driver():

    if request.method == 'POST':

        if not request.form['name'] or not request.form['address'] or not request.form['city']:
            flash('Please enter in all fields.', 'error')

        else:

            driver = Driver_records(request.form['name'], request.form['address'], request.form['city'])

            db.session.add(driver)
            db.session.commit()
            flash('Record added.')
            return redirect(url_for('home_page'))

    return render_template('new_driver.html')

@app.route('/new_order', methods = ['GET','POST'])
def new_order():

    if request.method == 'POST':

        orderPickup = Order_Table_Pickup(request.form['FromName'],request.form['FromAddress'],
        request.form['FromCity'],request.form['driverAssign'])

        orderDel = Order_Table_Del(request.form['ToName'],request.form['ToAddress'],
        request.form['ToCity'],request.form['driverAssign'])

        db.session.add(orderPickup)
        db.session.add(orderDel)
        db.session.commit()


        flash("Order Added")
        return redirect(url_for('home_page'))

    return render_template('new_order.html', driver_records = Driver_records.query.all())

# testing

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
