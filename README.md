# GemBet Regulatory Analysis

A research and data project examining how gambling regulation affects player protection, using GemBet -- an offshore sportsbook and casino operator -- as a case study. Built as a business analytics project comparing regulated operators (UK, US) against offshore operators (Curacao, Anjouan) across measurable transparency and accountability criteria.

## The question

Do players on offshore betting platforms actually get weaker protections than players on UK/US-regulated platforms, or is that just a reputation? This project treats it as a testable question rather than an assumption.

## Thesis

Operators regulated by bodies with real enforcement power (UK Gambling Commission, US state gaming boards, Gibraltar Gambling Commissioner) are legally required to disclose RTP (Return to Player) figures, submit games for independent testing, and maintain named dispute-resolution channels. Offshore operators licensed in low-barrier jurisdictions face little to no equivalent requirement -- and in at least one case in this dataset (BC.Game), that gap has already caused real, documented financial harm to players.

## What's in this repo

```
├── GemBet_Project_Structure.docx        # Initial project proposal and structure
├── GemBet_Operator_Dataset_CLEANED.xlsx # Full dataset: 7 operators, license info, RTP disclosure, audit status, sources
├── analyze.py                           # Python script that scores each operator and generates the comparison chart
├── regulatory_strength_chart.png        # Output chart comparing all 7 operators
└── GemBet_Final_Report.docx              # Full write-up: methodology, results, case studies, limitations, conclusion
```

## Methodology

Seven operators were researched -- three regulated (Bet365, DraftKings, William Hill) and four offshore (GemBet, Stake, Rollbit, BC.Game). For each, data was manually collected from official site footers/terms pages and cross-checked against third-party sources (regulator public registers, industry news, Slot Tracker for community-sourced RTP estimates).

Each operator was scored 0-3 on:
- **RTP disclosure** (1 point) -- is Return to Player publicly published?
- **Independent audit** (1 point, 0.5 for partial/crypto-based fairness systems) -- is fairness verified by a named third party?
- **Dispute mechanism** (1 point) -- is there a named, external complaints channel?

## Key findings

| Category | Average regulatory strength score (/3) |
|---|---|
| Regulated (Bet365, DraftKings, William Hill) | 2.33 |
| Offshore (GemBet, Stake, Rollbit, BC.Game) | 0.75 |

Bet365 scored a perfect 3.0. GemBet and BC.Game both scored 0.0. BC.Game's case is especially notable: it lost its original Curacao license following bankruptcy proceedings tied to over $2.5 million in unresolved player claims, then obtained an Anjouan license later found to have been issued by a fictitious regulatory body.

Full results, case studies, and discussion are in `GemBet_Final_Report.docx`.

## Running the analysis yourself

```bash
pip install pandas matplotlib openpyxl
python3 analyze.py
```

This reads `GemBet_Operator_Dataset_CLEANED.xlsx`, prints a summary table, and saves `regulatory_strength_chart.png`.

## Limitations

- The regulatory strength score is a simplified, unweighted model (three equally-weighted checks) -- a more rigorous model might weight criteria differently
- Sample size is 7 operators -- a larger sample would strengthen confidence in the category averages
- Data was collected manually from public-facing content rather than pulled systematically from regulator databases
- Some fields (RTP disclosure, payment processor jurisdiction) could not be fully verified for all operators due to geo-blocking from Singapore
