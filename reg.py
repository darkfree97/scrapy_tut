import re

referer = 'https://github.com/Xiangrui2019?tab=followers'
match = re.match(r'https://github\.com/(?P<referer>\w+)\?tab=followers', referer)

print(match.group(1))
