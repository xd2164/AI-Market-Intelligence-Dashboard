# AI Market Intelligence Dashboard - Data Methodology & Rationale

## 📊 Data Computation Rationale

### **Market Dynamics (Demand Side)**

#### **1. Funding Metrics**
- **`funding_total_usd`**: Sum of all funding rounds in each vertical over 12 months
- **`deals_count`**: Number of funding rounds/transactions
- **`avg_deal_size_usd`**: Calculated as `funding_total_usd ÷ deals_count`

**Rationale**: These metrics indicate market demand and investor confidence. Higher funding suggests strong market validation.

#### **2. Startup Metrics**
- **`startups_new`**: Companies founded in the last 12 months
- **`startups_funded`**: Companies that received any funding
- **`shutdowns`**: Companies that ceased operations
- **`startup_churn_ratio`**: Calculated as `startups_new ÷ max(shutdowns, 1)`

**Rationale**: Churn ratio > 1 indicates healthy market growth (more startups than shutdowns).

#### **3. User Adoption Metrics**
- **`users_students`**: Estimated active student users
- **`users_teachers`**: Estimated active teacher users
- **`users_institutions`**: Estimated institutional users

**Rationale**: User metrics indicate market penetration and adoption rates.

### **Hyperscaler Metrics (Supply Side)**

#### **1. Activity Metrics**
- **`announcements_count`**: Education-related announcements from official blogs
- **`initiatives_new`**: New programs/pilots launched in 12 months
- **`initiatives_total_cume`**: Lifetime cumulative initiatives (estimated if unknown)

#### **2. Derived Metrics**
- **`initiative_momentum_pct`**: Calculated as `initiatives_new ÷ max(initiatives_total_cume, 1)`

**Rationale**: Higher momentum indicates accelerating investment in education.

#### **3. Reach Metrics**
- **`user_reach_*`**: Estimated users reached through hyperscaler platforms

### **Context Signals**

#### **1. Signal Classification**
- **`policy`**: Official government/organization policies
- **`news`**: Media coverage and announcements
- **`adoption_or_risk_signal`**: Concrete adoption examples or risk indicators

#### **2. Sentiment Analysis**
- **`positive`**: Growth, success, expansion signals
- **`neutral`**: Factual reporting, policy updates
- **`risk`**: Concerns, challenges, negative impacts

**Rationale**: Sentiment analysis helps identify market sentiment and potential risks.

## 🔍 Data Sources & Validation

### **Primary Sources**
1. **Crunchbase API**: Funding and company data
2. **HolonIQ**: Education market intelligence
3. **Official Blogs**: AWS, Microsoft, Google education blogs
4. **Policy Sources**: UNESCO, OECD, US DoE

### **Fallback Sources**
1. **EdSurge**: Education technology news
2. **TechCrunch**: Technology and startup news
3. **EdTech Digest**: Education technology insights

### **Data Quality Gates**
- Every numeric value has a source URL
- Dates in ISO YYYY-MM-DD format
- No empty vertical or metric fields
- TBD values marked with notes

## 📈 Trend Analysis Methodology

### **Vertical Classification**
Using keyword matching for consistent classification:
- **Tutoring**: tutor, homework, practice, lesson planning, formative feedback
- **Advising**: advising, pathways, navigation, program planning, career
- **Credit Mobility**: credential, skills, competency, credit transfer, RPL

### **Time Series Analysis**
- 12-month lookback period for consistency
- Quarterly trend analysis where possible
- Year-over-year growth calculations

### **Market Maturity Indicators**
- **Early Stage**: High churn ratio, many new startups
- **Growth Stage**: Increasing funding, stable churn
- **Mature Stage**: Lower churn, fewer new startups, higher deal sizes
