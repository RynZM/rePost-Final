from flask import Flask, request, render_template, render_template_string
from PIL import Image
import pytesseract
from waitress import serve
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)

#find tesseract in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    if request.method == 'POST':
        # Get the uploaded photo
        file = request.files['file']

        # Read the text from the image 
        image = Image.open(file)
        
        text = pytesseract.image_to_string(image)
        text = str(text)
        
        formatted_text = text.replace('\n', '<br>')

        paragraphs = []
        current_paragraph = ''
        
        for line in formatted_text.split('<br>'):
            line = line.strip()
            if line:
                if len(line.split()) < 3 and current_paragraph:
                    current_paragraph += '' + line
                else:
                    if current_paragraph:
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = ''
                    current_paragraph += line + ' '
            else:
                if current_paragraph:
                    paragraphs.append(current_paragraph.strip())
                    current_paragraph = ''
        
        if current_paragraph:
            paragraphs.append(current_paragraph.strip())

        # Render the text on the page
        return render_template('result.html', text=text, paragraphs=paragraphs)

    # Render the form on the page
    return render_template('index.html')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'McFarland.Z.Ryan@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_email(recipient, text):
    subject = "Text extracted from image"
    body = text
    sender = app.config['MAIL_USERNAME']
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body
    mail.send(msg)

@app.route('/send-email_route', methods=['POST'])
def send_email_route():
    recipient = request.form['recipient_email']
    text = request.form['text']
    send_email(recipient, text)
    return 'Text extracted and Email has been sent!'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)



# CODE FOR BOOKS SPECIFICALLY
# paragraphs = []
        # current_paragraph = ''

        # for line in formatted_text.split('<br>'):
        #     line = line.strip()
        #     if line:
        #         current_paragraph += line + ' '
        #     else:
        #         if current_paragraph:
        #             paragraphs.append(current_paragraph.rstrip())
        #             current_paragraph = ''

