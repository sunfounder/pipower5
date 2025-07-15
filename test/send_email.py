from enum import StrEnum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json

# 默认配置字典 - 本地SMTP服务
DEFAULT_CONFIG = {
    "smtp_sender": "pipower5@localhost",
    "smtp_receiver": "pipower5@localhost",
    "smtp_password": "",
    "smtp_server": "localhost",
    "smtp_port": 25,
    "smtp_use_tls": False
}

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
        self._load_templates()

    def _load_templates(self):
        if os.path.exists(TEMPLATES):
            with open(TEMPLATES, 'r') as f:
                self.templates = json.load(f)

    def send_email(self, mode, data):
        data['device_name'] = 'PiPower 5'
        print(data)

        template = self.templates[mode]
        subject = template['subject'].format(**data)
        body_path = template['body_path']
        with open(TEMPLATE_DIR + body_path, 'r') as f:
            body = f.read()
        body = body.format(**data)
        attachment_path = None
        if 'attachment_path' in template:
            attachment_path = template['attachment_path'].format(**data)

        return self._send_email(subject, body, attachment_path)

    def _send_email(self, subject, body, attachment_path=None):
        """
        使用配置字典发送邮件
        
        参数:
        subject: 邮件主题
        body: 邮件正文
        attachment_path: 附件路径(可选)
        """

        smtp_receiver = self.config.get("smtp_receiver", "noreply@localhost")
        smtp_sender = self.config.get("smtp_sender", "noreply@localhost")
        smtp_password = self.config.get("smtp_password", "")
        smtp_server = self.config.get("smtp_server", "localhost")
        smtp_port = self.config.get("smtp_port", 25)
        smtp_use_tls = self.config.get("smtp_use_tls", False)
        
        message = MIMEMultipart()
        message["From"] = smtp_sender
        message["To"] = smtp_receiver
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
        
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()
        
        if smtp_password:
            server.login(smtp_sender, smtp_password)
        
        text = message.as_string()
        server.sendmail(message["From"], smtp_receiver, text)
        server.quit()

if __name__ == '__main__':
    config= {
        'send_email_on': [
            "battery_activated",
            "low_battery",
            "power_disconnected",
            "power_restored",
            "power_insufficient",
            "battery_critical_shutdown",
            "battery_voltage_critical_shutdown",
        ],
        "smtp_receiver": "381039379@qq.com",
        "smtp_sender": "381039379@qq.com",
        "smtp_password": "bjwkbepuzepebieb",
        "smtp_server": "smtp.qq.com",
        "smtp_port": 465,
        "smtp_use_tls": False  # 465端口使用SSL，不需要TLS
    }
    data = {
        'battery_percentage': 100,
        'battery_voltage': 12.34,
        'battery_current': 5.67,
        'battery_power': 68.6,
        'battery_temperature': 25.0,
    }
    email_sender = EmailSender(config)
    # email_sender.send_email(EmailModes.BATTERY_ACTIVATED, data)
    email_sender.send_email(EmailModes.LOW_BATTERY, data)