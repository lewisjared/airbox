"""
Low level abstraction over smtplib for sending emails from the Aurora

It looks like you don't need to specify passwords to send emails which simplifies things a lot
"""
import smtplib
from base64 import b64encode
from logging import getLogger

from airbox import config

logger = getLogger(__name__)

MARKER = "AUNIQUEMARKER"

HEADER_SEC = """From: {}
To: {}
Subject: {}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="{}"

--{}
"""

BODY_SEC = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

{}

--{}
"""

ATTACHMENT_SEC = """Content-Type: {}; name=\"{}\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename={}

{}

--{}"""


def encode_attachment(fname, content_type='application/pdf'):
    # Read a file and encode it into base64 format
    fo = open(fname, "rb")
    filecontent = fo.read()

    b64 = b64encode(filecontent).decode()
    # Define the attachment section
    return ATTACHMENT_SEC.format(content_type, fname, fname, b64, MARKER)


def addrs_to_list(to):
    return ", ".join(['<{}>'.format(t) for t in to])


def sendmail(to, subject, content, attachments=None):
    from_addr = config['email_from']
    if attachments is None:
        attachments = []
    header = HEADER_SEC.format(from_addr, addrs_to_list(to), subject, MARKER, MARKER)

    # Define the message action
    body = BODY_SEC.format(content, MARKER)

    message = header + body + "\n".join([encode_attachment(fname) for fname in attachments]) + '--'

    try:
        smtp = smtplib.SMTP('smtp.aad.gov.au')
        smtp.sendmail(from_addr, to, message)
    except smtplib.SMTPException:
        logger.exception('Failed to send message:\n{}'.format(message))
        raise
