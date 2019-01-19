#!/bin/env python3

from urllib import request
url = "https://segredos.licoes.com/header_test.php"
response = request.urlopen(url)
print(response.info().items())
