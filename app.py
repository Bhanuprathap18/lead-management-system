from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Lead table model
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    business_type = db.Column(db.String(100))
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='New')


# Home route
@app.route('/', methods=['GET', 'POST'])
def home():

    success_message = None

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        business_type = request.form['business_type']
        message = request.form['message']

        # Create new lead object
        new_lead = Lead(
            name=name,
            email=email,
            phone=phone,
            business_type=business_type,
            message=message
        )

        # Save to database
        db.session.add(new_lead)
        db.session.commit()

        # Success message
        success_message = f"Thank you {name}! Your lead has been submitted successfully."

    return render_template(
        'index.html',
        success_message=success_message
    )


# Dashboard route
@app.route('/dashboard')
def dashboard():

    search = request.args.get('search')

    if search:

        leads = Lead.query.filter(
            Lead.name.contains(search) |
            Lead.email.contains(search) |
            Lead.business_type.contains(search)
        ).all()

    else:
        leads = Lead.query.all()

    return render_template('dashboard.html', leads=leads)


# Update lead status
@app.route('/update_status/<int:id>/<status>')
def update_status(id, status):

    lead = Lead.query.get(id)

    lead.status = status

    db.session.commit()

    return redirect('/dashboard')


# Run app
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)