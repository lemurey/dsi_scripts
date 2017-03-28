#!/Users/lemur/anaconda2/bin/python
import matplotlib
matplotlib.use("Qt5Agg")
import pickle, sys, os
import matplotlib.pyplot as plt
from numpy.random import choice

def random_student(s, specific = None):
    '''
    INPUT:
        s: dictionary of {student name: student picture} or a list of student names
        specific: (optional) a specific key to use in dictionary
    OUTPUT: None

    if s is a dictionary, then it picks a random key from the dictionary and
    shows that students photo, with title of thier name
    if s is a list, it shows a random students name

    if specific is passed, it uses that value as the key of dictionary, or 
    prints that value if s is a list
    '''
    if isinstance(s, dict):
        key = choice(s.keys())
        if specific:
            key = specific
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(1500, 0, 350, 545)
        plt.imshow(s[key])
        plt.title(key)
        f = plt.gca()
        f.get_yaxis().set_visible(False)
        f.get_xaxis().set_visible(False)
        plt.show()
    else:
        key = choice(s)
        if specific:
            key = specific
        print key

def main():
    '''
    INPUT: None
    OUTPUT: None

    gets a random student from either the current cohort, or from a specified
    cohort if a cohort number is provided
    Can optionally take a specific student name and output their picture
    '''
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        base = os.environ['BASESTUDENT']
        base = base.format(sys.argv[1])
        cur_cohort = base.format('pkl')
        cur_students = base.format('txt')
    else:
        cur_cohort = os.environ['COHORT']
        cur_students = os.environ['STUDENTS']
    if os.path.isfile(cur_cohort):
        with open(cur_cohort, 'rb') as f:
            s = pickle.load(f)
    else:
        s = []
        with open(cur_students, 'r') as f:
            for line in f:
                s.append(line.split(',')[-1].strip())
    if len(sys.argv) == 1:
        sys.argv.append('1')
    if len(sys.argv) > 2:
        return random_student(s,sys.argv[2])
    elif not sys.argv[1].isdigit():
        return random_student(s,sys.argv[1])
    return random_student(s)

if __name__ == '__main__':
    main()    
