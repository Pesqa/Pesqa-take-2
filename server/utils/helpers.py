import re
import time
import datetime

def file_url(category):
    
    def create_filename(instance, filename):
        r = re.compile(r'[^\S]')
        filename = r.sub('', filename)
        now = datetime.datetime.now()
        timestamp = int(time.time())
        
        return 'uploads/{0}/{1.year:04}/{1.month:02}/{1.day:02}/{2}/{3}'.format(
            normalize(category), now, timestamp filename)
        )
        
    return create_filename

def normalize(string):
    return slugify(string).replace('-', '_')