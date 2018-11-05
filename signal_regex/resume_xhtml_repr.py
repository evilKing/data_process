#coding: utf-8

import re
from HTMLParser import HTMLParser

class ResumeXHtmlRepr(object):
    td_pat = re.compile('<td.*?>(?P<vo>.*?)</td>', re.S)
    tr_pat = re.compile('<tr.*?>(?P<vo>.*?)</tr>', re.S)
    tag_pat = re.compile('<.+?>', re.S)               # html tag
    newline_pat = re.compile('(</p>|</h\d>|</tr>|</ul>|</div>|<br */?>)')      # <p> --换行
    no_newline_pat = re.compile('(</p>|</h\d>|</td>|</tr>|</ul>|</div>|<br */?>)$')
    
    strip_pat = re.compile('<t[dr] */>')
    script_pat = re.compile('<script.+?</script>', re.S)
    style_pat = re.compile('<style.+?</style>', re.S)
    span_pat = re.compile('</span>')
    
    html_parser = HTMLParser()
    
    def __init__(self):
        pass
    
    def _td_repl(self, mat):
        '''若<p>个数较少，最后的</p>不换行'''
        
        cont = mat.group('vo')
        cont = self.newline_pat.sub('\n', cont)
        cont = self.tag_pat.sub('', cont)
        
        if cont.count('\n') <= 2 and len(cont) < 20 :
            cont = cont.strip() + ' '
            cont = cont.replace('\n', ' ')
            
        # 处理包含在一个cell中的group name
        cont_rep = cont.replace('\n','').replace(' ', '')

        return cont
    
    def parse_cont_lines(self, lines):
        lines = map(self.html_parser.unescape, lines)
        
        lines = map(lambda x: x.strip(), lines)
        lines = map(lambda x: x if self.no_newline_pat.search(x) else x + u'\n', lines)
        
        cont = ''.join(lines).strip()
        start_p = cont.find(u'<body')
        start_p = start_p if start_p > 0 else 0
        if cont[start_p:].startswith(u'<body><p><html') :
            new_start_p = cont.find(u'<body', start_p+5)
            start_p = new_start_p if new_start_p > 0 else start_p
         
        end_p = cont.find(u'</body>')
        end_p = end_p if end_p > 0 else len(cont)
        cont = cont[start_p: end_p]
        
        cont = self.html_parser.unescape(cont)  # 处理&amp;amp;
            
        cont = self.script_pat.sub('', cont)        # 处理<body>中的<script>标签
        cont = self.style_pat.sub('', cont)         # 处理<body>中的<style>标签
        cont = self.strip_pat.sub('', cont)         # 处理<td/>,<tr/>
        cont = self.span_pat.sub(' ', cont)         # 替换为空格
        
        cont = self.td_pat.sub(self._td_repl, cont)
        cont = self.newline_pat.sub('\n', cont)
        cont = self.tag_pat.sub('', cont)
        
        lines = cont.split('\n')
        lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: x != '', lines)
        return lines

html_repr = ResumeXHtmlRepr()
    
if __name__ == '__main__' :
    txt = u'''
            </tr>
            <tr>    <td><p class="正文">2008.9 - 2010.7    就读于吉林大学软件学院，获得硕士学位</p>
            <p class="正文">2004.9 - 2008.7    就读于吉林大学软件学院，获得学士学位</p>
            </td></tr>
        '''
    lines = map(lambda x: x.strip(), txt.split(u'\n'))
    for line in html_repr.parse_cont_lines(lines) :
        print(line)

    
    