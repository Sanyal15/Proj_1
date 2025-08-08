import pandas as pd
import os

def generate_dashboard(df, kpis=None):
    """
    Generate an Excel dashboard based on selected KPIs.
    """
    kpis = kpis or []
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/dashboard.xlsx"

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        wb = writer.book

        # KPI: Revenue by Category
        if "Revenue" in kpis:
            cat_sum = (
                df.groupby("product_category")["order_value"]
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index()
            )
            cat_sum.to_excel(writer, sheet_name='ByCategory', index=False)
            ws = writer.sheets['ByCategory']
            chart = wb.add_chart({'type': 'column'})
            chart.add_series({
                'name': 'Revenue',
                'categories': ['ByCategory', 1, 0, len(cat_sum), 0],
                'values': ['ByCategory', 1, 1, len(cat_sum), 1],
            })
            chart.set_title({'name': 'Revenue by Product Category'})
            ws.insert_chart('D2', chart)

        # KPI: Profit by Category
        if "Profit" in kpis:
            df["profit"] = df["order_value"] - df["discount_applied"]
            profit_by_cat = (
                df.groupby("product_category")["profit"]
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index()
            )
            profit_by_cat.to_excel(writer, sheet_name='ProfitByCategory', index=False)
            ws = writer.sheets['ProfitByCategory']
            chart = wb.add_chart({'type': 'column'})
            chart.add_series({
                'name': 'Profit',
                'categories': ['ProfitByCategory', 1, 0, len(profit_by_cat), 0],
                'values': ['ProfitByCategory', 1, 1, len(profit_by_cat), 1],
            })
            chart.set_title({'name': 'Profit by Product Category'})
            ws.insert_chart('D2', chart)

        # KPI: Monthly Revenue Trend
        if "Monthly Trend" in kpis:
            df['month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
            mon_sum = (
                df.groupby("month")["order_value"]
                  .sum()
                  .reset_index()
            )
            mon_sum.to_excel(writer, sheet_name='MonthlyTrend', index=False)
            ws = writer.sheets['MonthlyTrend']
            chart = wb.add_chart({'type': 'line'})
            chart.add_series({
                'name': 'Revenue',
                'categories': ['MonthlyTrend', 1, 0, len(mon_sum), 0],
                'values': ['MonthlyTrend', 1, 1, len(mon_sum), 1],
            })
            chart.set_title({'name': 'Monthly Revenue Trend'})
            ws.insert_chart('D2', chart)

        # KPI: Top Locations
        if "Top Locations" in kpis:
            loc_sum = (
                df.groupby("customer_location")["order_value"]
                  .sum()
                  .sort_values(ascending=False)
                  .reset_index()
            )
            loc_sum.to_excel(writer, sheet_name='ByLocation', index=False)
            ws = writer.sheets['ByLocation']
            chart = wb.add_chart({'type': 'bar'})
            chart.add_series({
                'name': 'Revenue',
                'categories': ['ByLocation', 1, 0, len(loc_sum), 0],
                'values': ['ByLocation', 1, 1, len(loc_sum), 1],
            })
            chart.set_title({'name': 'Revenue by Location'})
            ws.insert_chart('D2', chart)

    return output_path
