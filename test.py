# coding=utf-8
#

from lib.url.ershoufang import *
from lib.utility.writer import *

print get_qu_urls()
urls = get_sub_qu_urls()
print len(urls)

write_urls_to_file("sub_qu_urls.txt", urls)