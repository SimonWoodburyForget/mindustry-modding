import re
from bs4 import BeautifulSoup
from enum import Enum, auto

def decoder(it):
    '''Fixes some org mode markdown export.'''
    mode = 'normal'
    th_count = 0
    for line in it:
        x = line.strip()
        ws = re.match(r' *', line)
        th = re.match(r'<th.*>(.*)<\/th>', x)
        td = re.match(r'<td.*>(.*)<\/td>', x)
        
        if re.match(r'\s*<a id="(?!").*"><\/a>\s*', x):
            continue
        if x.startswith("<table"):
            mode = 'table'
            continue
        if x.startswith("</table>"):
            mode = 'normal'
            continue
        if any(x.startswith(y) for y in ['<col', '</col']):
            continue
        if mode == 'table':
            # yield table until outside of table
            if any(x.startswith(y) for y in
                   ["<tbody", "</tbody"]):
                continue
            if x.startswith("<thead"):
                continue
            if x.startswith("</thead>"):
                yield "|---" * th_count + "|" + "\n"
                th_count = 0
                continue 
            if x.startswith("<th"):
                th_count += 1
                yield ws.group() + th.group(1) + "|"
                continue
            if x.startswith("<tr"):
                yield "|"
                continue
            if x.startswith("</tr>"):
                yield '\n'
                continue
            if x.startswith("<td"):
                yield ws.group() + td.group(1) + "|"
                continue
            if line == '\n':
                yield ""
                continue
        yield line

def main():
    with open("./index.md") as f:
        md = ''.join(decoder(f.readlines()))

    out = md
    print(len(out))
    with open('../wiki/docs/modding.md', 'w') as f:
        print(out, file=f)
        
main()
