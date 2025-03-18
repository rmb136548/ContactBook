from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# مدل دیتابیس
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# صفحه اصلی
@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

# افزودن مخاطب
@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')

    if name and phone:
        new_contact = Contact(name=name, phone=phone)
        db.session.add(new_contact)
        db.session.commit()

    return redirect(url_for('index'))

# حذف مخاطب
@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
    
    return redirect(url_for('index'))

# اجرای برنامه
if __name__ == '__main__':
    with app.app_context():  # این خط مشکل را حل می‌کند
        db.create_all()
    app.run(debug=True)
