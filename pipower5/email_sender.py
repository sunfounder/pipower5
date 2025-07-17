from enum import StrEnum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json

DEFAULT_SMTP_PORT = 465
DEFAULT_SMTP_USE_TLS = False

class EmailModes(StrEnum):
    BATTERY_ACTIVATED = 'battery_activated'
    LOW_BATTERY = 'low_battery'
    POWER_DISCONNECTED = 'power_disconnected'
    POWER_RESTORED = 'power_restored'
    POWER_INSUFFICIENT = 'power_insufficient'
    BATTERY_CRITICAL_SHUTDOWN = 'battery_critical_shutdown'
    BATTERY_VOLTAGE_CRITICAL_SHUTDOWN = 'battery_voltage_critical_shutdown'

EMAIL_MODES = [
    EmailModes.BATTERY_ACTIVATED,
    EmailModes.LOW_BATTERY,
    EmailModes.POWER_DISCONNECTED,
    EmailModes.POWER_RESTORED,
    EmailModes.POWER_INSUFFICIENT,
    EmailModes.BATTERY_CRITICAL_SHUTDOWN,
    EmailModes.BATTERY_VOLTAGE_CRITICAL_SHUTDOWN,
]

TEMPLATE_DIR = '/opt/pipower5/email_templates/'
TEMPLATES = TEMPLATE_DIR + 'email_templates.json'

class EmailSender():
    def __init__(self, config=None):
        self.config = config
        self.templates = None
        self.load_templates()
        server = self.connect()
        server.close()
        self.ready = True

    def is_ready(self):
        return self.ready

    def load_templates(self):
        if os.path.exists(TEMPLATES):
            with open(TEMPLATES, 'r') as f:
                self.templates = json.load(f)
        else:
            raise FileNotFoundError(f"Email templates file {TEMPLATES} not found")

    def send_preset_email(self, mode, data):
        if not self.is_ready():
            return "Email sender not ready"
        template = self.templates[mode]
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
        
        smtp_email = self.config.get("smtp_email", None)
        smtp_password = self.config.get("smtp_password", None)
        smtp_server = self.config.get("smtp_server", None)
        smtp_port = self.config.get("smtp_port", DEFAULT_SMTP_PORT)
        smtp_use_tls = self.config.get("smtp_use_tls", DEFAULT_SMTP_USE_TLS)

        if not smtp_email or not smtp_server:
            raise ValueError("SMTP email or server is not set")

        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()
        
        if smtp_password:
            server.login(smtp_email, smtp_password)
        
        return server

    def send_email(self, subject, body, attachment_path=None):
        """
        使用配置字典发送邮件
        
        参数:
        subject: 邮件主题
        body: 邮件正文
        attachment_path: 附件路径(可选)
        """

        send_email_to = self.config.get("send_email_to", DEFAULT_CONFIG["send_email_to"])
        smtp_email = self.config.get("smtp_email", DEFAULT_CONFIG["smtp_email"])

        message = MIMEMultipart()
        message["From"] = smtp_email
        message["To"] = send_email_to
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
            server.sendmail(message["From"], send_email_to, text)
            server.quit()
            return True
        except Exception as e:
            return e
