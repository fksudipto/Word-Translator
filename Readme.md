# Translate English words from DEEpL and download in Excel


## How to run

**Step 1 : Install Firefox**

**Step 2: Install requirements**

```shell
pip install -r requirements.txt
```

**Step 3: Run translator**

```shell
python main.py --language=de --words=apple,orange,banana,mango,strawberry # Get language identifer from the list below
```

You'll get the translated excel file downloaded in the project root folder.

## Limitations

1. Search translations only in DeepL
2. Can only translate from English to other languages
3. Only supports these languages:

```shell
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
```

