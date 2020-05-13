# coding=utf-8
from googletrans import Translator


def main():
    translator = Translator()
    while(True):
        print('************************************************************')
        text = input('Input the sentence that will be translated: ')
        if text == 'quit':
            return None
        if not text: 
            continue
        result = translator.translate(text, dest='zh-CN')
        extra_data = result.extra_data
        print("translated result: ", result.text)
        if not extra_data['all-translations']:
            continue
        for v in extra_data['all-translations']:
            print('词性: {}'.format(v[0]))
            print('All-Trans: {}'.format(v[1]))
            for i in range(len(v[1])):
                print('No.{0}: {1:{3}<6} Synonyms: {2}'.format(
                    i, v[2][i][0].strip('!'), v[2][i][1][:3], chr(12288)))

if __name__ == '__main__':
    main()

