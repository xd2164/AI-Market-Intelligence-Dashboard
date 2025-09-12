"""
Utility functions for AI Market Intelligence Dashboard
"""
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd


# Vertical classification keywords
VERTICAL_KEYWORDS = {
    'tutoring': [
        'tutor', 'homework', 'practice', 'lesson planning', 'formative feedback',
        'copilot for teachers', 'adaptive instruction', 'personalized learning',
        'study help', 'academic support', 'learning assistance'
    ],
    'advising': [
        'advising', 'pathways', 'navigation', 'program planning', 'career',
        'student success', 'enrollment guidance', 'course selection',
        'academic advising', 'career guidance', 'student support'
    ],
    'credit_mobility': [
        'credential', 'skills', 'competency', 'credit transfer', 'RPL',
        'micro-credential', 'badging', 'skills taxonomy', 'prior learning',
        'competency-based', 'alternative credentials'
    ]
}


def classify_vertical(text: str) -> str:
    """
    Classify text into one of the three verticals based on keyword matching.
    
    Args:
        text: Text to classify
        
    Returns:
        Vertical classification: 'tutoring', 'advising', 'credit_mobility', or 'na'
    """
    if not text:
        return 'na'
    
    text_lower = text.lower()
    scores = {}
    
    for vertical, keywords in VERTICAL_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[vertical] = score
    
    # Return the vertical with the highest score, or 'na' if no matches
    if not any(scores.values()):
        return 'na'
    
    return max(scores, key=scores.get)


def get_date_range_12_months() -> Tuple[datetime, datetime]:
    """
    Get start and end dates for 12-month lookback period.
    
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    return start_date, end_date


def format_date_iso(date_obj) -> str:
    """
    Format date object to ISO YYYY-MM-DD string.
    
    Args:
        date_obj: datetime object or string
        
    Returns:
        ISO formatted date string
    """
    if isinstance(date_obj, str):
        try:
            date_obj = pd.to_datetime(date_obj)
        except:
            return ""
    
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime('%Y-%m-%d')
    
    return ""


def clean_numeric_value(value) -> Optional[float]:
    """
    Clean and convert value to numeric.
    
    Args:
        value: Value to clean
        
    Returns:
        Cleaned numeric value or None
    """
    if pd.isna(value) or value == "":
        return None
    
    if isinstance(value, (int, float)):
        return float(value)
    
    # Remove common non-numeric characters
    if isinstance(value, str):
        cleaned = re.sub(r'[^\d.,-]', '', value)
        cleaned = cleaned.replace(',', '')
        
        try:
            return float(cleaned)
        except ValueError:
            return None
    
    return None


def get_env_var(var_name: str, default: str = "") -> str:
    """
    Get environment variable with fallback to default.
    
    Args:
        var_name: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(var_name, default)


def create_dataframe_with_schema(schema: Dict[str, str]) -> pd.DataFrame:
    """
    Create empty DataFrame with specified schema.
    
    Args:
        schema: Dictionary mapping column names to data types
        
    Returns:
        Empty DataFrame with specified columns and types
    """
    df = pd.DataFrame(columns=list(schema.keys()))
    
    # Set data types
    for col, dtype in schema.items():
        if dtype == 'date':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif dtype == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif dtype == 'bool':
            df[col] = df[col].astype('boolean')
    
    return df


def validate_row_data(row_data: Dict, required_fields: List[str]) -> bool:
    """
    Validate that row data contains all required fields.
    
    Args:
        row_data: Dictionary of row data
        required_fields: List of required field names
        
    Returns:
        True if all required fields are present and non-empty
    """
    for field in required_fields:
        if field not in row_data or not row_data[field]:
            return False
    return True


def extract_user_metrics(text: str) -> Dict[str, Optional[int]]:
    """
    Extract user metrics (students, teachers, institutions) from text.
    
    Args:
        text: Text to search for user metrics
        
    Returns:
        Dictionary with extracted metrics
    """
    metrics = {
        'students': None,
        'teachers': None,
        'institutions': None
    }
    
    if not text:
        return metrics
    
    text_lower = text.lower()
    
    # Patterns to match user counts
    patterns = {
        'students': [r'(\d+(?:,\d+)*)\s*students?', r'(\d+(?:,\d+)*)\s*pupils?'],
        'teachers': [r'(\d+(?:,\d+)*)\s*teachers?', r'(\d+(?:,\d+)*)\s*educators?'],
        'institutions': [r'(\d+(?:,\d+)*)\s*schools?', r'(\d+(?:,\d+)*)\s*institutions?', r'(\d+(?:,\d+)*)\s*universities?']
    }
    
    for metric, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    value = int(match.group(1).replace(',', ''))
                    metrics[metric] = value
                    break
                except ValueError:
                    continue
    
    return metrics


