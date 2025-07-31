84669@BG10978 MINGW64 /e/labview_vi
$ git init
Initialized empty Git repository in E:/labview_vi/.git/

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        NI_card/

nothing added to commit but untracked files present (use "git add" to track)

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git add .

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git commit -m"set up new labview vi"
[master (root-commit) 79e3576] set up new labview vi
 Committer: ironDING <84669@topband.com>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 NI_card/N-PCI6221-V02.vi

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git push
fatal: No configured push destination.
Either specify the URL from the command-line or configure a remote repository us
ing

    git remote add <name> <url>

and then push using the remote name

    git push <name>


84669@BG10978 MINGW64 /e/labview_vi (master)
$ git config --global user.name "ironDING"

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git config --global user.email "dfs19960926@outlook.com"

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git push
fatal: No configured push destination.
Either specify the URL from the command-line or configure a remote repository us
ing

    git remote add <name> <url>

and then push using the remote name

    git push <name>


84669@BG10978 MINGW64 /e/labview_vi (master)
$ ^C

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git remote add origin https://github.com/fushunDING/labview_vi.git

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git remote -v
origin  https://github.com/fushunDING/labview_vi.git (fetch)
origin  https://github.com/fushunDING/labview_vi.git (push)

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git push -u origin main
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/fushunDING/labview_vi.git
'

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git add .

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git commit -m "set up labview vi"
On branch master
nothing to commit, working tree clean

84669@BG10978 MINGW64 /e/labview_vi (master)
$ git branch -M main

84669@BG10978 MINGW64 /e/labview_vi (main)
$ git push -u origin main
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (4/4), 70.51 KiB | 17.63 MiB/s, done.
Total 4 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/fushunDING/labview_vi.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

84669@BG10978 MINGW64 /e/labview_vi (main)
$ git branch
* main

* ## 创立labview_vi
  
