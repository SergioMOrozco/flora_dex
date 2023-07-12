from bs4 import BeautifulSoup
import re

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

soup = BeautifulSoup(open("test.html").read(), "html.parser")
txt = (t.text for t in soup.find_all("span"))

for span in soup.find_all('span'):
	print('"' + cleanhtml(str(span)) + '",')

