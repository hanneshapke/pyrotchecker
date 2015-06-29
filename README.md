# PyROTChecker
PYthonROTChecker is a tool to check websites for given ROT-n strings or keywords

### Try it out
https://pyrotchecker.herokuapp.com/


### Functionality
The PYthonROTChecker allows searching entire websites or given nodes of sites for keywords which are encrypted by the [rotate by n places](https://en.wikipedia.org/wiki/ROT13) cypher. This tools provides a simple API endpoint (based on Flask)), a simple front-end site (based on AngularJS), and a Python script.

### How to use the PYthonROTChecker?
* Use the **website** [https://pyrotchecker.herokuapp.com/](https://pyrotchecker.herokuapp.com/)
* Make an **API call** from the console via curl
```
curl --request GET "https://pyrotchecker.herokuapp.com/api/?url=https://en.wikipedia.org/wiki/ROT13&q=To%20get%20to%20the%20other%20side"
```
* Execute **Python script** with `python rotchecker.py`
```
python app/rotchecker.py --url https://en.wikipedia.org/wiki/ROT13 --str="To get to the other side"
```

The following functionality is implemented and usable via the Python script:
```
-u --url > request url of the website (required)
-s --str > query string/keywords, can be comma separated (required)
-t --tag > node to be checked (default: body)
-n --num > specify a specific rot shift (default: 13)
```

### How is the code checking for ROT-n terms?
* All parameters (e.g. url, search keywords, html tags) are validated 
* URL will be retrieved
* If status is 200, the preferred node will be extracted from the downloaded data
* Before search inf the remaining data for the keywords, the data will be stripped from remaining html tag to prevent that messages are hidden with tags in between (e.g. Gb trg gb gur <b>bgu</b>re fvqr)
* The keywords are converted into the rot-n space
* The remaining data is then searched for the converted keywords


### Suggestions for further improvements
* Add more unit and functional tests
* Allow functionality for extended ROT cyphers, e.g. ROT-47 which includes special characters
* API submissions via POST and a json construct
* Cache already checked sites via Redis
