# NovaCart AI Support Ticket Triage — Test Log

## Testing Details
Date tested: 24 November 2026
Workflow: Make.com + OpenAI + JSON Parser + Google Sheets
Tickets evaluated: 20
Evaluation metric: Category classification accuracy

| Ticket ID | Ticket text (short) | Expected category (dataset) | AI category | Match (Y/N) | AI team | Draft reply acceptable? |
|---|---|---|---|---|---|---|
| TK-1001 | Marked delivered, not received | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1002 | Item arrived broken | Damaged / Wrong Item | Damaged / Wrong Item | Y | Logistics | Not evaluated |
| TK-1003 | Refund not received | Refund / Return | Refund / Return | Y | Billing | Not evaluated |
| TK-1004 | Account locked | Account / Login | Account / Login | Y | Tech Support | Not evaluated |
| TK-1005 | Repeated complaint, unresolved | Complaint / Escalation | Complaint / Escalation | Y | Senior Support | Not evaluated |
| TK-1006 | Delivered status, item missing | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1007 | Account locked after failed attempts | Account / Login | Account / Login | Y | Tech Support | Not evaluated |
| TK-1008 | Product suitability question | Product Inquiry | Product Inquiry | Y | General Support | Not evaluated |
| TK-1009 | Incorrect refund amount | Refund / Return | Refund / Return | Y | Billing | Not evaluated |
| TK-1010 | Package delayed for gift | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1011 | Login OTP not received | Account / Login | Account / Login | Y | Tech Support | Not evaluated |
| TK-1012 | Broken item received | Damaged / Wrong Item | Damaged / Wrong Item | Y | Logistics | Not evaluated |
| TK-1013 | Delivered status, item missing | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1014 | Package delayed eight days | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1015 | Product size and restock inquiry | Product Inquiry | Product Inquiry | Y | General Support | Not evaluated |
| TK-1016 | Repeated unresolved complaint | Complaint / Escalation | Complaint / Escalation | Y | Senior Support | Not evaluated |
| TK-1017 | Return link not working | Refund / Return | Refund / Return | Y | Tech Support | Not evaluated |
| TK-1018 | Delivered status, item missing | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1019 | Overdue delivery | Delivery Delay | Delivery Delay | Y | Logistics | Not evaluated |
| TK-1020 | Product suitability question | Product Inquiry | Product Inquiry | Y | General Support | Not evaluated |

## Accuracy Calculation
Correct category predictions: 20
Total tickets tested: 20
Accuracy = (20 / 20) × 100 = 100%

## Observations
All 20 AI-predicted categories matched the original dataset categories. This result applies only to category classification on the evaluated sample. Priority, sentiment, routing quality and draft-reply acceptability were not included in the accuracy calculation.

## Limitations
The test used synthetic customer-support tickets. Performance on real-world messages may differ. Human review is recommended for sensitive or ambiguous cases.
