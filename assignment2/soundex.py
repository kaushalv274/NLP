from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('next')
    f1.initial_state = 'start'

    #create 0,1,2,3,4,5,6 states for all classes
    for x in range(0,7):
        f1.add_state(str(x))
        f1.set_final(str(x))

    list_0 = ['a','e','h','i','o','u','w','y']
    list_1 = ['b','f','p','v']
    list_2 = ['c','g','j','k','q','s','x','z']
    list_3 = ['d','t']
    list_4 = ['l']
    list_5 = ['m','n']
    list_6 = ['r']

    all_lists = [list_0,list_1,list_2,list_3,list_4,list_5,list_6]
    # Set all the final states

    for index,item in enumerate(all_lists):
        for letter in item:
            f1.add_arc('start',str(index),(letter),(letter))
            f1.add_arc('start',str(index),(letter.upper()),(letter.upper()))


    for x in range(0,7):
        for index,item in enumerate(all_lists):
            for letter in item:
                if x == index:
                    f1.add_arc(str(x),str(index),(letter),())
                    f1.add_arc(str(x),str(index),(letter.upper()),())
                elif index == 0:
                    f1.add_arc(str(x),str(index),(letter),())
                    f1.add_arc(str(x),str(index),(letter.upper()),())
                else:
                    f1.add_arc(str(x),str(index),(letter),(str(index)))
                    f1.add_arc(str(x),str(index),(letter.upper()),(str(index)))

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('start')
    f2.initial_state = 'start'
    for x in range(4):
        f2.add_state(str(x))
        f2.set_final(str(x))

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('start', '0', (letter), (letter))

    for n in range(10):
        f2.add_arc('start','1',(str(n)),(str(n)))

    for x in range(3):
        for n in range(10):
            f2.add_arc(str(x), str(x+1), (str(n)), (str(n)))

    for n in range(10):
        f2.add_arc(str(3),str(3),(str(n)),())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('start')
    f3.initial_state = 'start'
    for x in range(4):
        f3.add_state(str(x))
    f3.set_final(str(3))

    # Add the arcs
    f3.add_arc(str(0),str(1),(''),('0'))
    f3.add_arc('start','1',(''),('0'))
    f3.add_arc(str(1),str(2),(''),('0'))
    f3.add_arc(str(2),str(3),(''),('0'))

    for letter in string.letters:
        f3.add_arc('start', '0', (letter), (letter))

    for n in range(10):
        f3.add_arc('start','1',(str(n)),(str(n)))
    

    for x in range(3):
        for n in range(10):
            f3.add_arc(str(x), str(x+1), (str(n)), (str(n)))
        

    for n in range(10):
        f3.add_arc(str(3),str(3),(str(n)),())

    '''
    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')
    
    f3.initial_state = '1'
    f3.set_final('2')

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1', (str(number)), (str(number)))
    
    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))
    '''
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
