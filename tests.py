# -*- coding: utf-8 -*-

import datetime
from md5 import md5

print md5(str(datetime.datetime.now())).hexdigest()[5:13].lower()

today = datetime.date.today()
print 'Today    :', today

one_day = datetime.timedelta(days=1)
print 'One day  :', one_day

yesterday = today - one_day
print 'Yesterday:', yesterday

tomorrow = today + one_day
print 'Tomorrow :', tomorrow.strftime('%d.%m.%Y')
