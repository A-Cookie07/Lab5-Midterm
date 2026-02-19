#!/usr/bin/env python3
from git import Repo, RemoteProgress
local_dir = "./"
repo = Repo(local_dir)

def main():
    last_commit = repo.head.commit
    print(f"last commit was {last_commit.message}")
    print(f"this_repo remotes {len(repo.remotes)}")

    repo.git.add(all=True)
    message = input("input the commit message: \n")
    repo.index.commit(f"{message}")
    repo.remote("origin").push()

if __name__ == "__main__":
    main()
