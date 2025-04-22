# Formal Proof Helper

This is the repository containing the final project for CSCI 4420 - Computability & Logic, submitted by Justin Ottesen and Murray Copps. This project is a web app which assists users with Fitch-style proofs. The interface is very similar to the Fitch software used during the course, so we do not have specific usage instructions. Most of those instructions should apply.

## Features

### Roadmap

The roadmap of goals for the project are below. Depending on time constraints, as well as difficulty of implementation, we may not reach all milestones, but at minimum, we hope to complete the first 3 steps. Steps 4 and 5 are reach goals, which would be nice to have. We also are only implementing propositional logic for simplicity.

1. **Fitch Recreation** - The first step is to recreate a Fitch-style proof interface. This includes premises, conclusions, steps with justifications, introduction and elimination rules, and verifying correctness of steps and proofs.

2. **Patterns & Shortcuts** - There are many common patterns which can be used to take shortcuts, for example excluded middle, which can be proven using elimination and introduction rules. There will be some sort of store of these which can be used as lemmas in proofs.

3. **Step Scoring** - Next, we will generate a list of possible next steps (or lemmas as mentioned above) to take. These will be ordered using a simple scoring algorithm based on some version of edit distance to the conclusion statement.

4. **Look Ahead** - Now that we have a way of scoring steps, we can calculate scores using a breadth first search algorithm, which scores each state using the best possible score of any reachable state from the current state.

5. **Informed Search** - We can improve on our search algorithm by expanding possible choices according to some heuristic, possibly something as simple as our previous scoring heuristic, rather than just what we happen to expand first.

### Current Status

Web-App Support: Step 1

CLI Support: Step 2

## Setup Instructions
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app). The backend is a python module, managed by the `pyproject.toml` file.

Requirements (Hopefully not missing anything):
- `npm`: Package manager for npm front end
- `python`: Language for the backend

### Run Web-App

There are three scripts in the `scripts` directory, depending on your operating system and setup.

**Linux**: Start the program by running `run.sh`

**Windows**: There are a few options to try, depending on your preferences:
- There is a `run.bat` file, which can be run in a command prompt, or double clicked in a folder to run.
- There is a `run.ps1` file which can be run in powershell. You may get an error / warning message, which should be able to be resolved by running the following:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Once the system is running, go to http://localhost:3000/ and you should see the interface.

### Developer Setup

#### Front End

Run one of the `dev_setup` scripts in `frontend/scripts`, depending on your flavor of operating system. Once this is done, you can run `npm run dev` in the front end folder to just run the front end in isolation.

The front end communicates with the backend, so running it in isolation will likely not be too useful.

#### Back End

Run one of the `dev_setup` scripts in `backend/scripts`, depending on your flavor of operating system. Once this is done, you must activate the python virtual environment which should have been created at `backend/.venv`. Instructions for this are printed at the end of the `dev_setup` output script.

To run the backend in server mode, run `proof_server` in the command line. If you want a help menu, run `proof_server -h`.

To run the backend as a command line interface, run `proof_cli`. Again, for a help menu, run `proof_cli -h`.

To execute the full test suite, run `pytest` in the `backend` directory. For a help menu, run `pytest -h`