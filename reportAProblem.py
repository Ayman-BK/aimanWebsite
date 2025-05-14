from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# إعدادات البريد الإلكتروني
SMTP_SERVER = 'info@aimanomar.de'  # استبدلها بمزود البريد الإلكتروني الخاص بك
SMTP_PORT = 465  # أو 465 إذا كنت تستخدم SSL     587
SMTP_USERNAME = 'info@aimanomar.de'  # استبدلها بعنوان بريدك الإلكتروني
SMTP_PASSWORD = 'Ayman-BK-135'  # استبدلها بكلمة المرور الخاصة بك
RECIPIENT_EMAIL = 'info@aimanomar.de'  # البريد الإلكتروني المستلم

@app.route('/')
def index():
    return render_template_string(open('report-a-problem.html').read())

@app.route('/submit-problem', methods=['POST'])
def submit_problem():
    # الحصول على البيانات من النموذج
    name = request.form.get('name')
    email = request.form.get('email')
    problem_description = request.form.get('problemDescription')
    screenshot = request.files.get('screenshot')

    # إنشاء الرسالة الإلكترونية
    subject = "Problem Reported on Website"
    body = f"""
    Problem reported by: {name}
    Email: {email}

    Problem Description:
    {problem_description}
    """

    # إنشاء الرسالة البريدية
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # إرسال البريد الإلكتروني عبر SMTP
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # إذا كنت تستخدم اتصالًا غير مشفر
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, text)
        server.quit()
        return "Problem reported successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
