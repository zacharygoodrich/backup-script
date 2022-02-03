# IMPORTS
import os
import sys
import time
from datetime import datetime
import git
import shutil

# DIRECTORY OF YOUR PROJECTS | NOT THE DIRECTORY OF THE PROJECT ITSELF
source = ""
# DRIVE YOU WANT TO SAVE TO | YOU CAN EXTEND THE PATH IF YOU WOULD LIKE
destinationdrive = "D:/"

# CALLS FUNCTIONS
def Main(source, destinationdrive):
    # GETS PROJECT (FOLDER) NAMES IN SOURCE DIRECTORY, AND HAS YOU PICK WHICH ONE TO BACKUP
    projectchoice = ChooseProject(source)
    # ADDS THE PROJECT (FOLDER) NAME TO THE SOURCE DIRECTORY
    source += projectchoice
    # GETS CURRENT DATE
    now = datetime.now()
    # GETS LOCAL REPOSITORY DATA
    repo = GetRepo(source)
    # CHECKS IF THERE IS NO GIT INFO
    if repo == None:
        BackupNoGit(source, projectchoice, now)
    # GETS COMMIT DATA FROM REPOSITORY
    commit = repo.head.commit
    # READS YOUR GITIGNORE AND PUTS THE DATA IN A LIST
    ignorelist = IgnoreList(source)
    # SETS THE DESTINATION FOR THE BACKUP
    dest = SetDestinationGit(destinationdrive, repo, commit, projectchoice, now)
    # COPIES THE PROJECT AND GETS THE TIME TAKEN
    timeelapsed = CopyProject(source, dest, ignorelist)
    # LOGS INFORMATION IN THE BACKUP DESTINATION
    GitLog(repo, commit, dest, now, timeelapsed)
    # TELLS USER THE BACKUP IS DONE
    input("Backup Complete. Press ENTER to exit.")
    sys.exit()

# GETS PROJECT (FOLDER) NAMES IN SOURCE DIRECTORY, AND HAS YOU PICK WHICH ONE TO BACKUP
def ChooseProject(source):
    # GETS FOLDER NAMES IN THE SOURCE DIRECTORY
    try:
        directories = [filename for filename in os.listdir(source) if os.path.isdir(os.path.join(source, filename))]
    except:
        input("ERROR: Could not read folders in source directory. Press ENTER to exit.")
        sys.exit()
    # LISTS THE FOLDERS WITH NUMBERS
    for number, word in enumerate(directories, 1):
        print(number, word)
    projectchoice = input('Choose which project you want to backup: ')
    # LOOPS IF YOU INPUT THE PROJECTS FOLDER NAME WRONG
    for i in range(0,100):
        while True:
            # CHECKS IF USER IS SELECTING BY NUMBER
            try:
                projectchoiceint = int(projectchoice) - 1
                if len(directories) < projectchoiceint:
                    projectchoice = input("That does not match a folder name or number, please try again: ")
                else:
                    return directories[projectchoiceint]
            # CHECKS IF USER IS SELECTING BY FOLDER NAME
            except:
                if projectchoice not in directories:
                    projectchoice = input("That does not match a folder name or number, please try again: ")
                else:
                    return projectchoice

# GETS LOCAL REPOSITORY DATA
def GetRepo(source):
    try:
        repo = git.Repo(source + "/.git")
        return repo
    except git.NoSuchPathError:
        continuebackup = input("ERROR: Could not find the git information. Would you like to backup without git information? ").lower()
        if continuebackup.startswith('y'):
            return None
        elif continuebackup.startswith('n'):
            sys.exit()

