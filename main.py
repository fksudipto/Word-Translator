import os
import random
import time
from typing import Optional

import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

WEBDRIVER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'geckodriver'
)

USER_AGENTS = {
    1: "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
    2: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 "
       "(KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    3: "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) "
       "Gecko/20100101 Firefox/33.0",
    4: "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    5: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    6: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 "
       "(KHTML, like Gecko) Version/7.1 Safari/537.85.10",
    7: "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    8: "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) "
       "Gecko/20100101 Firefox/33.0",
    9: "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
}

LANGUAGES = {
    'bg': 'Bulgarian',
    'zh': 'Chinese',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'el': 'Greek',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
}


def get_browser_agent(index: Optional[int] = None) -> str:
    """
    Gets browser agent value based on index.
    If index not provided returns a random agent value.
    :param index: The index of the user agent to be returned
    :return: Browser agent value
    """
    key = index if index else random.randint(1, len(USER_AGENTS))
    return USER_AGENTS[key]


def get_webdriver(user_agent: str):
    """
    Gets selenium webdriver instance
    :param user_agent: User agent string
    :return driver: Selenium webdriver instance
    """
    firefox_options = Options()
    firefox_options.add_argument("no-sandbox")
    firefox_options.add_argument("--disable-extensions")
    firefox_options.add_argument(f'user-agent={user_agent}')
    firefox_options.add_argument("--headless")
    driver_path = WEBDRIVER_PATH
    driver = webdriver.Firefox(
        executable_path=driver_path, options=firefox_options
    )
    return driver


def process(word: str) -> str:
    word = word.strip()
    word = word.lower()
    word = word.replace('.', '')
    word = word.replace(':', '')
    word = word.replace(',', '')
    return word


URL = 'https://www.deepl.com/en/translator#en/{}/{}'


def translate(language: str, words: list):
    browser_agent = get_browser_agent(5)
    print(browser_agent)
    firefox_driver = get_webdriver(browser_agent)
    workbook = xlsxwriter.Workbook('{}.xlsx'.format(LANGUAGES.get(language)))
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Word')
    worksheet.write(0, 1, 'Translation')
    row = 1

    for word in words:
        url = URL.format(language, word)
        firefox_driver.get(url)
        WebDriverWait(firefox_driver, 10).until(
            ec.presence_of_all_elements_located(
                (By.TAG_NAME, 'textarea'))
        )

        time.sleep(3)

        translation = []

        translation_ele = firefox_driver.find_element(
            By.XPATH,
            '//div[contains(@id, "target-dummydiv")]'
        )

        translation.append(
            process(translation_ele.get_attribute('innerHTML'))
        )

        alternative_translations_ele = firefox_driver.find_elements(
            By.XPATH,
            '//ul[@aria-labelledby="alternatives-heading"]/li[@class="lmt__translations_as_text__item"]/button'
        )

        for text in alternative_translations_ele:
            translation.append(process(text.get_attribute('innerHTML')))

        print(translation)

        worksheet.write(row, 0, word)
        worksheet.write(row, 1, ','.join(list(set(translation))))

        row += 1

    firefox_driver.close()
    workbook.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Translate english words')
    parser.add_argument('--language', metavar='path', required=True,
                        help='Select the language')
    parser.add_argument('--words', metavar='path', required=True,
                        help='select words')
    args = parser.parse_args()
    selected_language = args.language
    selected_words = args.words.split(',') if args.words else None
    translate(selected_language, selected_words)
