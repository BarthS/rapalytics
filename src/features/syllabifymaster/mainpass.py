    ## main pass
    mypron = list(pron)
    nuclei = []
    onsets = []
    i = -1
    for (j, seg) in enumerate(mypron):
        if seg in VOWELS:
            nuclei.append([seg])
            onsets.append(mypron[i + 1:j]) # actually interludes, r.n.
            i = j                        
    codas = [mypron[i + 1:]]
    ## resolve disputes and compute coda
    for i in range(1, len(onsets)):
        coda = []
        # boundary cases
        if len(onsets[i]) > 1 and onsets[i][0] == 'R':
            nuclei[i - 1].append(onsets[i].pop(0))
        if len(onsets[i]) > 2 and onsets[i][-1] == 'Y':
            nuclei[i].insert(0, onsets[i].pop())
        if len(onsets[i]) > 1 and alaska_rule and nuclei[i-1][-1] in SLAX \
                                              and onsets[i][0] == 'S':
            coda.append(onsets[i].pop(0))
        # onset maximization
        depth = 1
        if len(onsets[i]) > 1:
            if tuple(onsets[i][-2:]) in O2:
                depth = 3 if tuple(onsets[i][-3:]) in O3 else 2
        for j in range(len(onsets[i]) - depth):
            coda.append(onsets[i].pop(0))
        # store coda
        codas.insert(i - 1, coda)

    ## verify that all segments are included in the ouput
    output = zip(onsets, nuclei, codas)
    flat_output = list(chain.from_iterable(chain.from_iterable(output)))
    if flat_output != mypron:
        raise ValueError("could not syllabify {}, got {}".format(mypron, 
                                                           flat_output))
    return output