# BettyAnn Chodkowski

Most of my repositories are private, so the contribution graph shows activity you can't click into. This page says what that work is.

I build data and ML pipelines in Python, mostly on Apple Silicon with local models (MLX). I also build the tooling that lets coding agents work in a repo safely: rules, hooks, and review steps that keep the agent inside clear limits.

---

## Projects

### Machine learning and data

**mGlu7 cross-subtype activity** · Python, scikit-learn, RDKit, ChEMBL
Does training on data-rich receptor subtypes improve potency prediction for a data-poor one? The mGlu7 receptor has few measured compounds; its relatives (mGlu2, 4, 5) have many. The pipeline builds labels from ChEMBL, splits compounds by chemical similarity so no near-copy of a test compound sits in training, and scores models against three simple baselines. A permutation test sets the noise floor a difference must clear before it counts. Figures and the write-up are generated from the result files, so a plot can't disagree with its number.

**NPI match** · Python, DuckDB · *in progress*
A matching and recommendation engine over the public NPPES physician registry. A physician's profile goes in; ten practice locations with reasons come out. The data has no record of which match a physician chose, so the score is a stand-in: hide one place a physician already practices and count how often it comes back in the top ten (recall@10). Covers entity resolution (block, score, group), ranking, and how each is measured.

**Refine Resume** · Python, MLX, RenderCV, pytest
Tailors a resume and cover letter to one job posting. A local model drafts; Python selects, checks, and renders. Every claim in a letter is traced to a source, and unsupported claims are flagged or removed. An ATS check and a consistency review run before anything is sent. A human approves every change that flows back into the base CV.

**Daily Brief** · Python, uv, launchd, MCP · *early stage*
A personal news brief built by a local model and delivered before 6am with no one at the keyboard. Planned: RSS fetch, per-article summaries, synthesis, embedding-based dedup over a SQLite archive, and an MCP server so the archive can be queried in plain language.

### Web

**AT Trekker** · Node.js, Leaflet, SQLite
An interactive Appalachian Trail map. Live position from Garmin MapShare, GPX upload, destination planning, and pace-adjusted time estimates. A separate poller fetches the Garmin feed on a timer, with retry and backoff, into the same database the web server reads.

**National Autism Peer Support website** · Python, WordPress REST API
The site for a non-profit and its local affiliates. Page copy and design tokens live in the repo and are published to WordPress.com over its REST API, never edited by hand. Built on the stock theme with no plugins, so the client can maintain it alone.

### Hardware and home lab

**Squirrel Sentry** · Python · *design stage*
A motion-triggered, non-lethal deterrent for squirrels in an attic. Randomized light and sound so the animals don't get used to it, plus a log that measures when they leave. Design limits, in order: no fire, no harm to the animals, no harm to the household.

**NAS from Macs** · Python, launchd, MLX
A home backup plan (Time Machine plus rsync to a ZFS mirror on a Linux box), hardware selection, a GPU stress test for Apple Silicon, and launchd jobs that track used-Mac prices.

### Public

**[ba-toolbox](https://github.com/BA88/ba-toolbox)** · Bash
Shell utilities, including a wrapper for the Claude Code CLI that sets a session name and terminal color on every launch.

---

## How I work with coding agents

Every project above shares one setup for working with Claude Code:

- **Rules** that load only when relevant: coding standards, testing, security, git workflow.
- **Hooks** that block unsafe actions before they run: git mutations by the agent, writes to protected paths, non-literal shell commands.
- **A ticket board** in `docs/TODO.md`, rendered to an HTML Kanban page and checked for drift.
- **A plan-then-implement loop**: one ticket step at a time, a branch review, and a human commit.

The agent writes code. I own the decisions and every commit.

---

## Tools

Python · uv · ruff · pytest · pandas · scikit-learn · RDKit · MLX · SQLite · DuckDB · Node.js · Bash · launchd · Claude Code · MCP
