import sys
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates

from datetime import datetime

temp = Counter()
for line in sys.stdin:
    success_time = line.split('/')[0]
    temp[datetime.strptime(success_time, '%H%M%S')] += 1

result = sorted(temp.items(), key=lambda x: x[0])
dates = matplotlib.dates.date2num(list(map(lambda x: x[0], result)))
counts = list(map(lambda x: x[1], result))
plt.plot_date(dates, counts)
plt.show()

