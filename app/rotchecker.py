import re
import urllib2
from urllib2 import URLError


class ROTCypher:
    ''' ... '''

    def __init__(self, rot_shift=13):
        ''' Sets the initial rot shift for th cypher '''
        self.rot_shift = rot_shift
        # self.alpha, self.rot = self.get_rot_sets(rot_shift)
        self.message = None
        self.status = 'alert alert-danger'

    # def get_rot_sets(self, num_char_diff):
    #     ''' Create char and rot strings for the conversion, default: 13 '''
    #     uppercase_set = ''.join(chr(ord('A') + i) for i in xrange(26))
    #     lowercase_set = ''.join(chr(ord('a') + i) for i in xrange(26))
    #     uppercase_rot = ''.join(
    #         [uppercase_set[num_char_diff:], uppercase_set[:num_char_diff]])
    #     lowercase_rot = ''.join(
    #         [lowercase_set[num_char_diff:], lowercase_set[:num_char_diff]])
    #     return (uppercase_set + lowercase_set, uppercase_rot + lowercase_rot)

    @property
    def alpha(self):
        ''' Sets the alphabetic lookup string '''
        uppercase_set = ''.join(chr(ord('A') + i) for i in xrange(26))
        lowercase_set = ''.join(chr(ord('a') + i) for i in xrange(26))
        return uppercase_set + lowercase_set

    @property
    def rot(self):
        ''' Sets the rot lookup string '''
        uppercase_set = ''.join(chr(ord('A') + i) for i in xrange(26))
        lowercase_set = ''.join(chr(ord('a') + i) for i in xrange(26))
        uppercase_rot = ''.join(
            [uppercase_set[self.rot_shift:], uppercase_set[:self.rot_shift]])
        lowercase_rot = ''.join(
            [lowercase_set[self.rot_shift:], lowercase_set[:self.rot_shift]])
        return uppercase_rot + lowercase_rot

    def checkcharacter_error(self, char):
        ''' Raise ValueError if char is longer than one character '''
        if len(char) > 1:
            raise ValueError('Only converts single char or rot characters')

    def chrtrot(self, char):
        ''' Convert single alphabet character to rot13 '''
        self.checkcharacter_error(char)
        if re.match('[a-zA-Z]+$', char):
            return self.rot[self.alpha.index(char)]
        return char

    def rottchr(self, char):
        ''' Convert single rot13 character to alphabet character '''
        self.checkcharacter_error(char)
        if re.match('[a-zA-Z]+$', char):
            return self.alpha[self.rot.index(char)]
        return char

    def convert_to_rot(self, text):
        ''' converts a string to rot13 '''
        result = ""
        for char in text:
            result += self.chrtrot(char)
        return result

    def convert_to_string(self, rot_text):
        ''' converts a rot13 string to an alphabetic string '''
        result = ""
        for char in rot_text:
            result += self.rottchr(char)
        return result

    ########

    def check_for_words(self, data, url, strings, tag):
        for string in strings:
            # added ignore condition for false bytes when site is loaded
            if self.convert_to_rot(string.decode('utf8')) in data:
                self.message = (
                    "Warning: String \'%s\' was found on "
                    "website %s within the %s tag"
                    % (string, url, tag))
                self.status = 'alert alert-warning'
            else:
                self.message = (
                    "Good news: No keywords found on the "
                    "website %s within the %s tag"
                    % (url, tag))
                self.status = 'alert alert-success'

    def check_website_for_rot(self, url, strings, tag='body'):
        # get url response
        if not validate_url(url):
            self.message = ("Website %s doesn\'t exist" % url)
            return
        tag = validate_tag(tag)
        try:
            response = urllib2.urlopen(url)
        except URLError, e:
            self.message = (
                "Website %s doesn\'t exist, request returned %s " % (url, e))
            return
        if response.code == 200:
            tag_content = get_tag_content(
                response.read().decode('utf8', 'ignore'), tag)
            if tag_content:
                no_tag_content = strip_tags(tag_content)
                self.check_for_words(no_tag_content, url, strings, tag)
            else:
                self.message = (
                    "Couldn\'t determine the %s tag content of the website %s"
                    % (tag, url))
        else:
            self.message = ("Website %s couldn\'t be accessed" % url)


##################
# Helper methods #
##################

def validate_tag(tag):
    ''' Checks if tag submission is empty '''
    if tag == 'undefined':
        tag = 'body'
    return tag


def validate_url(url):
    ''' very simple url validator,
    cases like ips, localhost, etc. omitted '''
    url_regex = re.compile(r'^https?://')
    if url_regex.search(url):
            return True
    return False


def get_tag_content(data, tag='body'):
    ''' extracts the data between tags, default is the body tag '''
    try:
        return data[data.index('<'+tag):data.index('</' + tag + '>')]
    except IndexError:
        return None


def strip_tags(data):
    return re.compile(r'<.*?>').sub('', data)

##################
#    __main__    #
##################

if __name__ == "__main__":
    # execute only if run as a script via `python app/rotchecker.py
    #      --url='https://en.wikipedia.org/wiki/ROT13'
    #      --str='Jul qvq gur puvpxra pebff gur ebnq?'
    #      --num=13`
    #      --tag=table
    import argparse
    parser = argparse.ArgumentParser(
        description='PyROTChecker checks websites for rot messages')
    parser.add_argument(
        '-u', '--url', help='URL to check for given string',
        required=True)
    parser.add_argument(
        '-s', '--str', help='Given string to check the website for',
        required=False)
    parser.add_argument(
        '-t', '--tag', help='Search within given tag',
        default='body')
    parser.add_argument(
        '-n', '--num', help='Given ROT shift',
        default=13)

    args = parser.parse_args()
    cypher = ROTCypher(int(args.num))

    # validate url
    if validate_url(args.url):
        cypher.check_website_for_rot(
            args.url,
            [urllib2.unquote(args.str)],
            args.tag)
        print (cypher.message)
    else:
        print ("Given url %s is not valid" % args.url)
