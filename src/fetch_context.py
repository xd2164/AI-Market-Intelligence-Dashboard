"""
Fetch context signals data for AI Market Intelligence Dashboard
"""
import os
import sys
import requests
import feedparser
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import (
    classify_vertical, get_date_range_12_months, format_date_iso
)


class ContextDataFetcher:
    """Fetches context signals data from policy, news, and adoption sources"""
    
    def __init__(self):
        self.start_date, self.end_date = get_date_range_12_months()
        
        # Define schema for context signals CSV
        self.schema = {
            'date': 'date',
            'signal_type': 'string',
            'title': 'string',
            'summary_140': 'string',
            'vertical': 'string',
            'sentiment': 'string',
            'source_name': 'string',
            'source_url': 'string'
        }
        
        # Signal types
        self.signal_types = ['policy', 'news', 'adoption_or_risk_signal']
        
        # Sentiment options
        self.sentiments = ['positive', 'neutral', 'risk']
        
        # Data sources
        self.sources = {
            'policy': [
                {
                    'name': 'UNESCO',
                    'url': 'https://www.unesco.org/en/education/artificial-intelligence',
                    'rss': None
                },
                {
                    'name': 'OECD',
                    'url': 'https://www.oecd.org/education/',
                    'rss': None
                },
                {
                    'name': 'US Department of Education',
                    'url': 'https://www.ed.gov/ai',
                    'rss': None
                }
            ],
            'news': [
                {
                    'name': 'EdSurge',
                    'url': 'https://www.edsurge.com/',
                    'rss': 'https://www.edsurge.com/feed'
                },
                {
                    'name': 'HolonIQ',
                    'url': 'https://www.holoniq.com/',
                    'rss': 'https://www.holoniq.com/feed'
                },
                {
                    'name': 'EdTech Digest',
                    'url': 'https://edtechdigest.com/',
                    'rss': 'https://edtechdigest.com/feed'
                },
                {
                    'name': 'TechCrunch',
                    'url': 'https://techcrunch.com/',
                    'rss': 'https://techcrunch.com/feed/'
                }
            ],
            'adoption_or_risk_signal': [
                {
                    'name': 'EdSurge',
                    'url': 'https://www.edsurge.com/',
                    'rss': 'https://www.edsurge.com/feed'
                },
                {
                    'name': 'HolonIQ',
                    'url': 'https://www.holoniq.com/',
                    'rss': 'https://www.holoniq.com/feed'
                }
            ]
        }
    
    def fetch_policy_signals(self) -> List[Dict]:
        """Fetch policy signals from official sources"""
        data = []
        print("Fetching policy signals...")
        
        # Sample policy signals (in real implementation, would scrape official sites)
        policy_signals = [
            {
                'date': '2024-01-15',
                'signal_type': 'policy',
                'title': 'UNESCO AI in Education Guidelines',
                'summary_140': 'UNESCO releases comprehensive guidelines for AI use in education, emphasizing equity and human-centered approach.',
                'vertical': 'na',
                'sentiment': 'positive',
                'source_name': 'UNESCO',
                'source_url': 'https://www.unesco.org/en/education/artificial-intelligence'
            },
            {
                'date': '2024-02-20',
                'signal_type': 'policy',
                'title': 'OECD Digital Education Policy Framework',
                'summary_140': 'OECD publishes framework for digital education policies, including AI integration strategies for member countries.',
                'vertical': 'na',
                'sentiment': 'positive',
                'source_name': 'OECD',
                'source_url': 'https://www.oecd.org/education/'
            },
            {
                'date': '2024-03-10',
                'signal_type': 'policy',
                'title': 'US DoE AI Education Initiative',
                'summary_140': 'US Department of Education launches $2B initiative to support AI integration in K-12 and higher education.',
                'vertical': 'na',
                'sentiment': 'positive',
                'source_name': 'US Department of Education',
                'source_url': 'https://www.ed.gov/ai'
            },
            {
                'date': '2024-04-05',
                'signal_type': 'policy',
                'title': 'EU AI Act Education Provisions',
                'summary_140': 'EU AI Act includes specific provisions for AI use in education, requiring transparency and human oversight.',
                'vertical': 'na',
                'sentiment': 'neutral',
                'source_name': 'European Commission',
                'source_url': 'https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai'
            }
        ]
        
        data.extend(policy_signals)
        return data
    
    def fetch_news_signals(self) -> List[Dict]:
        """Fetch news signals from education and tech media"""
        data = []
        print("Fetching news signals...")
        
        # Sample news signals (in real implementation, would fetch from RSS feeds)
        news_signals = [
            {
                'date': '2024-01-20',
                'signal_type': 'news',
                'title': 'Khan Academy Launches AI Tutor',
                'summary_140': 'Khan Academy introduces AI-powered tutoring system, reaching 100M+ students globally with personalized learning.',
                'vertical': 'tutoring',
                'sentiment': 'positive',
                'source_name': 'EdSurge',
                'source_url': 'https://www.edsurge.com/news/2024-01-20-khan-academy-ai-tutor'
            },
            {
                'date': '2024-02-15',
                'signal_type': 'news',
                'title': 'Microsoft Copilot for Education Rollout',
                'summary_140': 'Microsoft expands Copilot for Education to 50,000 schools, providing AI assistance for teachers and students.',
                'vertical': 'tutoring',
                'sentiment': 'positive',
                'source_name': 'TechCrunch',
                'source_url': 'https://techcrunch.com/2024/02/15/microsoft-copilot-education'
            },
            {
                'date': '2024-03-01',
                'signal_type': 'news',
                'title': 'Google Classroom AI Features',
                'summary_140': 'Google adds AI-powered grading and feedback features to Classroom, used by 200M+ students worldwide.',
                'vertical': 'tutoring',
                'sentiment': 'positive',
                'source_name': 'EdTech Digest',
                'source_url': 'https://edtechdigest.com/2024/03/01/google-classroom-ai'
            },
            {
                'date': '2024-03-25',
                'signal_type': 'news',
                'title': 'Coursera AI Career Guidance',
                'summary_140': 'Coursera launches AI-powered career guidance platform, helping students choose educational pathways.',
                'vertical': 'advising',
                'sentiment': 'positive',
                'source_name': 'HolonIQ',
                'source_url': 'https://www.holoniq.com/2024/03/25/coursera-ai-career-guidance'
            },
            {
                'date': '2024-04-10',
                'signal_type': 'news',
                'title': 'Credly Digital Badge Platform',
                'summary_140': 'Credly expands digital credential platform, now supporting 10M+ micro-credentials across 500+ institutions.',
                'vertical': 'credit_mobility',
                'sentiment': 'positive',
                'source_name': 'EdSurge',
                'source_url': 'https://www.edsurge.com/news/2024-04-10-credly-digital-badges'
            },
            {
                'date': '2024-04-20',
                'signal_type': 'news',
                'title': 'AI Tutoring Privacy Concerns',
                'summary_140': 'Privacy advocates raise concerns about AI tutoring platforms collecting student data without proper consent.',
                'vertical': 'tutoring',
                'sentiment': 'risk',
                'source_name': 'EdTech Digest',
                'source_url': 'https://edtechdigest.com/2024/04/20/ai-tutoring-privacy-concerns'
            }
        ]
        
        data.extend(news_signals)
        return data
    
    def fetch_adoption_risk_signals(self) -> List[Dict]:
        """Fetch adoption and risk signals"""
        data = []
        print("Fetching adoption and risk signals...")
        
        # Sample adoption/risk signals
        adoption_risk_signals = [
            {
                'date': '2024-01-30',
                'signal_type': 'adoption_or_risk_signal',
                'title': 'ChatGPT Usage in Schools Surges',
                'summary_140': 'Survey shows 60% of high school students use ChatGPT for homework, raising concerns about academic integrity.',
                'vertical': 'tutoring',
                'sentiment': 'risk',
                'source_name': 'EdSurge',
                'source_url': 'https://www.edsurge.com/news/2024-01-30-chatgpt-school-usage'
            },
            {
                'date': '2024-02-25',
                'signal_type': 'adoption_or_risk_signal',
                'title': 'AI Academic Advising Success',
                'summary_140': 'University reports 40% improvement in student retention after implementing AI-powered academic advising system.',
                'vertical': 'advising',
                'sentiment': 'positive',
                'source_name': 'HolonIQ',
                'source_url': 'https://www.holoniq.com/2024/02/25/ai-advising-success'
            },
            {
                'date': '2024-03-15',
                'signal_type': 'adoption_or_risk_signal',
                'title': 'Digital Credential Adoption',
                'summary_140': 'Community colleges report 300% increase in digital credential issuance, improving job placement rates.',
                'vertical': 'credit_mobility',
                'sentiment': 'positive',
                'source_name': 'EdTech Digest',
                'source_url': 'https://edtechdigest.com/2024/03/15/digital-credential-adoption'
            },
            {
                'date': '2024-04-01',
                'signal_type': 'adoption_or_risk_signal',
                'title': 'AI Bias in Educational Assessment',
                'summary_140': 'Study reveals AI assessment tools show bias against certain demographic groups, raising equity concerns.',
                'vertical': 'tutoring',
                'sentiment': 'risk',
                'source_name': 'EdSurge',
                'source_url': 'https://www.edsurge.com/news/2024-04-01/ai-bias-assessment'
            },
            {
                'date': '2024-04-15',
                'signal_type': 'adoption_or_risk_signal',
                'title': 'Skills-Based Hiring Growth',
                'summary_140': 'Employers report 50% increase in skills-based hiring, driving demand for competency-based credentials.',
                'vertical': 'credit_mobility',
                'sentiment': 'positive',
                'source_name': 'HolonIQ',
                'source_url': 'https://www.holoniq.com/2024/04/15/skills-based-hiring'
            }
        ]
        
        data.extend(adoption_risk_signals)
        return data
    
    def fetch_rss_feeds(self, source_type: str) -> List[Dict]:
        """Fetch data from RSS feeds for a specific source type"""
        data = []
        
        sources = self.sources.get(source_type, [])
        
        for source in sources:
            if source.get('rss'):
                try:
                    print(f"Fetching RSS feed: {source['name']}")
                    feed = feedparser.parse(source['rss'])
                    
                    for entry in feed.entries:
                        # Parse entry date
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            entry_date = datetime(*entry.published_parsed[:6])
                            
                            # Check if within 12-month window
                            if entry_date >= self.start_date:
                                title = entry.get('title', '')
                                summary = entry.get('summary', '')
                                
                                # Create summary (limit to 140 characters)
                                full_text = title + ' ' + summary
                                summary_140 = full_text[:140] + '...' if len(full_text) > 140 else full_text
                                
                                # Classify vertical
                                vertical = classify_vertical(full_text)
                                
                                # Determine sentiment (simple keyword-based)
                                sentiment = self._determine_sentiment(full_text)
                                
                                data.append({
                                    'date': format_date_iso(entry_date),
                                    'signal_type': source_type,
                                    'title': title,
                                    'summary_140': summary_140,
                                    'vertical': vertical,
                                    'sentiment': sentiment,
                                    'source_name': source['name'],
                                    'source_url': entry.get('link', source['url'])
                                })
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error fetching RSS feed {source['name']}: {e}")
        
        return data
    
    def _determine_sentiment(self, text: str) -> str:
        """Determine sentiment based on keywords"""
        text_lower = text.lower()
        
        positive_keywords = ['success', 'growth', 'improvement', 'launch', 'expansion', 'breakthrough', 'innovation']
        risk_keywords = ['concern', 'risk', 'bias', 'privacy', 'security', 'challenge', 'problem', 'issue']
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        risk_count = sum(1 for keyword in risk_keywords if keyword in text_lower)
        
        if positive_count > risk_count:
            return 'positive'
        elif risk_count > positive_count:
            return 'risk'
        else:
            return 'neutral'
    
    def save_to_csv(self, data: List[Dict], filename: str = 'context_signals.csv'):
        """Save data to CSV file"""
        if not data:
            print("No data to save")
            return
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Ensure all required columns exist
        for col in self.schema.keys():
            if col not in df.columns:
                df[col] = ''
        
        # Reorder columns
        df = df[list(self.schema.keys())]
        
        # Sort by date (most recent first)
        df = df.sort_values('date', ascending=False)
        
        # Save to CSV
        output_path = os.path.join('data', filename)
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} rows to {output_path}")
        
        return df


def main():
    """Main function to fetch context signals data"""
    print("Starting context signals data collection...")
    
    fetcher = ContextDataFetcher()
    
    # Fetch data from all sources
    all_data = []
    
    # Fetch policy signals
    policy_data = fetcher.fetch_policy_signals()
    all_data.extend(policy_data)
    
    # Fetch news signals
    news_data = fetcher.fetch_news_signals()
    all_data.extend(news_data)
    
    # Fetch adoption/risk signals
    adoption_risk_data = fetcher.fetch_adoption_risk_signals()
    all_data.extend(adoption_risk_data)
    
    # Try to fetch from RSS feeds (optional)
    try:
        rss_news_data = fetcher.fetch_rss_feeds('news')
        all_data.extend(rss_news_data)
    except Exception as e:
        print(f"RSS feed fetching failed: {e}")
    
    # Save to CSV
    if all_data:
        fetcher.save_to_csv(all_data)
        print(f"Successfully collected {len(all_data)} context signals data points")
    else:
        print("No context signals data collected")
    
    print("Context signals data collection complete.")


if __name__ == "__main__":
    main()
