#!/usr/bin/env python3
from git import Repo, RemoteProgress
local_dir = "./"
repo = Repo(local_dir)

##
# Overview
# what this does is uses the git Python library to commit any new files / changes to files to the 
# remote repository.  Basically this is the same as doing 
# `git add .`
# `git commit -m`
# `git push`
##

def commit_to_github():
    last_commit = repo.head.commit
    print(f"last commit was {last_commit.message}")
    print(f"this_repo remotes {len(repo.remotes)}")

    repo.git.add(all=True)
    message = input("input the commit message: \n")
    repo.index.commit(f"{message}")
    repo.remote("origin").push()

def main():
    commit_to_github()

if __name__ == "__main__":
    main()
