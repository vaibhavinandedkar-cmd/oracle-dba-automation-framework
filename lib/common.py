import oracledb
import yaml
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import os

def load_config():
    with open('config/config.yaml') as f:
        return yaml.safe_load(f)

config = load_config()

def setup_logging(module_name="framework"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"{log_dir}/{module_name}_{datetime.now():%Y%m%d}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )
    return logging.getLogger()

def send_email(subject, html_body):
    if not config.get('email', {}).get('enabled', False):
        return
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config['email']['from_email']
    msg['To'] = config['email']['to_email']
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(config['email']['smtp_server'], config['email']['smtp_port']) as server:
            server.starttls()
            server.login(config['email']['from_email'], config['email'].get('password', ''))
            server.send_message(msg)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
