"""
Simple script to create a sample Excel workbook without dependencies
This is a fallback for when Python packages aren't available
"""
import csv
import os

def create_simple_excel_placeholder():
    """Create a simple text representation of what the Excel workbook would contain"""
    
    # Read the CSV data
    market_data = []
    with open('data/market_dynamics.csv', 'r') as f:
        reader = csv.DictReader(f)
        market_data = list(reader)
    
    hyperscaler_data = []
    with open('data/hyperscaler_metrics.csv', 'r') as f:
        reader = csv.DictReader(f)
        hyperscaler_data = list(reader)
    
    context_data = []
    with open('data/context_signals.csv', 'r') as f:
        reader = csv.DictReader(f)
        context_data = list(reader)
    
    # Create a simple text representation
    with open('data/dashboard_v1_preview.txt', 'w') as f:
        f.write("AI MARKET INTELLIGENCE DASHBOARD v1.0\n")
        f.write("=" * 50 + "\n\n")
        
        # Market Dynamics Summary
        f.write("MARKET DYNAMICS SUMMARY\n")
        f.write("-" * 30 + "\n")
        
        # Group by vertical
        verticals = {}
        for row in market_data:
            vertical = row['vertical']
            if vertical not in verticals:
                verticals[vertical] = {}
            verticals[vertical][row['metric']] = row['value']
        
        for vertical, metrics in verticals.items():
            f.write(f"\n{vertical.upper()} VERTICAL:\n")
            f.write(f"  Funding Total: ${metrics.get('funding_total_usd', 'N/A')}\n")
            f.write(f"  Deals Count: {metrics.get('deals_count', 'N/A')}\n")
            f.write(f"  New Startups: {metrics.get('startups_new', 'N/A')}\n")
            f.write(f"  Startup Churn Ratio: {metrics.get('startup_churn_ratio', 'N/A')}\n")
        
        # Hyperscaler Summary
        f.write("\n\nHYPERSCALER METRICS SUMMARY\n")
        f.write("-" * 35 + "\n")
        
        hyperscalers = {}
        for row in hyperscaler_data:
            hyperscaler = row['hyperscaler']
            vertical = row['vertical']
            metric = row['metric']
            value = row['value']
            
            if hyperscaler not in hyperscalers:
                hyperscalers[hyperscaler] = {}
            if vertical not in hyperscalers[hyperscaler]:
                hyperscalers[hyperscaler][vertical] = {}
            hyperscalers[hyperscaler][vertical][metric] = value
        
        for hyperscaler, verticals in hyperscalers.items():
            f.write(f"\n{hyperscaler.upper()}:\n")
            for vertical, metrics in verticals.items():
                f.write(f"  {vertical}: {metrics.get('announcements_count', 0)} announcements, ")
                f.write(f"{metrics.get('initiatives_new', 0)} new initiatives\n")
        
        # Context Signals Summary
        f.write("\n\nCONTEXT SIGNALS SUMMARY\n")
        f.write("-" * 25 + "\n")
        
        signal_types = {}
        for row in context_data:
            signal_type = row['signal_type']
            if signal_type not in signal_types:
                signal_types[signal_type] = []
            signal_types[signal_type].append(row)
        
        for signal_type, signals in signal_types.items():
            f.write(f"\n{signal_type.upper()} SIGNALS (Top 3):\n")
            for signal in signals[:3]:
                f.write(f"  • {signal['title']} ({signal['date']})\n")
                f.write(f"    {signal['summary_140']}\n")
        
        f.write("\n\n" + "=" * 50 + "\n")
        f.write("This is a text preview of the Excel dashboard.\n")
        f.write("Install Python and run the build_workbook.py script\n")
        f.write("to generate the full Excel workbook with charts and formatting.\n")
    
    print("Created dashboard preview at data/dashboard_v1_preview.txt")

if __name__ == "__main__":
    create_simple_excel_placeholder()
