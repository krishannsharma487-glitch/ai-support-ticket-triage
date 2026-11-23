# Workflow Build Guide (Low-code): Google Sheets + Make.com + an LLM

> Tools: Google Sheets (free), Make.com (free plan; check current limits), an LLM with an API key or the built-in AI module (ChatGPT / Claude / Gemini).
> If API access is a problem, use the **fallback**: Google Sheets + Apps Script/"Gemini in Sheets", or a custom GPT/Gem that runs P1+P2 manually per ticket. State honestly in the report which version you built.

## Process flow
New ticket row in Sheet "Inbox" -> Make trigger -> LLM call P1 (classify) -> parse JSON -> Router:
 - confidence >= 0.6 -> LLM call P2 (draft reply) -> write to Sheet "Triage_Output" -> email to the team lead (status: Draft - Needs Approval)
 - confidence < 0.6 OR category = Complaint / Escalation -> flag "Human Review" -> Slack/email alert to Senior Support
Weekly (Monday 9 am schedule) -> read last 7 days -> LLM call P3 -> email summary to manager.

## Step-by-step
1. **Sheet setup.** Create Google Sheet "NovaCart Support Triage" with tabs `Inbox` (columns: ticket_id, created_at, channel, customer_segment, ticket_text), `Triage_Output` (ticket_id, category, priority, sentiment, team, confidence, reason, draft_reply, status, processed_at). Import ~20 rows from `data/synthetic_support_tickets.csv` into Inbox for the demo.
2. **Make scenario.** Sign up at make.com -> Create scenario.
3. **Trigger module:** Google Sheets > "Watch New Rows" (Inbox).
4. **LLM module 1 (classify):** add OpenAI / Anthropic / Gemini "Create a completion" module. Paste prompt P1; map `{ticket_text}`, `{channel}`, `{customer_segment}` from the trigger. Set temperature to 0-0.2.
5. **Parse JSON:** add "JSON > Parse JSON" module on the LLM output.
6. **Router:** two routes. Route A filter: `confidence >= 0.6` AND `category != Complaint / Escalation`. Route B: fallback (everything else).
7. **Route A:** LLM module 2 with prompt P2 (map category, sentiment, ticket_text, segment, and next_step via a "Switch" or a lookup table) -> Google Sheets "Add a Row" to Triage_Output (status = "Draft - Needs Approval") -> Gmail "Send an Email" to the team lead.
8. **Route B:** Sheets "Add a Row" with status = "Human Review" -> email alert to Senior Support (use your own email for demo).
9. **Weekly summary scenario** (optional but recommended for C3): Schedule trigger -> Sheets "Search Rows" -> Text aggregator -> LLM module with P3 -> Gmail.
10. **Test:** run once with 3-5 rows, check each output, fix prompt issues, then run 15-20 rows. Take screenshots: scenario canvas, one execution history, Triage_Output sheet, one email.
11. **Record results** in `results/test_log.md`: ticket_id, expected category (from dataset), AI category, match Y/N, reviewer comment on draft quality. Compute accuracy from YOUR tests only.

## What to demonstrate in the 6-minute presentation
Add one new row live -> show scenario triggering -> show the filled Triage_Output row and the draft email. Keep a recorded screen capture as backup in case of network failure.

## Known limitations to state
Free-tier operation limits, API cost, latency, English-only prompts, no real CRM/helpdesk integration, human approval required.
