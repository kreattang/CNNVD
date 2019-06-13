#!/usr/bin/python3

import ftplib
from contextlib import closing

with closing(ftplib.FTP('ftp.example.com')) as ftp:
    try:
        ftp.login('user7', 's$cret')

        ftp.mkd('newdir')

        files = []

        ftp.retrlines('LIST', files.append)

        for fl in files:
            print(fl)

    except ftplib.all_errors as e:
        print('FTP error:', e)