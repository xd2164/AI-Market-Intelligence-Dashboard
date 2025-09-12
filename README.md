# AI Market Intelligence Dashboard v1.0

A comprehensive data collection and analysis system for AI market intelligence across three key verticals: AI-enabled Tutoring, AI-enabled Advising, and AI-enabled Credit Mobility.

## Overview

This project collects and analyzes market data across three dimensions:
- **Market Dynamics (Demand)**: Funding, deals, startups, and user metrics
- **Hyperscaler Metrics (Supply)**: AWS, Microsoft, and Google education initiatives
- **Context Signals**: Policy, news, and adoption/risk signals

## Project Structure

```
AI_Market_Intelligence_Project/
├── src/
│   ├── fetch_market.py          # Market dynamics data collection
│   ├── fetch_hyperscalers.py    # Hyperscaler metrics collection
│   ├── fetch_context.py         # Context signals collection
│   ├── build_workbook.py        # Excel dashboard creation
│   └── utils.py                 # Common utilities and functions
├── data/
│   ├── market_dynamics.csv      # Market dynamics data
│   ├── hyperscaler_metrics.csv  # Hyperscaler metrics data
│   ├── context_signals.csv      # Context signals data
│   └── dashboard_v1.xlsx        # Excel dashboard workbook
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

## Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables (Optional)

Create a `.env` file in the project root with API keys (if available):

```env
CRUNCHBASE_API_KEY=your_crunchbase_api_key_here
HOLONIQ_API_KEY=your_holoniq_api_key_here
```

**Note**: The system works without API keys by using manual data sources and estimates.

## Usage

### Run Individual Data Collection Scripts

1. **Market Dynamics Data**:
   ```bash
   python src/fetch_market.py
   ```

2. **Hyperscaler Metrics Data**:
   ```bash
   python src/fetch_hyperscalers.py
   ```

3. **Context Signals Data**:
   ```bash
   python src/fetch_context.py
   ```

4. **Build Excel Dashboard**:
   ```bash
   python src/build_workbook.py
   ```

### Run Complete Data Collection

To collect all data and build the dashboard in sequence:

```bash
# Run all data collection scripts
python src/fetch_market.py
python src/fetch_hyperscalers.py
python src/fetch_context.py

# Build the Excel dashboard
python src/build_workbook.py
```

## Data Schemas

### Market Dynamics (`market_dynamics.csv`)

| Column | Type | Description |
|--------|------|-------------|
| vertical | string | tutoring/advising/credit_mobility |
| metric | string | funding_total_usd, deals_count, etc. |
| value | float/string | Numeric value where possible |
| unit | string | USD, count, ratio |
| as_of_date | date | ISO YYYY-MM-DD format |
| source_name | string | Data source name |
| source_url | string | Link to source |
| notes | string | Additional notes |

### Hyperscaler Metrics (`hyperscaler_metrics.csv`)

| Column | Type | Description |
|--------|------|-------------|
| hyperscaler | string | aws/microsoft/google |
| vertical | string | tutoring/advising/credit_mobility |
| metric | string | announcements_count, initiatives_new, etc. |
| value | float/string | Numeric value where possible |
| unit | string | count, %, users |
| as_of_date | date | ISO YYYY-MM-DD format |
| cume_estimated | bool | Whether cumulative value is estimated |
| source_name | string | Data source name |
| source_url | string | Link to source |
| notes | string | Additional notes |

### Context Signals (`context_signals.csv`)

| Column | Type | Description |
|--------|------|-------------|
| date | date | ISO YYYY-MM-DD format |
| signal_type | string | policy/news/adoption_or_risk_signal |
| title | string | Signal title/headline |
| summary_140 | string | Summary (≤140 characters) |
| vertical | string | tutoring/advising/credit_mobility/na |
| sentiment | string | positive/neutral/risk |
| source_name | string | Source publisher/organization |
| source_url | string | Link to source |

## Excel Dashboard

The `dashboard_v1.xlsx` workbook contains three sheets:

### 1. Market_Dynamics
- Pivoted view of market metrics by vertical
- Startup churn ratio analysis
- Funding and deal metrics

### 2. Hyperscalers
- Hyperscaler metrics summary table
- Initiative momentum analysis
- User reach estimates

### 3. Context
- Full context signals table
- Top-3 most recent signals by type
- Policy, news, and adoption/risk summaries

## Vertical Classification

The system automatically classifies content into verticals using keyword matching:

- **Tutoring**: tutor, homework, practice, lesson planning, formative feedback, copilot for teachers
- **Advising**: advising, pathways, navigation, program planning, career, student success
- **Credit Mobility**: credential, skills, competency, credit transfer, RPL, micro-credential

## Data Sources

### Market Dynamics
- **Primary**: Crunchbase API, HolonIQ API
- **Fallback**: Manual data from EdSurge, TechCrunch, EdTech Digest

### Hyperscaler Metrics
- **AWS**: AWS Blog RSS, AWS Educate
- **Microsoft**: Microsoft Education Blog, Tech Community
- **Google**: Google Education Blog, Google for Education

### Context Signals
- **Policy**: UNESCO, OECD, US Department of Education
- **News**: EdSurge, HolonIQ, EdTech Digest, TechCrunch
- **Adoption/Risk**: Various education and technology media

## Derived Metrics

The system automatically calculates:

- `avg_deal_size_usd = funding_total_usd / deals_count`
- `startup_churn_ratio = startups_new / max(shutdowns, 1)`
- `initiative_momentum_pct = initiatives_new / max(initiatives_total_cume, 1)`

## Quality Gates

- Every numeric value has a source URL
- Dates are in ISO YYYY-MM-DD format
- No empty vertical or metric fields
- TBD values are marked with notes

## Troubleshooting

### Common Issues

1. **Missing API Keys**: The system works without API keys using manual data sources
2. **Network Errors**: RSS feeds may be temporarily unavailable; the system will continue with available data
3. **Empty Data**: Check that the `data/` directory exists and has write permissions

### Data Validation

- All CSV files are validated for required columns
- Derived metrics are calculated and validated
- Source URLs are verified where possible

## Contributing

To extend the system:

1. Add new data sources in the respective fetch scripts
2. Update vertical classification keywords in `utils.py`
3. Modify schemas if new metrics are added
4. Update the Excel workbook builder for new visualizations

## License

This project is for educational and research purposes. Please respect the terms of service of any APIs or data sources used.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure the `data/` directory exists and is writable
4. Check that Python 3.10+ is being used
