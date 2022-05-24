# set_word_view  if end_lang is not None:  protect_open заменить name на полный путь до файла
import docx
import os
import sys
import time

from docx import Document
from docx.shared import Inches
from selenium import webdriver
from selenium.webdriver.common.by import By

import script_epub
import script_fb2
import Google_translater
global name


def create_directory_with_temp_files():
    try:
        os.mkdir("Temp_files")
    except FileExistsError:
        pass
    except:
        print("Please run the program as administrator.")
        time.sleep(5)
        sys.exit()


def time_delay(func):
    def wrapper(*args, **kwargs):
        t_start = time.time()
        res = func(*args, **kwargs)
        t_end = time.time()
        delay = round(t_end - t_start, 2)
        print(delay)
        return res

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
        """Returns str-variable with the text and name of the input file"""
        name_with_ext = input("Write the name of your file (for example: Harry_Potter.txt): ")
        name_with_ext1 = "dushi.fb2"
        name_with_ext2 = r"voina-i-mir.epub"
        name_with_ext3 = r"input_copy.txt"
        name_with_ext4 = r"input.txt"
        #name = easygui.fileopenbox().split('\\')[-1]
        if "." not in name_with_ext:
            print("Please write file name with its extension (with '.txt', '.epub', or '.fb2')\n\n")
            continue
        name, ext = name_with_ext.split('.')
        if ext == 'epub':
            script_epub.make_convert_epub_to_txt(name_with_ext)
        elif ext == 'fb2':
            script_fb2.make_convert_fb2_to_txt(name)
        elif ext == 'txt':
            pass
        else:
            print("My program can't work with this file type...\n\n")
            continue

        try:
            row_text = protect_open(name + '.txt')
        except FileNotFoundError:
            print("The file wasn't found in the same directory where the program is...\n\n")
            continue
        break
    return row_text, name


def parse_website_text(i):
    xpath_input_text = "/html/body/div[1]/div[2]/div/div/div/main/div[2]/form/div/div[1]/div/div/textarea"
    xpath_input_button = "/html/body/div[1]/div[2]/div/div/div/main/div[2]/form/div/div[1]/div/div/div/input"
    xpath_output_text = "/html/body/div[1]/div[2]/div/div/div/main/div[6]"
    browser = webdriver.Chrome()
    browser.get("https://tophonetics.com")
    if i == count:
        browser.find_element(by=By.XPATH, value=xpath_input_text).send_keys(row_text[5000 * (i - 1):])
    else:
        browser.find_element(by=By.XPATH, value=xpath_input_text).send_keys(row_text[5000 * (i - 1):5000 * i])
    browser.find_element(by=By.XPATH, value=xpath_input_button).click()
    website_text = browser.find_element(by=By.XPATH, value=xpath_output_text).text
    browser.close()

    return website_text


