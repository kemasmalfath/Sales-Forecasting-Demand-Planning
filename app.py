from flask import Flask, render_template
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # ===== LOAD DATA =====
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, 'data', 'sales_data.csv')
    if not os.path.exists(data_path):
        return "Data tidak ditemukan. Jalankan generate_data.py terlebih dahulu."

    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

    # ===== TRAIN/TEST SPLIT (untuk evaluasi model) =====
    train_size = len(df) - 30
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]

    # ===== TRAIN HOLT-WINTERS MODEL =====
    model = ExponentialSmoothing(
        train['Sales'],
        trend='add',
        seasonal='add',
        seasonal_periods=7,
        initialization_method="estimated"
    )
    fit_model = model.fit()

    # ===== EVALUATE ON TEST SET =====
    test_pred = fit_model.forecast(30)
    mae = mean_absolute_error(test['Sales'], test_pred)
    rmse = np.sqrt(mean_squared_error(test['Sales'], test_pred))
    mape = np.mean(np.abs((test['Sales'].values - test_pred.values) / test['Sales'].values)) * 100

    # ===== RETRAIN ON FULL DATA & FORECAST 30 DAYS =====
    full_model = ExponentialSmoothing(
        df['Sales'],
        trend='add',
        seasonal='add',
        seasonal_periods=7,
        initialization_method="estimated"
    )
    full_fit = full_model.fit()
    forecast_steps = 30
    forecast = full_fit.forecast(forecast_steps)
    forecast = np.maximum(forecast, 0)

    last_date = df['Date'].iloc[-1]
    forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, forecast_steps + 1)]

    # ===== BUSINESS METRICS =====
    total_historical = int(df['Sales'].sum())
    avg_daily = int(df['Sales'].mean())
    total_predicted = int(forecast.sum())
    avg_predicted = int(forecast.mean())

    last_30 = df['Sales'].iloc[-30:]
    last_30_sum = int(last_30.sum())
    trend_pct = ((total_predicted - last_30_sum) / last_30_sum) * 100 if last_30_sum > 0 else 0
    trend_dir = "Naik" if trend_pct > 0 else "Turun"

    # ===== WEEKLY PATTERN =====
    df['DayOfWeek'] = df['Date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_labels = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    weekly_avg = df.groupby('DayOfWeek')['Sales'].mean().reindex(day_order).values.tolist()

    peak_day_idx = int(np.argmax(weekly_avg))
    low_day_idx = int(np.argmin(weekly_avg))

    # ===== MONTHLY TREND =====
    df['YearMonth'] = df['Date'].dt.to_period('M')
    monthly = df.groupby('YearMonth')['Sales'].sum()
    monthly_labels = [str(m) for m in monthly.index]
    monthly_values = monthly.values.tolist()

    best_month = monthly_labels[int(np.argmax(monthly_values))]
    worst_month = monthly_labels[int(np.argmin(monthly_values))]

    # ===== FORECAST PEAK =====
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
    peak_date = forecast_df.loc[forecast_df['Forecast'].idxmax()]['Date']
    peak_value = int(forecast_df['Forecast'].max())

    # ===== PREPARE DATA FOR FRONTEND =====
    # Last 90 days for a cleaner chart view
    recent_df = df.iloc[-90:]

    plot_data = {
        'hist_dates': recent_df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'hist_sales': recent_df['Sales'].tolist(),
        'pred_dates': [d.strftime('%Y-%m-%d') for d in forecast_dates],
        'pred_sales': [round(v, 1) for v in forecast.tolist()],
        'weekly_labels': day_labels,
        'weekly_values': [round(v, 1) for v in weekly_avg],
        'monthly_labels': monthly_labels[-12:],
        'monthly_values': monthly_values[-12:]
    }

    insights = {
        'total_historical': f"{total_historical:,}",
        'avg_daily': f"{avg_daily:,}",
        'total_predicted': f"{total_predicted:,}",
        'avg_predicted': f"{avg_predicted:,}",
        'trend_pct': f"{abs(trend_pct):.1f}",
        'trend_dir': trend_dir,
        'mae': f"{mae:.1f}",
        'rmse': f"{rmse:.1f}",
        'mape': f"{mape:.1f}",
        'peak_day': day_labels[peak_day_idx],
        'low_day': day_labels[low_day_idx],
        'peak_forecast_date': peak_date.strftime('%d %B %Y'),
        'peak_forecast_value': f"{peak_value:,}",
        'best_month': best_month,
        'worst_month': worst_month,
        'data_points': f"{len(df):,}",
        'date_range': f"{df['Date'].iloc[0].strftime('%d %b %Y')} — {df['Date'].iloc[-1].strftime('%d %b %Y')}"
    }

    return render_template('index.html', plot_data=json.dumps(plot_data), insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
