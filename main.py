import os
import sys
import docx
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium import webdriver

from docx import Document
from docx.shared import Inches
import time
import script_epub
import script_fb2


def time_delay(func):
    def wrapper(*args, **kwargs):
        t_start = time.time()
        res = func(*args, **kwargs)
        t_end = time.time()
        delay = round(t_end - t_start, 2)
        return res, delay
    return wrapper


def protect_open(file_name):
    lst_replace = ['0x', '\x0c']
    with open(file_name, encoding='utf-8') as file:
        row_text = file.read()
        for elem in lst_replace:
            if row_text.count(elem) >= 1:
                row_text = row_text.replace(elem, '')
    return row_text


def get_text():
    while True:
        """Return str-variable with text and name of input file"""
        # name = input("Write name of your file with a extension(for example: Harry_Potter.txt): ")
        name1 = "dushi.fb2"
        name2 = r"voina-i-mir.epub"
        name = r"input_copy.txt"
        name4 = r"input.txt"
        if "." not in name:
            print("Please write file name with it extension(with '.txt', '.epub' or '.fb2')\n\n")
            continue
        name, ext = name.split('.')
        if ext == 'epub':
            script_epub.make_convert_epub_to_txt(name)
        elif ext == 'fb2':
            script_fb2.make_convert_fb2_to_txt(name)
        elif ext == 'txt':
            pass
        else:
            print("My program can't working with this file types...\n\n")
            continue

        try:
            row_text = protect_open(name + '.txt')
        except FileNotFoundError:
            print("File not found in directory where program is...\n\n")
            continue
        break
    return row_text, name


@time_delay
def parse_website_text(i):
    xpath_input_text = "/html/body/div[1]/div[2]/div/div/div/main/div[2]/form/div/div[1]/div/div/textarea"
    xpath_input_button = "/html/body/div[1]/div[2]/div/div/div/main/div[2]/form/div/div[1]/div/div/div/input"
    xpath_output_text = "/html/body/div[1]/div[2]/div/div/div/main/div[6]"
    browser = webdriver.Chrome()
    browser.get("https://tophonetics.com")
    if i == count:
        browser.find_element(by=By.XPATH, value=xpath_input_text).send_keys(row_text[5000*(i-1):])
    else:
        browser.find_element(by=By.XPATH, value=xpath_input_text).send_keys(row_text[5000*(i-1):5000*i])
    browser.find_element(by=By.XPATH, value=xpath_input_button).click()
    website_text = browser.find_element(by=By.XPATH, value=xpath_output_text).text
    browser.close()

    return website_text


def get_row_website_text():
    global count
    website_text = ''
    count = (len(row_text) // 5000) + 1
    for i in range(1, count+1):
        # website_text += parse_website_text(i)
        f = parse_website_text(i)
        website_text += f[0]
        delay = f[1]
        print(i, delay)

    with open("Row_transcribed_text_from_website.txt", 'w', encoding='utf-8') as file:
        file.write(website_text)

    del website_text

#кастомная замена в txt
def do_replace(row_text):
    dict_with_replaces = {
        'ɛ': 'e', 'i(:)': 'i', 'i:': 'i', 'i': 'ɪi',
        'u(ː)': 'ʊu', 'uː': 'ʊu', 'ɔː': 'oː', 'ɒ': 'ɔ',
        'aʊ': 'æʊ', 'aɪ': 'ɑɪ', '(ə)': '', 'tj': 'ʧ', 'dj': 'ʤ',
        'tʃ': 'ʧ', 'dʒ': 'ʤ', '.': ' .', ',': ' ,', ':': ' :',
        ';': ' ;', '!': ' !', '?': ' ?', 'r ': ' ', 'r': 'ɻ', ' ': '  '}

    for before, after in dict_with_replaces.items():
        # print(f"before[{before}] = {row_text}")
        row_text = row_text.replace(before, after)
        # print(f"after[{before}] = {row_text}\n")
    return row_text


def get_sentences(text):
    indexes = [-1]
    for symb_ind in range(len(text)):
        if text[symb_ind] in ".!?":
            indexes.append(symb_ind)

    sentences = []
    for position in range(len(indexes) - 1):

        sentence = text[indexes[position] + 1: indexes[position + 1] + 1]
        while '\n' in sentence:
            sentence = sentence.replace('\n', '')
        sentences.append(sentence.strip()+'\n')

    return sentences


print("""              Description:
 This program make a Bilingual text from English text and it doesn't need a transcription.
Just put your file to a directory where program is. My program do all other work.

 Program works with txt, epub, fb2 formats. 
But if your file has a fb2 format you should choose your file in the folder window which will open later.

 Output file has a name 'Bilingual_(input file name).docx'. 
Other files are temp. You can delete its if you don't need its.

                Work_details:
 What does program do? Find your file in directory where is this program and
use "chromedriver" to open Google for opening web-site "https://tophonetics.com" and translate your file there.
(Works only with Google browser)
Translate speed is about 250 symbols at 1 second.
P.s. If web-site doesn't loading please run program later 
because there are rare situations when web-site doesn't available. 
 Contacts: ivan.eudokimoff2014@gmail.com

Thanks for using my program:)\n\n""")


row_text, name = get_text()
print("\nFile was opened successful!\n")

while True:
    try:
        get_row_website_text()
        print("\nProgram got a transcription.\n")
        break
    except:
        print("Error: please put the file 'chromedriver' in a directory where program is and rerun this program.")
        time.sleep(5)
        sys.exit()


document = Document()
document.styles['Normal'].font.name = "Cambria"
document.styles['Normal'].font.size = docx.shared.Pt(16)

row_transcribed_text = protect_open('row_transcribed_text_from_website.txt')
row_transcribed_text = do_replace(row_transcribed_text)

sentences_transcribed_text = get_sentences(row_transcribed_text)
sentences_text = get_sentences(row_text)

for i in range(len(sentences_transcribed_text)):
    word_element = str(i+1) + '\n' + sentences_text[i] + sentences_transcribed_text[i] + '\n'
    document.add_paragraph(word_element)


document.save(f"Bilingual_{name}.docx")
print(f"\nBilingual has created! It name: Bilingual_{name}.docx\nProgram will close after 5 seconds")
time.sleep(5)