def get_row_website_text():
    global count
    website_text = ''
    count = (len(row_text) // 5000) + 1
    for i in range(1, count + 1):
        website_text += parse_website_text(i)

    website_text = do_replace(website_text)
    with open(r"Temp_files\Transcribed_text_from_website.txt", 'w', encoding='utf-8') as file:
        file.write(website_text)

    del website_text


def set_new_dict_with_replaces():
    try:
        with open(r"Temp_files\Transcription_replaces.txt", 'r', encoding='utf-8') as f:
            f_in = f.read()
            temp = f_in.replace('{', '').replace('}', '')

            prepared, indx_array = [], [-1]
            for indx in range(len(temp)):
                if temp[indx] == ',' and temp[indx + 1] != "'":
                    indx_array.append(indx)
            indx_array.append(len(temp))

            for i in range(len(indx_array) - 1):
                prepared.append(temp[indx_array[i] + 1: indx_array[i + 1]].strip())

            new_replaces_dict = {}
            for pair in prepared:
                pair = pair
                ind = 0
                while True:
                    check = pair.find(':', ind)
                    if pair[check + 1] not in ")'":
                        ind = check
                        break
                    ind = check + 1

                key = pair[:check].strip().replace("'", '')
                value = pair[check + 1:].strip().replace("'", '')
                new_replaces_dict[key] = value
    except FileNotFoundError:
        print("\nYou haven't file with special replaces.")
        print("First launch sets basic replaces and adds its at 'Transcription_replaces.txt' in Temp_file directory")
        print("You can change symbols in ' ' in Transcription_replaces.txt before next launch.")
        time.sleep(7)
        return None
    return new_replaces_dict


def do_replace(row_text):
    dict_with_replaces = {
        'ɛ': 'e', 'i(ː)': 'i', 'i:': 'i', 'i': 'ɪi',
        'u(ː)': 'ʊu', 'uː': 'ʊu', 'ɔː': 'oː', 'ɒ': 'ɔ',
        'aʊ': 'æʊ', 'aɪ': 'ɑɪ', '(ə)': '', 'tj': 'ʧ', 'dj': 'ʤ',
        'tʃ': 'ʧ', 'dʒ': 'ʤ', '.': ' .', ',': ' ,', ':': ' :',
        ';': ' ;', '!': ' !', '?': ' ?', 'r ': ' ', 'r': 'ɻ', ' ': '  '}

    while True:
        set_replace = input("Do you want to set symbol replacements? (Yes/No): ").lower().strip()
        if set_replace not in ['yes', 'no']:
            print("Please write 'yes' or 'no'.\n")
        else:
            break

    if set_replace:
        new_replaces = set_new_dict_with_replaces()
        if new_replaces is not None:
            dict_with_replaces = new_replaces
        else:
            with open(r"Temp_files\Transcription_replaces.txt", 'w', encoding='utf-8') as file:
                file.write(str(dict_with_replaces))

    for before, after in dict_with_replaces.items():
        row_text = row_text.replace(before, after)
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
        sentences.append(sentence.strip() + '\n')

    return sentences


def set_word_view(start_lang, end_lang=None, flag_transcription='yes'):
    if flag_transcription == 'yes':
        print("The program has started make a transcription...")
        get_transcription()
        transcription_sentences = get_sentences(protect_open(r"Temp_files\Transcribed_text_from_website.txt"))
    else:
        transcription_sentences = ''

    if end_lang is not None:
        input_sentences = get_sentences(protect_open(name+'.txt'))
        print("The program has started make a translate...")
        translated_sentences = Google_translater.do_translate(input_sentences, start_lang=start_lang, end_lang=end_lang)
# french, transcribed, english
    while True:
        try:
            order = input(f"\nChange sentence order in the bilingual text (for example: '{start_lang}, {end_lang}, transcribed'): ").strip().lower()
            if order[-1] == '.':
                order = order[:len(order)-1]
            if order.find(',') == -1:
                raise
            order = order.split(',')
            for i in range(len(order)):
                order[i] = order[i].strip()
            if set(order) <= set(Google_translater.languages_list()):
                print("You might have made a mistake in your language list.")
                print("Please pay attention to the input format and to which languages you need.\n")
                continue
            # print(set(order))
            # print(set(Google_translater.languages_list())
            break
        except:
            print("You might have made a mistake in your language list.")
            print("Please pay attention to the input format and to which languages you need.\n")

    compare_dict = {start_lang: input_sentences, end_lang: translated_sentences, 'transcribed': transcription_sentences}
    if flag_transcription == 'no':
        del compare_dict['transcribed']
    if flag_transcription == 'no':
        del compare_dict['transcribed']
    order_dict = {}
    if len(compare_dict) == 1:
        print("You chose no language and no transcription. It makes no sense.")
        print("Please restart the program and write a correct data.")
        time.sleep(5)
        sys.exit()
    for elem in order:
        order_dict[elem] = compare_dict[elem]
    return zip(*order_dict.values())


def create_word_file(zip_sentences):
    document = Document()
    document.styles['Normal'].font.name = "Cambria"
    document.styles['Normal'].font.size = docx.shared.Pt(16)

    count = 1
    for pack in zip_sentences:
        word_element = str(count) + '\n'
        count += 1
        for i in range(len(pack)):
             word_element += pack[i]
        word_element += '\n'
        document.add_paragraph(word_element)

    document.save(f"Bilingual_{name}.docx")


def get_language(first_lang=True):
    if first_lang:
        script_sentence = "Write the language of your input file: "
    else:
        script_sentence = "Write the language you want it to be translated into: "
    while True:
        language = input(script_sentence).lower().strip()
        if language == 'all':
            print('All available languages:')
            for lang in Google_translater.languages_list():
                print(lang)
            print()
        elif language not in Google_translater.languages_list():
            print(f"We can't translate from {language} or this language name contains a mistake.")
            print("If you want to see all the available languages, write 'all'\n")
        else:
            break
    return language


def get_transcription():
    while True:
        try:
            get_row_website_text()
            print("\nThe program has got the transcription.\n")
            break
        except:
            print("Error: please put the file 'chromedriver' in the same directory where the program is and restart the program.")
            time.sleep(5)
            sys.exit()


if __name__ == '__main__':
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
    print("The file was opened successfully.\n")

    start_lang = get_language(first_lang=True)
    while True:
        flag_another_translate = input("Do you want to add another translate?(Yes/No): ").lower().strip()
        if flag_another_translate not in ['yes', 'no']:
            print("Please write 'Yes' or 'no'\n")
            continue
        elif flag_another_translate == 'yes':
            end_lang = get_language(first_lang=False)
        elif flag_another_translate == 'no':
            end_lang = None

        flag_transcription = input("Do you want to add transcription(IPA vowel chart) in English?(Yes/No): ").lower().strip()
        if flag_another_translate not in ['yes', 'no']:
            print("Please write 'Yes' or 'no'\n")
            continue
        break

    create_directory_with_temp_files()
    zip_sentences = set_word_view(start_lang, end_lang=end_lang, flag_transcription=flag_transcription)
    create_word_file(zip_sentences)

    flag = False
    try:
        with open(name + '.epub') as f:
            flag = True
    except:
        pass
    try:
        with open(name + '.fb2') as f:
            flag = True
    except:
        pass

    if flag:
        os.remove(fr"{os.getcwd()}\{name}.txt")

    print(f"\nYour bilingual file has been created! Its name is: Bilingual_{name}.docx")
    print("The program will be closed in 5 seconds.")
    time.sleep(5)
