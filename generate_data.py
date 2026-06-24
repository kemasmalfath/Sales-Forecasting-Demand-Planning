import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data(file_path="data/sales_data.csv"):
    # Create dir if not exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    np.random.seed(42)
    
    # 2 years of daily data
    days = 730
    start_date = datetime.today() - timedelta(days=days)
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Base sales
    base_sales = 100
    
    # Trend: slightly upward
    trend = np.linspace(0, 50, days)
    
    # Seasonality: Weekly (higher on weekends)
    weekly_seasonality = [20 if d.weekday() >= 5 else 0 for d in dates]
    
    # Seasonality: Yearly (sine wave, peak in summer/winter depending on phase)
    yearly_seasonality = 30 * np.sin(2 * np.pi * np.arange(days) / 365)
    
    # Noise
    noise = np.random.normal(0, 15, days)
    
    # Calculate final sales, ensure no negative values
    sales = base_sales + trend + weekly_seasonality + yearly_seasonality + noise
    sales = np.maximum(sales, 10).astype(int) # At least 10 items sold
    
    df = pd.DataFrame({
        'Date': dates,
        'Sales': sales
    })
    
    # Ensure date only
    df['Date'] = df['Date'].dt.date
    
    df.to_csv(file_path, index=False)
    print(f"Generated {days} days of data at {file_path}")

if __name__ == "__main__":
    generate_sales_data()
