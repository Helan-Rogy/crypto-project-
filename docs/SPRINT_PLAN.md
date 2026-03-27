# Sprint Plan: Sprint 1 (Current)

This document outlines the tasks and goals for the current sprint of the Crypto Investment Manager.

## Sprint Roadmap (2-Week Cycle)
**Current Date**: 2026-03-27
**Sprint Goal**: Finalize the core portfolio tracking and reporting features to make the application fully functional for beta release.

| ID | Title | Task | Assigned To | Effort | Status |
|----|-------|------|-------------|--------|--------|
| T1 | Portfolio UI | Finalize layout and charts for the Portfolio page. | Developer | 5 | In Progress |
| T2 | PDF Reporting | Implement `report_generator.py` for dynamic PDF creation. | Developer | 8 | Completed |
| T3 | Risk Predictor | Integrate `risk_predictor.py` into the Risk Analysis page. | Data Scientist | 13 | In Progress |
| T4 | 2FA Mockup | Create a visual placeholder and logic for 2FA settings. | UI Designer | 3 | Planned |
| T5 | Settings Page | Link user preferences (currency, name) to global state. | Developer | 5 | Planned |

## Core Sprint Tasks

### 1. Finalize Portfolio Charts
- **Task**: Use Plotly for clear, interactive pie and bar charts showing asset distribution.
- **Goal**: Make it easy for users to distinguish between BTC, ETH, and other altcoins.

### 2. Risk Model Verification
- **Task**: Validate the prediction logic in `risk_predictor.py`.
- **Goal**: Ensure that risk scores are accurate and based on real historical data.

### 3. Reporting Logic Integration
- **Task**: Connect the "Reports" page with the backend report generator.
- **Goal**: Users can download a full PDF summary of their current portfolio status.

---
## Review and Retrospective (End of Sprint)
- **Review**: Demo the live application with working charts and PDF downloads.
- **Retrospective**: Identify bottlenecks in data integration and performance optimizations.
