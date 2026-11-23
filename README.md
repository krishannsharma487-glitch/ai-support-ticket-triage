# AI-Enabled Customer Support Ticket Triage and Response Agent
AI for Managers (PMC30022), IILM University, Greater Noida. End Semester Project, 2026.

**Group members and GitHub profiles:** [ADD NAMES AND LINKS]

## Overview
A Generative-AI + low-code automation design that classifies customer-support tickets, drafts replies for human approval, and reports analytics to managers. The company (NovaCart) and all data are **fictional / synthetic**.

## Repository structure
| Folder | Contents |
|---|---|
| `data/` | `synthetic_support_tickets.csv` (400 synthetic tickets) |
| `notebooks/` | `generate_dataset.py`, `analysis.py`, `make_diagram.py` |
| `prompts/` | `prompts.md` (P1 classify, P2 draft reply, P3 weekly summary) |
| `workflow/` | `workflow_guide.md` (Google Sheets + Make.com build steps) |
| `docs/` | `process_diagram.png` |
| `results/` | analysis tables, `charts/`, `scenario_model.csv`, test log |
| `screenshots/` | [ADD: Make scenario, execution history, output sheet, email] |
| `report/` | Final report PDF |

## How to reproduce
```
pip install pandas numpy matplotlib
python notebooks/generate_dataset.py
python notebooks/analysis.py
```
## Notes
- Impact figures in `results/scenario_model.csv` are assumption-based projections, not measured results.
- Replace this README's placeholders before submission.
