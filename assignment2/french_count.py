import sys
from fst import FST
from fsmutils import composewords
from fsmutils import trace

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.initial_state = 'start'

    f.add_state('onez')
    f.add_state('onenz')
    f.add_state('twoz')
    f.add_state('threez')
    f.set_final('threez')
    f.add_state('twonz0')
    f.add_state('twonz1')
    f.add_state('twonz2')
    f.add_state('twonz7')
    f.add_state('twonz8')
    f.add_state('twonz9')
    f.add_state('threenz1')
    #for x in range(20):
        #f.add_state('threenz'+str(x))
        #f.set_final('threenz'+str(x))

    f.add_arc('start','onez',('0'),())
    for x in range(1,10):
        if x == 1:
            f.add_arc('start','onenz',(str(x)),[kFRENCH_TRANS[100]])
        else:
            f.add_arc('start','onenz',(str(x)),[kFRENCH_TRANS[x]+" "+kFRENCH_TRANS[100]])
    f.add_arc('onez','twoz',('0'),())


    f.add_arc('onenz','twonz0',('0'),())
    f.add_arc('onenz','twonz1',('1'),())
    for x in range(2,7):
        f.add_arc('onenz','twonz2',(str(x)),[kFRENCH_TRANS[x*10]])
    f.add_arc('onenz','twonz7',('7'),[kFRENCH_TRANS[60]])
    f.add_arc('onenz','twonz8',('8'),[kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])
    f.add_arc('onenz','twonz9',('9'),[kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])

    f.add_arc('onez','twonz1',('1'),())
    for x in range(2,7):
        f.add_arc('onez','twonz2',(str(x)),[kFRENCH_TRANS[x*10]])
    f.add_arc('onez','twonz7',('7'),[kFRENCH_TRANS[60]])
    f.add_arc('onez','twonz8',('8'),[kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])
    f.add_arc('onez','twonz9',('9'),[kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])

    f.add_arc('twoz','threez',('0'),['zero'])
    for x in range(1,9):
        f.add_arc('twoz','threenz1',(str(x)),[kFRENCH_TRANS[x]])

    lst = [0,8]
    for ele in lst:
        for x in range(10):
            if x == 0:
                f.add_arc('twonz'+str(ele),'threenz1',(str(x)),())
            else:
                f.add_arc('twonz'+str(ele),'threenz1',(str(x)),[kFRENCH_TRANS[x]])

    lsst = [1,7,9]
    for ele in lsst:
        for x in range(7):
            if ele==7 and x==1:
                f.add_arc('twonz'+str(ele),'threenz1',(str(x)),[kFRENCH_AND+" "+kFRENCH_TRANS[x+10]])
            else:
                f.add_arc('twonz'+str(ele),'threenz1',(str(x)),[kFRENCH_TRANS[x+10]])
        for x in range(7,10):
            f.add_arc('twonz'+str(ele),'threenz1',(str(x)),[kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[x]])


    for x in range(10):
        if x ==1:
            f.add_arc('twonz2','threenz1',(str(x)),[kFRENCH_AND+" "+kFRENCH_TRANS[1]])
        elif x==0:
            f.add_arc('twonz2','threenz1',(str(x)),())
        else:
            f.add_arc('twonz2','threenz1',(str(x)),[kFRENCH_TRANS[x]])
    
    f.set_final('threenz1')

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
        #print trace(f,'001')
