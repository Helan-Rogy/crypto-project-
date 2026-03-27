# User Stories: Crypto Investment Manager

This document defines the core product features from the perspective of the end user.

## Epic 1: Secure Portfolio Management
As an investor, I want to securely manage my crypto investments so that I can protect my assets and track their performance over time.

- **Story 1.1: Registration & Login**
  - **As a** new user,
  - **I want to** create a secure account with a strong password policy,
  - **So that** only I can access my private investment data.
  - **Acceptance Criteria**:
    - [ ] Sign-up form with email validation.
    - [ ] Password contains at least 8 characters, one uppercase, one lowercase, one number, and one special character.
    - [ ] Successful login redirects to the main dashboard.

- **Story 1.2: Two-Factor Authentication (2FA)**
  - **As a** security-conscious investor,
  - **I want to** enable 2FA during sign-up,
  - **So that** an extra layer of protection is added to my account.
  - **Acceptance Criteria**:
    - [ ] Checkbox in sign-up for 2FA.
    - [ ] Integrated notification/alert system for logins.

## Epic 2: Real-time Analytics & Dashboard
As a trader, I want to see a holistic view of my portfolio with real-time updates so that I can make informed investment decisions.

- **Story 2.1: Portfolio Dashboard**
  - **As an** investor,
  - **I want to** see my overall portfolio balance and individual asset performance,
  - **So that** I know my current market standing at a glance.
  - **Acceptance Criteria**:
    - [ ] Real-time price updates for top-tier crypto assets.
    - [ ] Portfolio performance charts (e.g., bar or pie charts).

- **Story 2.2: Risk Analysis**
  - **As a** risk-averse trader,
  - **I want to** see a risk score for my current investments,
  - **So that** I can adjust my strategy to minimize potential losses.
  - **Acceptance Criteria**:
    - [ ] Risk predictor module showing asset-specific risk scores.
    - [ ] Historical volatility visualization.

## Epic 3: Reporting & Alerts
As a professional user, I want to generate detailed reports and receive alerts so that I can document my strategy and respond quickly to market events.

- **Story 3.1: Automated Reports**
  - **As a** professional investor,
  - **I want to** generate PDF reports of my portfolio's performance,
  - **So that** I can keep records for long-term planning and tax purposes.
  - **Acceptance Criteria**:
    - [ ] Button on the "Reports" page to generate and download PDFs.
    - [ ] Standardized report format with summary, risk, and portfolio details.

- **Story 3.2: Security Alerts**
  - **As a** user,
  - **I want to** receive an alert when someone logs in to my account,
  - **So that** I can immediately respond if a breach occurs.
  - **Acceptance Criteria**:
    - [ ] Alert system on "Alerts" page showing recent security notifications.
    - [ ] Email notifications for login activity.
