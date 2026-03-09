def xss_filter_tag(str):
    if str == '':
        return ""
    
    str = str.lower()
    str = str.replace("&", "&amp")
    str = str.replace("%00", "null")
    str = str.replace("%", "&#37")
    str = str.replace("../", "")
    str = str.replace("..\\\\", "")
    str = str.replace("./", "")
    str = str.replace("<script", "&gtscript")
    str = str.replace("</script", "&gt/script")
    str = str.replace("<object", "&gtobject")
    str = str.replace("</object", "&gt/object")
    str = str.replace("<applet", "&gtapplet")
    str = str.replace("</applet", "&gt/applet")
    str = str.replace("<embed", "&gtembed")
    str = str.replace("</embed", "&gt/embed")
    str = str.replace("<form", "&gtform")
    str = str.replace("</form", "&gt/form")
    str = str.replace("<img", "&gtimg")
    str = str.replace("</img", "&gt/img")
    str = str.replace("<svg", "&gtsvg")
    str = str.replace("</svg", "&gt/svg")
    str = str.replace("<xml", "&gtxml")
    str = str.replace("</xml", "&gt/xml")
    str = str.replace("<video", "&gtvideo")
    str = str.replace("</video", "&gt/video")
    str = str.replace("<iframe", "&gtiframe")
    str = str.replace("</iframe", "&gt/iframe")
    return str


def xss_filter_keyword(str):

    clean = ''

    if '.' in str:
        splits = str.split('.')
        stripped = [part.strip() for part in splits]
        str = '.'.join(stripped)

    deny_list = [
    "onanimationiteration",
    "onanimationstart",
    "onanimationedn",
    "ontransition",
    "onmouseover",
    "onscrollend",
    "javascript",
    "onsubmit",
    "onselect",
    "onchange",
    "onclick",
    "onerror",
    "onfocus",
    "onload",
    "onblur",
    "location",
    ".history",
    ".cookie",
    ".href",
    ".open",
    "console.log(",
    "replace(",
    "alert(",
    "eval(",
    "fetch(",
    "[",
    "]",
    "`"
    ]

    for k in deny_list:
        if k in str:
            print("Blacklist:", k)
            clean = 'filter!!'

    if clean == '':
        clean = str

    return clean