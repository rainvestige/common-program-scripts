# coding=utf-8
from googletrans import Translator
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

    translator = Translator()
    try:
        while(True):
            #print('{:*<80}'.format('*'))
            #text = input('Input the sentence that will be translated: ')
            text = input('en->zh : ')
            if text == 'quit':
                return None
            if not text: 
                continue
            result = translator.translate(text.replace('\n', ' '), dest='zh-CN')
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
    except (EOFError, KeyboardInterrupt) as e:
        print('\nShutting down...')

if __name__ == '__main__':
    main()

