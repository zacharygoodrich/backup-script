# backup-script
A python script to create a local backup of your projects, either by manually launching or though git hooks. Utilizes your gitignore in the backup.
### Prerequisite
Both of these scripts rely on __GitPython__. If you do not have it installed please follow their install instructions [here](https://gitpython.readthedocs.io/en/stable/intro.html).
## Manual Script (backupscript.py)
- First open the file, set the source (directory that holds your projects), and the drive you want to backup to (Default is D Drive). 
  - You can extend the drive path if you would like. (e.g. "D:/MyProjects/")
- When you run the script, it will list the projects in your source directory for you to choose to backup.
- If it finds a local git repository, then just wait for it to say that the backup is complete, and that is it!
  - If it does not find a repository, then it will request for a summary and a message. Again, wait for it to say that the backup is complete.
- A log will be made and put into the backup location, listing commit info (or just a summary and message), and the time to copy.
## Hooks (post-commit)
- Drag the two files in the hook folder (both named post-commit) and put them into the hooks folder of your project's local repository (.git).
  - If you do not see a .git folder, you may have view hidden items turned off in file explorer.
- In the post-commit shell file (the one that's not python), change the directory in quotations to your python executable location. 
  - The one included is the default for Windows, just change the YOURUSER to your windows username.
- Then, in the post-commit.py file, change the drive you want to backup to (Default is D Drive). 
  - You can extend the drive path if you would like. (e.g. "D:/MyProjects/")
- That's it! Now it should backup every time you commit that project. 
  - If it isn't backing up correctly, or at all, try committing through the command line, or run the manual script. It should give you an error message of what is going wrong.
