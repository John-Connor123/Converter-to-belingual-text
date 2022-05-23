import time
from selenium.webdriver.common.by import By
from selenium import webdriver
import os


if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID


    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
            self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff


    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]


    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value


    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'


    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

def make_convert_fb2_to_txt(path_fb2):
    print("Преобразуем '.fb2' в '.txt'. Сейчас откроется окно сайта, делающего это. Выберите файл, который вы хотите превратить в белингву и просто ждите.")
    xpath_button_choose_file = "/html/body/div[4]/div[3]/div[1]/div/div/div/button"
    xpath_run_button = "/html/body/div[4]/div[5]/div[2]/div[1]/form/div[3]/button"
    browser = webdriver.Chrome()
    browser.get("https://document.online-convert.com/ru/convert/fb2-to-txt")
    browser.find_element(by=By.XPATH, value=xpath_button_choose_file).click()

    flag = False
    while not flag:
        try:
            browser.find_element(by=By.XPATH, value=xpath_run_button).click()
            time.sleep(2)
        except:
            pass

        try:
            with open(rf"{get_download_folder()}\{path_fb2.split('.')[0]}.txt", "r", encoding='utf-8') as file:
                flag = True
                browser.close()
        except:
            pass

    path_file_from_folder = rf"{get_download_folder()}\{path_fb2.split('.')[0]}.txt"
    with open(path_file_from_folder, "r", encoding='utf-8') as file:
        text = file.read()
    os.remove(path_file_from_folder)
    with open(rf"{os.getcwd()}\{path_fb2.split('.')[0]}.txt", 'w', encoding='utf-8') as file:
        file.write(text)