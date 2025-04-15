# Formal Proof Helper

This is the repository containing the final project for CSCI 4420 - Computability & Logic, submitted by Justin Ottesen and Murray Copps. This project is a web app which assists users with Fitch-style proofs. After the user enters the premises and conclusion, at each step of the proof they will be prompted with an algorithm's best guess as to what the next step of the proof should be.

## Features

### Roadmap

1. **Fitch Recreation** - The first step is to recreate a Fitch-style proof interface. This includes premises, conclusions, steps with justifications, introduction and elimination rules, and verifying correctness of steps and proofs.

2. **Patterns & Shortcuts** - There are many common patterns which can be used to take shortcuts, for example excluded middle, which can be proven using elimination and introduction rules. There will be some sort of store of these which can be used as lemmas in proofs.

3. **Step Scoring** - Next, we will generate a list of possible next steps (or lemmas as mentioned above) to take. These will be ordered using a simple scoring algorithm based on some version of edit distance to the conclusion statement.

4. **Look Ahead** - Now that we have a way of scoring steps, we can calculate scores using a breadth first search algorithm, which scores each state using the best possible score of any reachable state from the current state.

5. **Informed Search** - We can improve on our search algorithm by expanding possible choices according to some heuristic, possibly something as simple as our previous scoring heuristic, rather than just what we happen to expand first.

### Project Status

| Feature              | Importance | Status       | Goal Date |
|----------------------|------------|--------------|-----------|
| Fitch Recreation     | Required   | In Progress  | 4/1/25    |
| Patterns & Shortcuts | Required   | To Do        | 4/8/25    |
| Step Scoring         | Required   | To Do        | 4/15/25   |
| Look Ahead           | Bonus      | To Do        | 4/22/25   |
| Informed Search      | Reach      | To Do        | 4/22/25   |

### Detailed Progress & Next Steps

#### Fitch Recreation
- [x] Users can enter premises, proof, and conclusion steps
- [x] Users can create subproofs
- [ ] Users can rearrange and delete steps / subproofs
- [ ] Users can apply base rules to statements & cite supporting steps
- [ ] App can validate user input and verify statement syntax
- [ ] App can validate proper application of rules
- [ ] App can validate all rules in succession to verify correctness of a proof

## Setup Instructions
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

### Command Line Interface

> These instructions assume you are on ubuntu which is what I use, @murraycopps maybe you can give windows instructions?

#### User Setup

TBD, if this is not filled out, you can just follow the developer setup instructions.

#### Developer Setup

Go to the `backend` directory and run the following:

On the first time opening the repository, run:

```sh
./scripts/dev_setup.sh      # Run the setup script
source .venv/bin/activate   # Activate the new virtual environment
```

Each time you open the repository, you will need to activate the virtual environment.

To see the help menu for the command line interface, run in your terminal:

```sh
proof_cli -h
```

### Web-App Interface

*Be sure to read both the front-end and back-end instructions*

#### Front End

##### Getting Started

> Again Ubuntu instructions, I will try to go back and add windows

Make sure npm is installed:

```bash
sudo apt update && sudo apt install npm 
```

Install dependencies:
```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

##### Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

##### Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

#### Back end


##### User Setup

TBD, if this is not filled out, you can just follow the developer setup instructions.

##### Developer Setup

Follow the instructions described in the [Command Line](#command-line-interface) section, instead running the server instead of the cli:

```sh
proof_server -h
```