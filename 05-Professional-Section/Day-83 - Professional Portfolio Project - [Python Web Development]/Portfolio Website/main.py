from flask import Flask, render_template, request, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Email configuration
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send email
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS
            msg['Subject'] = f"Portfolio Contact Form: {name}"

            body = f"""
            Name: {name}
            Email: {email}
            Message: {message}
            """
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, text)
            server.quit()

            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
            print(str(e))

        return render_template('contact.html')

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
