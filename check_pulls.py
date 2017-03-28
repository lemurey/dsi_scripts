#!/Users/lemur/anaconda/bin/python
from pygithub3 import Github
from datetime import datetime
import argparse, getpass

def check_project_pulls(students, login, password, repo='project-proposals', dates=False):
    '''
    INPUT: 
        students: dictionary
        login: string
        password: string
        repo: string
    OUTPUT: dictionary

    takes a dictionary of form {github user name: student name}
    also takes github username and password for access to the zipfian repo,
    can pass in repo name if checking something other than project-proposals

    returns a dictionary with students who have not submitted pulls to
    the repo
    '''
    gh = Github(login=login, password=password, user='zipfian', repo=repo )

    total_students = len(students)
    updates = {student:[] for student in students.values()}

    res = gh.pull_requests.list()
    num_pulls = 0
    for page in res:
        users = list(page)
        for u in users:
            username = u.user['login'].lower()
            if username in students:
                updates[students[username]] = u.updated_at
                num_pulls += 1
                del students[username]
    
    if not dates:
        left_to_pull = total_students-num_pulls
        return left_to_pull,students
    else:
        return updates

def get_students(filename):
    '''
    INPUT:
        filename: string
    OUTPUT:
        students: dictionary

    takes in a filename for a text file which has the students github usernames 
    and names as comma separated values on each line, returns a dictionary of
    {github user name: student name}
    '''
    students = {}
    with open(filename,'r') as f:
        for line in f:
            l = line.split(',')
            students[l[0].lower()] = ' '.join(l[1:]).strip()
    return students

def parse_date(date):
    '''
    INPUT:
        date: string
    OUTPUT:
        compdate: python datetime object

    converts a dd/mm/yyyy string into a python datetime object
    '''
    if '/' in date:
        dates = date.split('/')
    else:
        return 'improperly formated date'

    formated = [0,1,2]
    for i,elem in enumerate(dates):
        if i <= 1:
            if len(elem) > 2 or len(elem) < 1:
                return 'improperly formated date'
        else:
            if len(elem) != 4:
                return 'improperly formated date'
        formated[i] = int(elem)

    month,day,year = formated

    compdate = datetime(year,month,day,0,0,0)
    return compdate

def parse_updates(updates,date):
    '''
    INPUT:
        updates: dictionary
        date: datetime object
    OUTPUT:
        None

    prints student names who have not updated pull requests after a specified
    date
    '''
    for k,v in updates.iteritems():
        if v < date:
            print k

def main():  
    '''
    INPUT:
        None
    OUTPUT:
        None

    parses command line arguments and determines if students have made pull 
    requests to a repo. Defaults to checking for pull requests in a binary way
    for the project-proposals repo. Other repos can be specified with the --repo
    or -r flags. If the --date or -d flag is set with a mm/dd/yyyy date it will
    check if pull requests have been made after that date.

    Requires the pygithub3 module, can get it with pip install pygithub3
    '''

    parser = argparse.ArgumentParser(description='Check for student pull requests to a zipfian repo')
    parser.add_argument('students',
                        type=str,
                        nargs=1,
                        help='path to students file. A list of student github usernames and names separated by a comma. username1,student 1 username2,student 2')
    parser.add_argument('username',
                        type=str,
                        nargs=1,
                        help='github username'
                        )
    parser.add_argument('--repo', '-r',
                        metavar='repo',
                        type=str,
                        nargs=1,
                        help='repo to check for pull requests to, defaults to project-proposals'
                        )
    parser.add_argument('--date','-d',
                        metavar='end date',
                        type=str,
                        nargs=1,
                        help='comparison date in mm/dd/yyyy format')
    parser.add_argument('--password','-p',
                        metavar='password',
                        type=str,
                        nargs=1,
                        help='github password, optional, if left out will prompt user for password later on')

    args = parser.parse_args()
    students = get_students(args.students[0])
    user = args.username[0]

    if args.password:
        password = args.password[0]
    else:
        password = getpass.getpass()

    if args.repo: 
        repo = args.repo[0]
    else: 
        repo = 'project-proposals'

    if args.date:
        date = parse_date(args.date[0])
    else:
        date = None

    if date:
        if isinstance(date, datetime):
            updates = check_project_pulls(students, user, password, repo=repo, dates=True)
            parse_updates(updates,date)
        else:
            print 'Please enter your date formated as mm/dd/yyyy'
        
    else:
        num, students = check_project_pulls(students, user, password, repo=repo)
        print num
        for name in students.values():
            print name



if __name__ == '__main__':
    main()

