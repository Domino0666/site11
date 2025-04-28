from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv





app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

load_dotenv('config.env')

mail_receive = os.getenv('MAIL_RECEIVE')

app.config['MAIL_SERVER'] =  os.getenv('MAIL_SERVER') # 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') # 587
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') #True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') #'fabian.czesio@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') #'ptpg ahrh sazk lkkq'
app.config['MAIL_DEFAULT_SENDER'] = (f'{os.getenv('MAIL_DAFAULT_SENDER_NAME')}', f'{os.getenv('MAIL_USERNAME')}') # ENST, EMAIL
mail = Mail(app)

def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)


limiter = Limiter(
    key_func=get_ip,
    app=app
    )


@app.errorhandler(429)
def ratelimit_handler(e):
    print(f'[RATE LIMIT] {get_ip()} przekroczył limit.')
    return redirect(url_for('error', error=429))

@app.errorhandler(404)
def notfound_handler(e):
    return redirect(url_for('error', error=404))

@app.errorhandler(500)
def servererror_handler(e):
    return redirect(url_for('error', error=500))

@app.route('/error/<error>/')
def error(error):
    if str(error) == "429":
        message = "Przekroczono limit zapytań do serwera."
    elif str(error) == "404":
        message = "Nie znaleziono strony."
    elif str(error) == "500":
        message = "Ups... wygląda na to że popełniliśmy błąd."

    return render_template('429.html', error=error, message=message), int(error)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/oferta/")
def offer():
    return render_template("offer.html")

@app.route('/kontakt/', methods=['GET', 'POST'])
@limiter.limit("2 per hour", methods=["POST"])
def kontakt():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        city = request.form.get('location')
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    padding: 20px;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #004E8A;
                    padding: 20px;
                    text-align: center;
                    color: white;
                }}
                .header img {{
                    max-width: 160px;
                    margin-bottom: 10px;
                }}
                .content {{
                    padding: 20px;
                }}
                .content h2 {{
                    margin-top: 0;
                    color: #004E8A;
                }}
                .info p {{
                    margin: 8px 0;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                    padding: 15px;
                }}
                hr {{
                    border: none;
                    border-top: 1px solid #ddd;
                    margin: 30px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://enst.pl/pliki/logo.png" alt="ENST Logo">
                    <h2>Nowa wiadomość z formularza kontaktowego</h2>
                </div>
                <div class="content">
                    <div class="info">
                        <p><strong>Imię i nazwisko:</strong> {name}</p>
                        <p><strong>Email nadawcy:</strong> {email}</p>
                        <p><strong>Miasto:</strong> {city}</p>
                        
                        <hr>

                        <p><strong>Temat:</strong> {subject}</p>
                        <p><strong>Treść wiadomości:</strong><br>{message}</p>
                    </div>
                </div>
                <div class="footer">
                    Wiadomość została wysłana automatycznie przez formularz kontaktowy na stronie enst.pl
                </div>
            </div>
        </body>
        </html>
        """


        html_confrim = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 650px;
                    margin: auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #004E8A;
                    color: white;
                    text-align: center;
                    padding: 30px 20px 20px;
                }}
                .header img {{
                    max-width: 160px;
                    margin-bottom: 10px;
                }}
                .header h2 {{
                    margin: 10px 0 0;
                }}
                .content {{
                    padding: 30px 25px;
                    color: #333;
                }}
                .large-text {{
                    font-size: 18px;
                    font-weight: 600;
                    margin-bottom: 15px;
                }}
                .largem-text {{
                    font-size: 13px;
                    font-weight: 600;
                    margin-bottom: 13px;
                    color: #999;
                }}
                .medium-text {{
                    font-size: 16px;
                    margin-top: 25px;
                    margin-bottom: 15px;
                }}
                .data-box {{
                    background-color: #f0f8ff;
                    border: 1px solid #cce0ff;
                    border-radius: 8px;
                    padding: 15px 20px;
                    margin-top: 15px;
                }}
                .data-box p {{
                    font-size: 14px;
                    margin: 6px 0;
                }}
                hr {{
                    border: none;
                    border-top: 1px solid #ddd;
                    margin: 30px 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #004E8A;
                    color: white !important;
                    text-decoration: none !important;
                    font-weight: 500;
                    padding: 12px 28px;
                    border-radius: 6px;
                    margin-top: 25px;
                    font-size: 15px;
                    text-align:center;
                }}
                .btn:hover {{
                    background-color: #003766;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #999;
                    padding: 20px 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://enst.pl/pliki/logo.png" alt="ENST Logo">
                    <h2>Potwierdzenie otrzymania wiadomości</h2>
                </div>
                <div class="content">
                    <p class="largem-text" style="text-align:center;">Dziękujemy za kontakt z ENST.</p>
                    <p class="large-text" style="text-align:center;">Otrzymaliśmy Twoją wiadomość i postaramy się odpowiedzieć jak najszybciej.</p>

                    <hr>

                    <h3>Twoje dane kontaktowe:</h3>
                    <div class="data-box">
                        <p><strong>Imię i nazwisko:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Miasto:</strong> {city}</p>
                    </div>

                    <p class="medium-text" style="text-align:center;">
                        Prosimy, upewnij się, że powyższe dane są poprawne.<br>
                        Jeżeli zawierają błędy, prosimy o ponowne przesłanie formularza z poprawnymi informacjami.
                    </p>

                    <a href="https://enst.pl/kontakt" class="btn" style="text-decoration:none !important; color:white !important; background-color: #09b649 !important; text-align:center;">Popraw dane</a>
                </div>
                <div class="footer">
                    Wiadomość została wygenerowana automatycznie – prosimy na nią nie odpowiadać.
                </div>
            </div>
        </body>
        </html>
        """



        try:
            msg = Message(subject=f"[{city}] {subject}", recipients=[mail_receive], html=html_body)
            mail.send(msg)
            flash('Wiadomość została wysłana!', 'success')
        except Exception as e:
            print(e)
            flash('Wystąpił błąd przy wysyłaniu wiadomości. Spróbuj później.', 'danger')
        try:
            msg = Message(subject=f"[ENST] - Potwierdzenie", recipients=[f'{email}'], html=html_confrim)
            mail.send(msg)
            flash('Potwierdzenie zostało wysłane na podany adres e-mail', 'success')
        except:
            print(e)
            flash('Wiadomość została wysłana pomyślnie lecz nie udało się wysłać potwierdzenia na podany adres email, czy jest on poprawny?')
        return redirect(url_for('kontakt'))
    
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
