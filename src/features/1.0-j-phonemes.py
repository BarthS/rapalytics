__author__ = 'Jan Lubatschowski'

from pycorenlp import StanfordCoreNLP
import codecs, nltk, re, requests

################ Remember to have the Stanford CoreNLP server running
## Run the following in C:\Users\Jan\stanford-corenlp-full-2015-12-09
## java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
def main():
    # Read file, regex out anomalies, split into lines
    with codecs.open('../../data/raw/battle-cry-army-of-the-pharaohs.txt', 'rb', encoding='utf-8', errors='ignore') as f:
        lyrics = re.sub('[^a-zA-Z0-9\n\'\[\]]', ' ', f.read()).lower()
    lines = [l for l in lyrics.split('\n') if (len(l) > 0 and l[0] != '[')]
    #print(lines)

    # Tokenize using Stanford CoreNLP
    nlp = StanfordCoreNLP('http://localhost:9000')
    tokens = []
    for line in lines:
        output = nlp.annotate(line, properties={
            'annotators': 'tokenize, ssplit', \
            'outputFormat': 'json' \
        })
        tokens.append([t['word'] for s in output['sentences'] for t in s['tokens']])
    print(tokens)

    # Create arpabet using CMU dictionary
    arpabet = nltk.corpus.cmudict.dict()
    base_url = 'http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run'
    # This is for all the special cases, a.k.a. words not found in the cmu dict
    # Doesn't currently work
    file = {'corpus':
                ('words.txt', " ".join([t for line in tokens for t in line if t not in arpabet.keys()]))}
    res = requests.post(base_url, \
                        data={'formtype': 'simple'}, \
                        files=file, allow_redirects=True)
    dict_re = re.compile(r"\d+\.dic")
    print(res.text)
    #dict_path = dict_re.search(res.text).group(0)
    #res = requests.get(res.url + dict_path)

    # Get phonemes of words that are in the cmu dict
    #custom_dict = {line.split('\t')[0].lower(): line.split('\t')[1].split(' ') for line in res.text.split('\n') if
    #               len(line) > 1}

    def get_phonemes(word):
        try:
            return arpabet[word][0]
        except:
            try:
                return custom_dict[word]
            except:
                print(word)
                return word

    phonemes = [[get_phonemes(t) for t in line] for line in tokens]



if __name__ == '__main__':
    main()