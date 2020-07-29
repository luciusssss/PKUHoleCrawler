import os



def parseHTML(data):
    """
    Every pair of tags are on the same column,
    subtags have deeper step-in, which uses `\\t`,
    """
    TAG_BEGIN = 1
    TAG_END = 2
    TAG_SINGLE_LINE = 3

    def top(stack):
        return stack[-1]

    def tag_type(line):
        isTag = (line.find('<') == 0)
        isTagEnd = (line.find('</') == 0)
        isTagBegin = (isTag and not isTagEnd)
        isSingleLine = (line.find('/>') != -1 or line.find('</') > 0)
        topWord = ""
        r = line.find('>')
        rs = line.find(' ')
        if isTagEnd:
            topWord = line[2:min(r, rs)]
        elif isTagBegin:
            topWord = line[1:min(r, rs)]

        if topWord in ['link', 'meta']:
            return topWord, TAG_SINGLE_LINE
        elif isSingleLine:
            return "", TAG_SINGLE_LINE
        elif isTagBegin:
            return topWord, TAG_BEGIN
        elif isTagEnd:
            return topWord, TAG_END
        else:
            return "", TAG_SINGLE_LINE

    stack = []
    out = ""
    lst = data.replace("><", ">\n<").split('\n')
    if lst[0].find("<!doctype") != -1:
        out += lst[0] + '\n' # <!doctype html>
    for line in lst[1:]:
        if line != "":
            topWord, tag = tag_type(line)
            if tag == TAG_BEGIN:
                out += len(stack)*'\t' + line + '\n'
                stack.append(topWord)
            elif tag == TAG_END:
                stack.pop()
                out += len(stack)*'\t' + line + '\n'
            else:
                out += len(stack)*'\t' + line + '\n'

    return out

def writeHTMLFile(file, data):
    parsed = parseHTML(data)
    with open(file, 'w') as f:
        f.write(parsed)

if __name__ == "__main__":
    data = r'<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><link rel="icon" href="./static/favicon/256.png"><meta name="format-detection" content="telephone=no"><link rel="stylesheet" href="./static/fonts_7/icomoon.css"/><meta name="mobile-web-app-capable" content="yes"><link rel="shortcut icon" href="./static/favicon/256.png"><link rel="manifest" href="./static/manifest.json"><meta name="theme-color" content="#333333"/><meta name="apple-mobile-web-app-capable" content="yes"><link rel="apple-touch-icon" sizes="180x180" href="./static/favicon/180.png"/><link rel="apple-touch-icon" sizes="256x256" href="./static/favicon/256.png"/><meta name="apple-mobile-web-app-status-bar-style" content="default"><meta name="apple-mobile-web-app-title" content="\xe6\xa0\x91\xe6\xb4\x9e"><link rel="apple-touch-startup-image" href="./static/splash/750x1334.png" media="(device-width: 375px) and (-webkit-device-pixel-ratio: 2)"/><link rel="apple-touch-startup-image" href="./static/splash/1242x2208.png" media="(device-width: 414px) and (-webkit-device-pixel-ratio: 3)"/><link rel="apple-touch-startup-image" href="./static/splash/1668x2388.png" media="(device-width: 834px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)"/><link rel="apple-touch-startup-image" href="./static/splash/2388x1668.png" media="(device-width: 834px) and (-webkit-device-pixel-ratio: 2) and (orientation: landscape)"/><title>P\xe5\xa4\xa7\xe6\xa0\x91\xe6\xb4\x9e</title><link href="./static/css/main.a3e91d9e.chunk.css" rel="stylesheet"></head><body><div id="root"></div><script src="stats.js" defer="defer"></script><script src="./static/js/runtime~main.47dca567.js"></script><script src="./static/js/2.00494b3c.chunk.js"></script><script src="./static/js/main.369915c9.chunk.js"></script></body></html>'
    writeHTMLFile('items/index.html', data)