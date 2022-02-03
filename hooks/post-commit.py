# IMPORTS
import os
import sys
import time
from datetime import datetime
import git
import shutil

# DRIVE YOU WANT TO SAVE TO | YOU CAN EXTEND THE PATH IF YOU WOULD LIKE
destinationdrive = "D:/"
# USE GITIGNORE?
gitignore = False

# CALLS FUNCTIONS
def Main(destinationdrive):
    # SETS THE SOURCE DIRECTORY
    source = GetSourceDir()
    # GETS PROJECT (FOLDER) NAME
    projectchoice = os.path.basename(source)
    # GETS CURRENT DATE
    now = datetime.now()
    # GETS LOCAL REPOSITORY DATA
    repo = GetRepo(source)
    # GETS COMMIT DATA FROM REPOSITORY
    commit = repo.head.commit
    # READS YOUR GITIGNORE AND PUTS THE DATA IN A LIST
    if gitignore:
        ignorelist = IgnoreList(source)
    else:
        ignorelist = []
    # SETS THE DESTINATION FOR THE BACKUP
    dest = SetDestination(destinationdrive, repo, commit, projectchoice, now)
    # COPIES THE PROJECT AND GETS THE TIME TAKEN
    timeelapsed = CopyProject(source, dest, ignorelist)
    # LOGS INFORMATION IN THE BACKUP DESTINATION
    GitLog(repo, commit, dest, now, timeelapsed)
    # TELLS USER THE BACKUP IS DONE
    print("Backup Complete.")

# SETS THE SOURCE DIRECTORY
def GetSourceDir():
    try:
        source = os.getcwd()
        return source
    except:
        sys.exit("ERROR: Could not get the project directory.")

# GETS LOCAL REPOSITORY DATA
def GetRepo(source):
    try:
        repo = git.Repo(source + "/.git")
        return repo
    except git.NoSuchPathError:
        sys.exit("ERROR: Could not find the git information.")

# READS YOUR GITIGNORE AND PUTS THE DATA IN A LIST
def IgnoreList(source):
    ignore = []
    try:
        gitignorefile = open(source + "/.gitignore", "r")
    except FileNotFoundError:
        sys.exit("ERROR: Could not find gitignore file.")
    for line in gitignorefile:
        # FILTERS OUT COMMENTS AND BLANK LINES
        if not line.startswith('#') and line.strip():
            # GETS RID OF BLANK SPACES
            strippedline = line.strip()
            # GETS RID OF END DIRECTORY SLASHES
            rstrippedline = strippedline.rstrip('/')
            ignore.append(rstrippedline)
    gitignorefile.close()
    return ignore

# SETS THE DESTINATION FOR THE BACKUP
def SetDestination(destinationdrive, repo, commit, projectchoice, now):
    datetimestring = now.strftime("%m%d%Y%H%M%S")
    try:
        # GETS FOLDER NAMES IN BACKUP DIRECTORY
        for filename in os.listdir(destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name)):
            # LOOKS FOR THE MOST RECENT COMMITS SHORT HASH
            if str(repo.git.rev_parse(commit.hexsha, short=7)) in filename:
                sys.exit("ERROR: A backup of this commit was already detected in %s" % (destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name)))
            else:
                return destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name) + "/" + str(repo.git.rev_parse(commit.hexsha, short=7)) + "_" + datetimestring + "_" + str. rstrip(commit.summary)
    # IF THE DIRECTORY DOESNT EXIST YET THEN IT WILL MAKE IT
    except FileNotFoundError:
        return destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name) + "/" + str(repo.git.rev_parse(commit.hexsha, short=7)) + "_" + datetimestring + "_" + str. rstrip(commit.summary)

# COPIES THE PROJECT AND GETS THE TIME TAKEN
def CopyProject(source, dest, ignorelist):
    starttime = time.time()
    try:
        shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*ignorelist))
    except:
        sys.exit("ERROR: Could not copy files.")
    endtime = time.time()
    # STOPS THE TIME ELAPSED 2 PLACES AFTER THE DECIMAL POINT
    try:
        timeelapsed = endtime - starttime
        timeelapsedstring = str(timeelapsed)
        timeelapsedpartition = timeelapsedstring.partition('.')
        timelist = list(timeelapsedpartition)
        timems = timelist[2]
        timems = timems[:2]
        return timelist[0] + timelist[1] + timems
    except:
        return endtime - starttime

# LOGS INFORMATION IN THE BACKUP DESTINATION
def GitLog(repo, commit, dest, now, timeelapsed):
    lines = ['Author - ' + str(commit.author), 'Authored Date - ' + str(commit.authored_datetime), 'Committed Date - ' + str(commit.committed_datetime), 'Backup Date - ' + str(now.strftime("%m/%d/%Y %H:%M:%S")), 'Time Elapsed - ' + str(timeelapsed) + ' seconds', 'Branch - ' + str(repo.active_branch.name), 'Hash - ' + str(commit.hexsha), 'Short Hash - ' + str(repo.git.rev_parse(commit.hexsha, short=7)), 'Summary - ' + str(commit.summary), 'Message - ' + str.strip(commit.message.replace(commit.summary, ""))]
    try:
        with open(dest + '/backuplog.txt', 'w') as file:
            file.write('\n'.join(lines))
    except FileNotFoundError:
        sys.exit("ERROR: Could not write log in destination directory.")

Main(destinationdrive)