"""
Low level abstraction over smtplib for sending emails from the Aurora

It looks like you don't need to specify passwords to send emails which simplifies things a lot
"""

import smtplib
from base64 import b64encode
from logging import getLogger
from os.path import basename

from airbox import config

logger = getLogger(__name__)

MARKER = "AUNIQUEMARKER"

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
    return ATTACHMENT_SEC.format(content_type, basename(fname), basename(fname), b64, MARKER)


def generate_header(params):
    tags = "\n".join(["{}: {}".format(k, v) for k, v in params])
    return tags + "\n\n--{}\n".format(MARKER)


def addrs_to_list(to):
    return ", ".join(['<{}>'.format(t) for t in to])


def sendmail(to, subject, content, attachments=None, cc=None):
    from_addr = config['email_from']
    if attachments is None:
        attachments = []

    # Create the header
    header_kwargs = [
        ("From", from_addr),
        ("To", addrs_to_list(to)),
        ("Subject", subject),
        ("MIME-Version", "1.0"),
        ("Content-Type", 'multipart/mixed; boundary="{}"'.format(MARKER))
    ]
    if cc is not None:
        header_kwargs.insert(2, ("CC", addrs_to_list(cc)))
    header = generate_header(header_kwargs)

    # Define the message action
    body = BODY_SEC.format(content, MARKER)

    message = header + body + \
              "\n".join([encode_attachment(fname, content_type) for content_type, fname in attachments]) + '--'
    logger.info('Sending message "{}" to {}. Total size: {}KB'.format(subject, addrs_to_list(to), len(message) / 1024))
    logger.debug(message)
    if not config['debug']:
        try:
            smtp = smtplib.SMTP('smtp.aad.gov.au')
            smtp.sendmail(from_addr, to, message)
        except smtplib.SMTPException:
            logger.exception('Failed to send message:\n{}'.format(message))
            raise
    else:
        logger.info('Skipping sending email due to debug mode')
