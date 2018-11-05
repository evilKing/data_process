import requests
import json

class Baidu_Translator(object):

    def __init__(self):
        self.url = r"http://fanyi.baidu.com/basetrans"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",
        }
        self.count = 0

    def translate(self, raw_word):
        data = dict()
        data['query'] = raw_word
        data['from'] = 'en'
        data['to'] = 'zh'
        try:
            print(self.count, '当前的 count')
            if self.count > 1:
                self.count = 0
                return ''
            response = requests.post(url=self.url, headers=self.headers, data=data, timeout=1)
        except requests.exceptions.ReadTimeout:
            print('read time out')
            self.count += 1
            return self.translate(raw_word)

        except requests.exceptions.ConnectionError:
            print('connection error')
            self.count += 1
            return self.translate(raw_word)

        self.count = 0
        if response.text is None:
            return ''
        return json.loads(response.text)['trans'][0]['dst']

baidu_corr = Baidu_Translator()

if __name__ == '__main__':
    translated_word = baidu_corr.translate('developer')
    print(translated_word)
