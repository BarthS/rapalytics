"""
    Syllabifies a CMU dictionary (ARPABET) word string
    
    # Alaska rule:
    >>> pprint(syllabify('AH0 L AE1 S K AH0'.split())) # Alaska
    '-AH0-.L-AE1-S.K-AH0-'
    >>> pprint(syllabify('AH0 L AE1 S K AH0'.split(), 0)) # Alaska
    '-AH0-.L-AE1-.S K-AH0-'

    # huge medial onsets:
    >>> pprint(syllabify('M IH1 N S T R AH0 L'.split())) # minstrel
    'M-IH1-N.S T R-AH0-L'
    >>> pprint(syllabify('AA1  K T R W AA0 R'.split())) # octroi
    '-AA1-K.T R W-AA0-R'

    # destressing
    >>> pprint(destress(syllabify('M IH1 L AH0 T EH2 R IY0'.split())))
    'M-IH-.L-AH-.T-EH-.R-IY-'

    # normal treatment of 'j':
    >>> pprint(syllabify('M EH1 N Y UW0'.split())) # menu
    'M-EH1-N.Y-UW0-'
    >>> pprint(syllabify('S P AE1 N Y AH0 L'.split())) # spaniel
    'S P-AE1-N.Y-AH0-L'
    >>> pprint(syllabify('K AE1 N Y AH0 N'.split())) # canyon
    'K-AE1-N.Y-AH0-N'
    >>> pprint(syllabify('M IH0 N Y UW2 EH1 T'.split())) # minuet
    'M-IH0-N.Y-UW2-.-EH1-T'
    >>> pprint(syllabify('JH UW1 N Y ER0'.split())) # junior
    'JH-UW1-N.Y-ER0-'
    >>> pprint(syllabify('K L EH R IH HH Y UW'.split())) # clerihew
    'K L-EH-.R-IH-.HH Y-UW-'

    # nuclear treatment of 'j'
    >>> pprint(syllabify('R EH1 S K Y UW0'.split())) # rescue
    'R-EH1-S.K-Y UW0-'
    >>> pprint(syllabify('T R IH1 B Y UW0 T'.split())) # tribute
    'T R-IH1-B.Y-UW0-T'
    >>> pprint(syllabify('N EH1 B Y AH0 L AH0'.split())) # nebula
    'N-EH1-B.Y-AH0-.L-AH0-'
    >>> pprint(syllabify('S P AE1 CH UH0 L AH0'.split())) # spatula
    'S P-AE1-.CH-UH0-.L-AH0-'
    >>> pprint(syllabify('AH0 K Y UW1 M AH0 N'.split())) # acumen
    '-AH0-K.Y-UW1-.M-AH0-N'
    >>> pprint(syllabify('S AH1 K Y AH0 L IH0 N T'.split())) # succulent
    'S-AH1-K.Y-AH0-.L-IH0-N T'
    >>> pprint(syllabify('F AO1 R M Y AH0 L AH0'.split())) # formula
    'F-AO1 R-M.Y-AH0-.L-AH0-'
    >>> pprint(syllabify('V AE1 L Y UW0'.split())) # value
    'V-AE1-L.Y-UW0-'

    # everything else
    >>> pprint(syllabify('N AO0 S T AE1 L JH IH0 K'.split())) # nostalgic
    'N-AO0-.S T-AE1-L.JH-IH0-K'
    >>> pprint(syllabify('CH ER1 CH M AH0 N'.split())) # churchmen
    'CH-ER1-CH.M-AH0-N'
    >>> pprint(syllabify('K AA1 M P AH0 N S EY2 T'.split())) # compensate
    'K-AA1-M.P-AH0-N.S-EY2-T'
    >>> pprint(syllabify('IH0 N S EH1 N S'.split())) # inCENSE
    '-IH0-N.S-EH1-N S'
    >>> pprint(syllabify('IH1 N S EH2 N S'.split())) # INcense
    '-IH1-N.S-EH2-N S'
    >>> pprint(syllabify('AH0 S EH1 N D'.split())) # ascend
    '-AH0-.S-EH1-N D'
    >>> pprint(syllabify('R OW1 T EY2 T'.split())) # rotate
    'R-OW1-.T-EY2-T'
    >>> pprint(syllabify('AA1 R T AH0 S T'.split())) # artist
    '-AA1 R-.T-AH0-S T'
    >>> pprint(syllabify('AE1 K T ER0'.split())) # actor
    '-AE1-K.T-ER0-'
    >>> pprint(syllabify('P L AE1 S T ER0'.split())) # plaster
    'P L-AE1-S.T-ER0-'
    >>> pprint(syllabify('B AH1 T ER0'.split())) # butter
    'B-AH1-.T-ER0-'
    >>> pprint(syllabify('K AE1 M AH0 L'.split())) # camel
    'K-AE1-.M-AH0-L'
    >>> pprint(syllabify('AH1 P ER0'.split())) # upper
    '-AH1-.P-ER0-'
    >>> pprint(syllabify('B AH0 L UW1 N'.split())) # balloon
    'B-AH0-.L-UW1-N'
    >>> pprint(syllabify('P R OW0 K L EY1 M'.split())) # proclaim
    'P R-OW0-.K L-EY1-M'
    >>> pprint(syllabify('IH0 N S EY1 N'.split())) # insane
    '-IH0-N.S-EY1-N'
    >>> pprint(syllabify('IH0 K S K L UW1 D'.split())) # exclude
    '-IH0-K.S K L-UW1-D'
    """