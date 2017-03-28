#!/Users/lemur/anaconda/bin/python
from random import shuffle
import sys


def make_groups(student_list, number_of_groups):
    '''
    Divide into some number of groups a list of students

    INPUT: list, int
        - list of names
        - number of groups to divide it into
    OUTPUT: list of lists
    '''
    assert number_of_groups >= 1, 'Number of groups must be >= 1'
    shuffle(student_list)
    groups = [[] for _ in range(number_of_groups)]
    while student_list:
        for index in range(number_of_groups):
            groups[index].append(student_list.pop())
            if not student_list:
                break
    return groups


def show_groups(student_list, number_of_groups, labels=None):
    '''
    Print the group assignments for students

    INPUT: list, int, list
        - list of names
        - number of groups to divide it into
        - list of labels for groups
    '''
    if labels:
        assert len(labels) == number_of_groups, "should have same number of groups and labels"
    grouped = make_groups(student_list, number_of_groups)
    o_line = '{}, ' * 5
    o_line = o_line.strip(', ')
    for i, group in enumerate(grouped):
        if labels:
            print '{}:'.format(labels[i])
        else:
            print 'Group #{}:'.format(i+1)
        for student in group:
            print '\t{}'.format(student)


def grab_students_from_file(path):
    '''
    Get a list of students from a cohort file. Assumes the file is formated with
    student names one per line as: github_user_name,student_name

    INPUT: string
        - path to the student file
    OUTPUT: list
        - list of student names
    '''
    students = []
    with open(path, 'r') as f:
        for line in f:
            students.append(line.strip().split(',')[-1])
    return students


def main():
    '''
    print student groups to the terminal
    pass in path to student file and either number of groups or sequence of labels
    lables are defined as sequential arguments after the path of the students file
    '''
    students = grab_students_from_file(sys.argv[1])
    if len(sys.argv) > 3:
        labels = sys.argv[2:]
        shuffle(labels)
        show_groups(students, len(labels), labels)
    else:
        show_groups(students, int(sys.argv[2]))


if __name__ == '__main__':
    main()