#  LETS YOU INSERT DATA TO BACKUP IF GIT INFO IS NOT FOUND
def BackupNoGit(source, projectchoice, now):
    datetimestring = now.strftime("%m%d%Y%H%M%S")
    # USED IN FOLDER NAME
    summary = input("Give the backup a summary: ")
    # USED IN LOGS
    message = input("Give the backup a message: ")
    # SETS THE DESTINATION FOR THE BACKUP
    dest = destinationdrive + projectchoice + "_Backup/" + datetimestring + "_" + summary
    # COPIES THE PROJECT AND GETS THE TIME TAKEN
    timeelapsed = CopyProject(source, dest, [])
    # LOGS INFORMATION IN THE BACKUP DESTINATION
    Log(dest, summary, message, now, timeelapsed)
    # TELLS USER THE BACKUP IS DONE
    input("Backup Complete. Press ENTER to exit.")
    sys.exit()

# READS YOUR GITIGNORE AND PUTS THE DATA IN A LIST
def IgnoreList(source):
    ignore = []
    try:
        gitignorefile = open(source + "/.gitignore", "r")
    except FileNotFoundError:
        input("ERROR: Could not find gitignore file. Press ENTER to exit.")
        sys.exit()
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
def SetDestinationGit(destinationdrive, repo, commit, projectchoice, now):
    datetimestring = now.strftime("%m%d%Y%H%M%S")
    try:
        # GETS FOLDER NAMES IN BACKUP DIRECTORY
        for filename in os.listdir(destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name)):
            # LOOKS FOR THE MOST RECENT COMMITS SHORT HASH
            if str(repo.git.rev_parse(commit.hexsha, short=7)) in filename:
                # CHECKS IF THE USER WANTS TO BACKUP IF IT FINDS A DUPLICATE COMMIT BACKUP
                newname = input("A backup of the most recent commit already exists! Would you like to give this backup a new name? ").lower()
                if newname.startswith('y'):
                    return destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name) + "/" + datetimestring + "_" + input("Give the backup a summary: ")
                elif newname.startswith('n'):
                    cancelbackup = input("Would you like to cancel with backup? ").lower()
                    if cancelbackup.startswith('y'):
                        sys.exit()
                    elif cancelbackup.startswith('n'):
                        return destinationdrive + projectchoice + "_Backup/" + str(repo.active_branch.name) + "/" + str(repo.git.rev_parse(commit.hexsha, short=7)) + "_" + datetimestring + "_" + str. rstrip(commit.summary)
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
        input("ERROR: Could not copy files. Press ENTER to exit.")
        sys.exit()
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
def Log(dest, summary, message, datetime, timeelapsed):
    lines = ['Summary - ' + str(summary), 'Message - ' + str(message), 'Backup Date - ' + str(datetime.strftime("%m/%d/%Y %H:%M:%S")), 'Time Elapsed - ' + str(timeelapsed) + ' seconds']
    try:
        with open(dest + '/backuplog.txt', 'w') as file:
            file.write('\n'.join(lines))
    except FileNotFoundError:
        input("ERROR: Could not write log in destination directory. Press ENTER to exit.")
        sys.exit()

# LOGS INFORMATION IN THE BACKUP DESTINATION
def GitLog(repo, commit, dest, now, timeelapsed):
    lines = ['Author - ' + str(commit.author), 'Authored Date - ' + str(commit.authored_datetime), 'Committed Date - ' + str(commit.committed_datetime), 'Backup Date - ' + str(now.strftime("%m/%d/%Y %H:%M:%S")), 'Time Elapsed - ' + str(timeelapsed) + ' seconds', 'Branch - ' + str(repo.active_branch.name), 'Hash - ' + str(commit.hexsha), 'Short Hash - ' + str(repo.git.rev_parse(commit.hexsha, short=7)), 'Summary - ' + str(commit.summary), 'Message - ' + str.strip(commit.message.replace(commit.summary, ""))]
    try:
        with open(dest + '/backuplog.txt', 'w') as file:
            file.write('\n'.join(lines))
    except FileNotFoundError:
        input("ERROR: Could not write log in destination directory. Press ENTER to exit.")
        sys.exit()

Main(source, destinationdrive)