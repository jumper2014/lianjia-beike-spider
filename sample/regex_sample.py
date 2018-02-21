#!/usr/bin/env python
# coding=utf-8

import re
if __name__ == '__main__':
    text = '''<div class="page-box fr"><div class="page-box house-lst-page-box" comp-module="page" page-data='{"totalPage":3,"curPage":1}' page-url="/xiaoqu/caolu/pg{page}/"></div>
</div>
    '''
    res = re.search('.*"totalPage":(\d+),.*', text)
    print(res.group(1))