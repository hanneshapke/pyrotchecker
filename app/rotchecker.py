import re
import urllib2


class ROTCypher:
    ''' ... '''

    def __init__(self, rot_shift=13):
        self.alpha, self.rot = self.get_rot_sets(rot_shift)

    def get_rot_sets(self, num_char_diff):
        ''' Create char and rot strings for the conversion, default: 13 '''
        uppercase_set = ''.join(chr(ord('A') + i) for i in xrange(26))
        lowercase_set = ''.join(chr(ord('a') + i) for i in xrange(26))
        uppercase_rot = ''.join(
            [uppercase_set[num_char_diff:], uppercase_set[:num_char_diff]])
        lowercase_rot = ''.join(
            [lowercase_set[num_char_diff:], lowercase_set[:num_char_diff]])
        return (uppercase_set + lowercase_set, uppercase_rot + lowercase_rot)

    def checkcharacter_error(self, char):
        ''' Raise ValueError if char is longer than one character '''
        if len(char) > 1:
            raise ValueError('Only converts single char or rot13 characters')

    def chrtrot(self, char):
        ''' Convert single alphabet character to rot13 '''
        self.checkcharacter_error(char)
        if re.match('^[\w-]+$', char):
            return self.rot[self.alpha.index(char)]  # also find
        return char

    def rottchr(self, char):
        ''' Convert single rot13 character to alphabet character '''
        self.checkcharacter_error(char)
        if re.match('^[\w-]+$', char):
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

    def validate_url(self, url):
        ''' very simple url validator,
        cases like ips, localhost, etc. omitted '''
        url_regex = re.compile(r'^https?://')
        if url_regex.search(url):
                return True
        return False

    def get_body_content(self, data):
        try:
            return data[data.index('<body'):data.index('</body>')]
        except IndexError:
            return None

    def strip_tags(self, data):
        return re.compile(r'<.*?>').sub('', data)

    def check_for_words(self, data, url, strings):
        for string in strings:
            if self.convert_to_rot(string) in data:
                print (
                    "String \'%s\' was found in website %s" % (string, url))
            else:
                print (
                    "No match found for the strings/kewords on the website %s"
                    % url)

    def check_website_for_rot(self, url, strings):
        # validate url
        if not self.validate_url(url):
            return ("Given url %s is not valid" % url)
        # get url response
        response = urllib2.urlopen(url)
        if response.code == 200:
            body_content = self.get_body_content(response.read())
            if body_content:
                no_tag_content = self.strip_tags(body_content)
                self.check_for_words(no_tag_content, url, strings)
            else:
                return (
                    "Couldn\'t determine the body content of the website %s"
                    % url)
        else:
            return ("Website %s couldn\'t be accessed" % url)

if __name__ == "__main__":
    # execute only if run as a script via `python app/rotchecker.py
    #      --url='https://en.wikipedia.org/wiki/ROT13'
    #      --str='Jul qvq gur puvpxra pebff gur ebnq?'
    #      --num=13`
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
        '-n', '--num', help='Given ROT shift',
        default=13)
    args = parser.parse_args()
    cypher = ROTCypher(int(args.num))
    print (cypher.check_website_for_rot(args.url, [args.str]))
