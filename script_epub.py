import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        output += '{} '.format(t)
    return output


def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output


def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext


def make_convert_epub_to_txt(path_epub):
    out = epub2text(path_epub)
    path_of_name = path_epub.split('.')[0]
    to_delete = [r"xml version='1.0' encoding='utf-8'?", "html", r'0x93']
    for i in range(len(out)):
        for elem in to_delete:
            if elem in out[i]:
                out[i] = out[i].replace(elem, '')
    with open(f'{path_of_name}.txt', 'w', encoding='utf-8') as file:
        file.write("".join(out))
