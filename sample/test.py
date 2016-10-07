# coding=utf-8
#

from lib.url.ershoufang import *
from lib.url.xiaoqu import *
from lib.utility.writer import *


urls = get_ershoufang_bankuai_urls()
print len(urls)
write_urls_to_file("ershoufang_bankuai_urls.txt", urls)

urls = get_xiaoqu_area_urls()
print len(urls)
write_urls_to_file("xiaoqu_bankuai_urls.txt", urls)