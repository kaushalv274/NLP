import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is a size N array of integers representing the best sequence.
    """
    print emission_scores
    print
    print trans_scores
    print
    print start_scores
    print
    print end_scores
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    y = []

    # Create two temp 2D array to store optimal values and backpointers
    # size of both of these arrays would be NxL. 
    back_pointers = np.zeros(emission_scores.shape, dtype=np.int32)
    values = np.zeros(emission_scores.shape)
    values -= 100000

    for i in xrange(L):
        values[0][i] = emission_scores[0][i] + start_scores[i]
        back_pointers[0][i] = 0

    for i in xrange(N-1):
        for j in xrange(L):
            for k in xrange(L):
                val = emission_scores[i+1][j] + values[i][k] + trans_scores[k][j]
                if val > values[i+1][j]:
                    values[i+1][j] = val
                    back_pointers[i+1][j] = k
    score = -10000
    last_tag_index = 0
    for i in xrange(L):
        val = values[N-1][i] + end_scores[i]
        if val>score:
            score = val
            last_tag_index = i
    tag_list = list()
    tag_list.append(last_tag_index)
    last_tag = last_tag_index
    for i in xrange(N-1,0,-1):
        tag_list.append(back_pointers[i][last_tag])
        last_tag = back_pointers[i][last_tag]

    for i in xrange(N):
        # stupid sequence
        y.append(i % L)
    # score set to 0
    return (score, tag_list[::-1])