def calculate_derived_metrics(data: pd.DataFrame, metric_type: str) -> pd.DataFrame:
    """
    Calculate derived metrics based on the metric type.
    
    Args:
        data: DataFrame with base metrics
        metric_type: Type of metrics ('market_dynamics' or 'hyperscaler')
        
    Returns:
        DataFrame with derived metrics added
    """
    if metric_type == 'market_dynamics':
        # Calculate avg_deal_size_usd
        funding_data = data[data['metric'] == 'funding_total_usd']
        deals_data = data[data['metric'] == 'deals_count']
        
        for vertical in ['tutoring', 'advising', 'credit_mobility']:
            funding = funding_data[funding_data['vertical'] == vertical]['value'].iloc[0] if len(funding_data[funding_data['vertical'] == vertical]) > 0 else 0
            deals = deals_data[deals_data['vertical'] == vertical]['value'].iloc[0] if len(deals_data[deals_data['vertical'] == vertical]) > 0 else 0
            
            if deals and deals > 0:
                avg_deal_size = funding / deals
                new_row = {
                    'vertical': vertical,
                    'metric': 'avg_deal_size_usd',
                    'value': avg_deal_size,
                    'unit': 'USD',
                    'as_of_date': datetime.now().strftime('%Y-%m-%d'),
                    'source_name': 'calculated',
                    'source_url': '',
                    'notes': f'Calculated from funding_total_usd / deals_count'
                }
                data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        
        # Calculate startup_churn_ratio
        startups_new_data = data[data['metric'] == 'startups_new']
        shutdowns_data = data[data['metric'] == 'shutdowns']
        
        for vertical in ['tutoring', 'advising', 'credit_mobility']:
            startups_new = startups_new_data[startups_new_data['vertical'] == vertical]['value'].iloc[0] if len(startups_new_data[startups_new_data['vertical'] == vertical]) > 0 else 0
            shutdowns = shutdowns_data[shutdowns_data['vertical'] == vertical]['value'].iloc[0] if len(shutdowns_data[shutdowns_data['vertical'] == vertical]) > 0 else 0
            
            churn_ratio = startups_new / max(shutdowns, 1)
            new_row = {
                'vertical': vertical,
                'metric': 'startup_churn_ratio',
                'value': churn_ratio,
                'unit': 'ratio',
                'as_of_date': datetime.now().strftime('%Y-%m-%d'),
                'source_name': 'calculated',
                'source_url': '',
                'notes': f'Calculated from startups_new / max(shutdowns, 1)'
            }
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    
    elif metric_type == 'hyperscaler':
        # Calculate initiative_momentum_pct
        initiatives_new_data = data[data['metric'] == 'initiatives_new']
        initiatives_cume_data = data[data['metric'] == 'initiatives_total_cume']
        
        for hyperscaler in ['aws', 'microsoft', 'google']:
            for vertical in ['tutoring', 'advising', 'credit_mobility']:
                new_initiatives = initiatives_new_data[
                    (initiatives_new_data['hyperscaler'] == hyperscaler) & 
                    (initiatives_new_data['vertical'] == vertical)
                ]['value'].iloc[0] if len(initiatives_new_data[
                    (initiatives_new_data['hyperscaler'] == hyperscaler) & 
                    (initiatives_new_data['vertical'] == vertical)
                ]) > 0 else 0
                
                cume_initiatives = initiatives_cume_data[
                    (initiatives_cume_data['hyperscaler'] == hyperscaler) & 
                    (initiatives_cume_data['vertical'] == vertical)
                ]['value'].iloc[0] if len(initiatives_cume_data[
                    (initiatives_cume_data['hyperscaler'] == hyperscaler) & 
                    (initiatives_cume_data['vertical'] == vertical)
                ]) > 0 else 0
                
                momentum_pct = new_initiatives / max(cume_initiatives, 1)
                new_row = {
                    'hyperscaler': hyperscaler,
                    'vertical': vertical,
                    'metric': 'initiative_momentum_pct',
                    'value': momentum_pct,
                    'unit': '%',
                    'as_of_date': datetime.now().strftime('%Y-%m-%d'),
                    'cume_estimated': False,
                    'source_name': 'calculated',
                    'source_url': '',
                    'notes': f'Calculated from initiatives_new / max(initiatives_total_cume, 1)'
                }
                data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    
    return data
