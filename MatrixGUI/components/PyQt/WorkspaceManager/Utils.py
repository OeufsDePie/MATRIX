import string
import unicodedata
import re                 # regular expressions

class Utils:
    """ Useful functions.
    """

    @staticmethod
    def valid_name(s):
        """ Transform a string in order to get a valid filename

        This method may produce invalid filenames such as "."
        """
        # the authorized characters
        valid_chars = "-_.()/ %s%s" % (string.ascii_letters, string.digits)
        # tranform to authorized characters
        valid_string = ''.join(c for c in unicodedata.normalize('NFKD',s) if c in valid_chars)
        # remove spaces at the extremities
        valid_string = valid_string.strip()
        # replace spaces by underscores
        valid_string  = valid_string.replace(" ","_")
        # remove multiple spaces and others
        valid_string = re.sub('\.+','\.',valid_string)
        valid_string = re.sub('-+','-',valid_string)
        valid_string = re.sub('_+','_',valid_string)
        return valid_string
