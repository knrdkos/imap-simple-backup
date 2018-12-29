#!/usr/bin/python3

import imaplib
import mailbox as mb

from optparse import OptionParser

SUCCESS = 'OK'

parser = OptionParser()
parser.add_option("--imap-server",
                  dest="IMAP_SERVER",
                  default='imap.gmail.com')
parser.add_option("-o",
                  "--output-dir",
                  dest="OUTPUT_DIRECTORY",
                  default='dumps.mbox')

parser.add_option("-a",
                  "--imap-account",
                  dest="EMAIL_ACCOUNT")
parser.add_option("-p",
                  "--password",
                  dest="PASSWORD")

(options, args) = parser.parse_args()

mailbox = imaplib.IMAP4_SSL(options.IMAP_SERVER)
mailbox.login(options.EMAIL_ACCOUNT, options.PASSWORD)

select_typ, select_data = mailbox.select('"[Gmail]/All Mail"', readonly=True)

if select_typ == SUCCESS:
    search_typ, search_data = mailbox.search(None, "ALL")
    if search_typ == SUCCESS:
        dest_mbox = mb.mbox(options.OUTPUT_DIRECTORY, create=True)
        dest_mbox.lock()
        messages = search_data[0].split()
        total = len(messages)
        for m in messages:
            print("downloading %s/%s" % (m.decode("utf-8"), total))
            t, d = mailbox.fetch(m, '(RFC822)')
            if t == SUCCESS:
                dest_mbox.add(d[0][1])
        dest_mbox.close()
    mailbox.close()
else:
    print("ERR: %s" % select_typ)

mailbox.logout()
