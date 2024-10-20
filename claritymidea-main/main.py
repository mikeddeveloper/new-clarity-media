from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl  
import traceback

app = Flask(__name__)

SENDER_EMAIL = 'adegboyegamichael291@gmail.com'        # Your gmail
SENDER_PASSWORD = 'ardl dftn odhc kvrr'        # The app apssword i told you about
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()  
    user_name = data.get('name')
    user_phone = data.get('phone')
    user_email = data.get('email')
    user_event = data.get('event')
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL
        msg['Subject'] = f'Message from {user_email}'

        html_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }}
                .container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #333;
                    margin-bottom: 10px;
                }}
                .content {{
                    margin-bottom: 20px;
                }}
                .footer {{
                    font-size: 12px;
                    color: #888;
                    margin-top: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Message from {user_name}</h2>
                <div class="content">
                    <p><strong>Email:</strong> {user_email}</p>
                    <p><strong>Name:</strong> {user_name}</p>
                    <p><strong>Phone:</strong> {user_phone}</p>
                    <p><strong>Event:</strong> {user_event}</p>
                </div>
                <div class="footer">
                    <p>This email was sent from your website contact form.</p>
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))  

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())  # Changed sender to SENDER_EMAIL

        return jsonify({'status': 'success', 'message': 'Email sent successfully!'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())  # Logs full error traceback
        return jsonify({'status': 'error', 'message': 'Internal Server Error. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
