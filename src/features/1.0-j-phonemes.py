__author__ = 'Jan Lubatschowski'

from pycorenlp import StanfordCoreNLP
import codecs, nltk, re, requests

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
    # @Bart, add the code from your notebook, there's a big chunk that's missing
    #base_url = 'http://www.speech.cs.cmu.edu/cgi-bin/tools/lmtool/run'
    #file = {'corpus': ('words.txt', " ".join([t for line in tokens for t in line if t not in arpabet.keys()]))}
    #res = requests.post(base_url, \
    #                    data={'formtype': 'simple'}, \
    #                    files=file, allow_redirects=True)
    #dict_re = re.compile(r"\d+\.dic")
    #dict_path = dict_re.search(res.text).group(0)
    #res = requests.get(res.url + dict_path)


if __name__ == '__main__':
    main()