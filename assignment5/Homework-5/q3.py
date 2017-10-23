#!/usr/bin/env python
import distsim

# you may have to replace this line if it is too slow 
word_to_ccdict = distsim.load_contexts("nytcounts.4k")


### provide your answer below
ans = list()
###Answer examples
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['miami'],set(['miami']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['doctor'],set(['doctor']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['giant'],set(['giant']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['agree'],set(['agree']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['terrorist'],set(['terrorist']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['hotel'],set(['hotel']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['hospital'],set(['hospital']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['seattle'],set(['seattle']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['california'],set(['california']),distsim.cossim_sparse))
ans.append(distsim.show_nearest(word_to_ccdict, word_to_ccdict['california'],set(['california']),distsim.cossim_sparse))

for item in ans:
    print item