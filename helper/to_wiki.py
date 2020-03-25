import re
import functools as ft

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
            if x.startswith("<thead"):
                continue
            elif x.startswith("</thead>"):
                yield ws.group() + "|---" * th_count + "|" + "\n"
                th_count = 0
            elif x.startswith("<th"):
                th_count += 1
                yield th.group(1) + "|"
            elif x.startswith("<tr"):
                yield ws.group() + "|"
            elif x.startswith("</tr>"):
                yield '\n'
            elif x.startswith("<td"):
                yield td.group(1) + "|"
            continue
        yield line

def normalize(md):
    '''Normalize anchors.'''
    def on_match(link):
        desc = link.group(1)
        old = link.group(2)
        href = (link.group(2)
                .lower()
                .replace('%20', '-')
                .replace(" ", "-")
                .replace("~", "")
                .replace(".", ""))
        old, new = f'[{desc}]({old})', f'[{desc}]({href})'
        print(old, new)
        return old, new

    replacers = set((on_match(x) for x in re.finditer(r'\[([^\]\[]*)\]\((#[^\)]*)\)', md)))
    return ft.reduce(lambda md, x: md.replace(x[0], x[1]), replacers, md)

def main():
    
    with open("./index.md") as f:
        md = ''.join(decoder(f.readlines()))

    md = re.sub("# Table of Contents[\s\S]*# Overview", "# Modding", md)
    md = normalize(md)
    
    out = md
    print(len(out))
    with open('../wiki/docs/modding.md', 'w') as f:
        print(out, file=f)

if __name__ == '__main__':
    main()
