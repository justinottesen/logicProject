# How To Git (and GitHub)

This is a simplified tutorial for how we will use Git and GitHub in this project. It will not cover everything, but it will cover most of what you should need to know when working in a project of two people. It will be more geared towards **what** to do, rather than **why** or **how**. If you have any questions or run into any problems, ask me (Justin) for help.

You should use the command line for Git, using anything else may be easy 90% of the time, but it only makes the already easy parts easy. This whole tutorial will assume you are using the git command line interface. I will be writing this from an Ubuntu Linux perspective, but everything I say should also apply to Windows, I just do not have as much experience there.

I will also outline some instructions here for how to configure GitHub to avoid us shooting ourselves in the foot, because mistakes always happen, and some are more permanent than others. If you aren't sure how to follow my instructions there, feel free to ask for help, or you can transfer repository ownership to me, instructions for that are below as well.

## General Overview

As its name implies, `main` is the main branch. It is the trunk of our version control tree, and should always contain a coherent and working version of our code. When you would like to make code changes, you will branch off of main, do all work on that branch, then submit a Pull Request to merge your code back into main. This helps us catch mistakes before they make it into the shared `main` branch, and forces both team members to be aware of what changes are made and what needs to be done next.

## Setting up GitHub

Again, if you have a hard time following these steps, or just don't feel like it, you can transfer ownership to me. To do this, go to the `Settings` tab, scroll to the bottom and click `Transfer` under `Transfer ownership`. Select `Specify an organization or username`, and type in `justinottesen` to transfer it to me. Follow the remaining instructions and click `I understand, transfer this repository`.

If you are feeling brave, do the following:
1. Open `Settigs`, choose the `General` option from the sidebar, and scroll down to the `Pull Requests` section. Make sure that `Allow merge commits` is **not** checked, and the other two options (`Allow squash merging` and `Allow rebase merging`) are.
2. Open `Settings` and choose the `Branches` option from the sidebar. Click `Add rule` near the top right. Fill the `Branch name pattern` with `main`, check off `Require a pull request before merging`, check off `Require approvals`, and set the `Required number of approvals before merging` to `1`. Click `Require linear history` and `Do not allow bypassing the above settings`.

These both help prevent us from making mistakes that are both easy to make, and painful to clean up.

## Developer Workflow

This is the process you should go through when you are going to make changes to the code.

1.  Make sure you have the most up to date version of `main`, and create a branch off of it. For example, if I am going to add statement parsing, I would run the following commands:
    ```sh
    git checkout main                   # Switches you to the main branch
    git pull                            # Pulls all changes from GitHub into your local repository
    git checkout -b statement_parsing   # Creates a new branch and switches to it
    ```
    The comments pretty clearly explain what is happening here. To verify that you end up on the right branch, you can run `git branch`, which will output a `*` next to the branch you are currently on.
2.  Make whatever changes you want to make on your branch, code as normal. As you are making progress, you should make commits to document what you are doing. I will assume you know how this part works. Just run `git add <path>` and `git commit -m "<commit message>"`. Once you are done, run `git push`, and just copy-paste what the error message says if it gives you one.
3. Once you have pushed, go to GitHub to create a pull request. When you open the website, it should prompt you with the button to open a pull request. If not, go to the `Pull Requests` tab, select `New pull request`, and choose `main` as the `base` branch, and your branch as the `compare` branch. Choose a title and description, and wait for team member approval on your pull request.
4. Your team member may have feedback or requests, address them by pushing new commits on that branch. Once you have an approved pull request, merge into `main` using either the `Squash and merge` option, or the `Rebase and merge` option. Squashing combines all commits from the branch into one when you merge it, rebasing preserves them as separate commits.

    If it tells you to solve a merge conflict, let me know, and I can take care of that for you. The preferred way of doing this is a bit more involved, it uses `git rebase`.

## Reviewing Pull Requests

To review your team member's pull request, open it and press the "files changed" tab. There, you should see all the changes made in the pull request. You can add comments by each line. Once you have reviewed the code changes, click the green `Review changes` button in the top right, select either `Comment`, `Approve`, or `Request Changes`, and click `Submit Review`.