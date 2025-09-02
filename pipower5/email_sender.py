
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
import logging

DEFAULT_SMTP_PORT = 465
DEFAULT_SMTP_SECURITY = 'ssl'

TEMPLATE_DIR = '/opt/pipower5/email_templates/'
TEMPLATES = TEMPLATE_DIR + 'email_templates.json'

class EmailSender():
    def __init__(self, config=None, log=None):
        self.log = log or logging.getLogger(__name__)
        self.templates = None
        self.load_templates()

        self.send_email_to = None
        self.smtp_email = None
        self.smtp_password = None
        self.smtp_server = None
        self.smtp_port = DEFAULT_SMTP_PORT
        self.smtp_security = DEFAULT_SMTP_SECURITY

        self.update_config(config)
        # server = self.connect()
        # server.close()
        self.ready = True

    def is_ready(self):
        return self.ready

    def update_config(self, config):
        patch = {}
        if 'send_email_to' in config:
            to = config.get("send_email_to", None)
            self.send_email_to = to
            patch['send_email_to'] = to
            self.log.debug(f"Set send email to: {to}")
        if 'smtp_email' in config:
            email = config.get("smtp_email", None)
            self.smtp_email = email
            patch['smtp_email'] = email
            self.log.debug(f"Set smtp email: {email}")
        if 'smtp_password' in config:
            password = config.get("smtp_password", None)
            self.smtp_password = password
            patch['smtp_password'] = password
            self.log.debug(f"Set smtp password.")
        if 'smtp_server' in config:
            server = config.get("smtp_server", None)
            self.smtp_server = server
            patch['smtp_server'] = server
            self.log.debug(f"Set smtp server: {server}")
        if 'smtp_port' in config:
            port = config.get("smtp_port", DEFAULT_SMTP_PORT)
            self.smtp_port = port
            patch['smtp_port'] = port
            self.log.debug(f"Set smtp port: {port}")
        if 'smtp_security' in config:
            security = config.get("smtp_security", None)
            if security not in ['none', 'ssl', 'tls']:
                raise ValueError(f"smtp_security must be 'none', 'ssl' or 'tls', not {security}")
            self.smtp_security = security
            patch['smtp_security'] = security
            self.log.debug(f"Set smtp security: {security}")
        return patch

    def load_templates(self):
        if os.path.exists(TEMPLATES):
            with open(TEMPLATES, 'r') as f:
                self.templates = json.load(f)
        else:
            raise FileNotFoundError(f"Email templates file {TEMPLATES} not found")

    def send_preset_email(self, event, data):
        if not self.is_ready():
            return "Email sender not ready"
        template = self.templates[event]
        subject = template['subject'].format(**data)
        body_path = template['body_path']
        body_path = TEMPLATE_DIR + body_path
        with open(body_path, 'r') as f:
            body = f.read()
        body = body.format(**data)
        attachment_path = None
        if 'attachment_path' in template:
            attachment_path = template['attachment_path'].format(**data)

        return self.send_email(subject, body, attachment_path)

    def connect(self):
        """
        连接SMTP服务器

        Returns:
            smtplib.SMTP: 连接成功返回SMTP服务器对象，否则返回None
        """
        
        if not self.smtp_email or not self.smtp_server:
            raise ValueError("SMTP email or server is not set")

        self.log.debug(f"Connecting to smtp server: {self.smtp_server}:{self.smtp_port}, security: {self.smtp_security}")
        self.log.debug(f"SMTP email: {self.smtp_email}")
        
        if self.smtp_security == 'none':
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        elif self.smtp_security == 'ssl':
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        elif self.smtp_security == 'tls':
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
        
        if self.smtp_password:
            server.login(self.smtp_email, self.smtp_password)
        
        return server

    def send_email(self, subject, body, attachment_path=None):
        """
        使用配置字典发送邮件
        
        参数:
        subject: 邮件主题
        body: 邮件正文
        attachment_path: 附件路径(可选)
        """

        message = MIMEMultipart()
        message["From"] = self.smtp_email
        message["To"] = self.send_email_to
        message["Subject"] = subject
        
        message.attach(MIMEText(body, 'html'))
        
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            message.attach(part)
        
        try:
            server = self.connect()
            text = message.as_string()
            server.sendmail(message["From"], self.send_email_to, text)
            server.quit()
            return True
        except Exception as e:
            return e
