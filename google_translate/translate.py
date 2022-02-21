# coding=utf-8
from googletrans import Translator
from httpcore import SyncHTTPProxy
import readline

class Completer:
    def __init__(self, words):
        self.words = words
        self.prefix = None

    def complete(self, prefix, index):
        if prefix != self.prefix:
            # we have a new prefix!
            # find all words that start with this prefix
            self.matching_words = [
                w for w in self.words if w.startswith(prefix)
            ]

        try:
            return self.matching_words[index]
        except IndexError:
            return None

def get_word_list(filename):
    word_list = []
    with open(filename, 'r') as fd:
        for line in fd:
            word_list.append(line.strip())
    return word_list

def main():
    word_list_filename = "/usr/share/dict/words"
    word_list = get_word_list(word_list_filename)

    completer = Completer(word_list)
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer.complete)

    service_urls = ['translate.google.com.hk']
    translator = Translator()
    try:
        while(True):
            text = input('\33[1;34m' + 'en->zh : \33[0m')
            if text == 'quit':
                return None
            if not text:
                continue
            try:
                result = translator.translate(text, dest='zh-cn')
            except AttributeError:
                print('Attribute Error')
                continue
            extra_data = result.extra_data
            print(f"translated result: {result.text}\t"
                  f"pronunciation: {extra_data['translation'][1][-1]}")
            if not extra_data['all-translations']:
                continue
            for v in extra_data['all-translations']:
                print('词性: {}'.format(v[0]))
                print('All-Trans: {}'.format(v[1]))
                try:
                    for i in range(len(v[1])):
                        print('No.{0}: {1:{3}<6} Synonyms: {2}'
                            .format(i, v[2][i][0].strip('!'),
                                    v[2][i][1][:3], chr(12288)))
                except IndexError:
                    print('Index Error')
                    continue
    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')

if __name__ == '__main__':
    main()
