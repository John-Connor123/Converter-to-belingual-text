import googletrans
from googletrans import Translator
import main


def languages_list():
    dict_inverse = {value: key for key, value in googletrans.LANGUAGES.items()}
    return dict_inverse.keys()


def get_prepared_sentences(lst_sentences):
    input_to_translate_text = []
    max_count_chars = 2500
    abs_index = 0
    while abs_index < len(lst_sentences):
        count = 0
        move_index = 0
        path_of_input = ''
        while count < max_count_chars and move_index < len(lst_sentences):
            sum_indexes = abs_index + move_index
            if sum_indexes < len(lst_sentences) and count + len(lst_sentences[sum_indexes]) < max_count_chars:
                count += len(lst_sentences[sum_indexes])
                move_index += 1
                path_of_input += lst_sentences[sum_indexes]
            else:
                input_to_translate_text.append(path_of_input)
                break
        abs_index += move_index
    return input_to_translate_text


def get_translated_sentences(prepared_sentences, start_lang, end_lang):
    translator = Translator()
    output_sentences = []
    for elem in prepared_sentences:
        res = translator.translate(elem, src=start_lang, dest=end_lang).text
        output_sentences += main.get_sentences(res)
    return output_sentences


def do_translate(lst_sentences, start_lang, end_lang):
    input_to_translate_text = get_prepared_sentences(lst_sentences)
    output_sentences = get_translated_sentences(input_to_translate_text, start_lang, end_lang)
    return output_sentences


# print(do_translate(lst_sentences, 'english', 'russian'))
if __name__ == '__main__':
    with open("input.txt", encoding='utf-8') as f:
        lst_sentences = main.get_sentences(f.read())
        translate = do_translate(lst_sentences, start_lang='english', end_lang='russian')
        d = {1: [1,1], 2: [2,2], 3: [3,3]}
        for i in zip(*d.values()):
            print(i)