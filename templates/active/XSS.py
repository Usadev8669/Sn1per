# Import any WebDriver class that you would usually import from
# selenium.webdriver from the seleniumrequests module
import sys
from seleniumrequests import Firefox

url = sys.argv[1]
# Simple usage with built-in WebDrivers:
webdriver = Firefox()
response = webdriver.request(
	'GET', f'{url}/xss.php?xss=<script>document.write(INJECTX)</script>'
)
if '<script>document.write(INJECTX)</script>' in response.text:
	print("Vulnerable!")
print(response.text)
webdriver.quit()
SECONDARY_COMMANDS=''
