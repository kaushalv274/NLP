#!/usr/bin/env python
import distsim
word_to_vec_dict = distsim.load_word2vec("nyt_word2vec.4k")
###Provide your answer below

###Answer examples
ans = list()

ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['miami'],set(['miami']),distsim.cossim_dense))
ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['doctor'],set(['doctor']),distsim.cossim_dense))
ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['giant'],set(['giant']),distsim.cossim_dense))
ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['agree'],set(['agree']),distsim.cossim_dense))
ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['terrorist'],set(['terrorist']),distsim.cossim_dense))
ans.append(distsim.show_nearest(word_to_vec_dict, word_to_vec_dict['hotel'],set(['hotel']),distsim.cossim_dense))

for item in ans:
    print item