def generate_insights(df, instruction=None):
    """
    Create a few bullet-point insights based on key metrics.
    """
    insights = []

    # Top category
    top_cat = df.groupby("product_category")["order_value"].sum().idxmax()
    insights.append(f"• 📌 Top product category by revenue: **{top_cat}**")

    # Month-to-month change
    df['month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
    mon = df.groupby("month")["order_value"].sum().sort_index()
    if len(mon) >= 2:
        latest, prev = mon.iloc[-1], mon.iloc[-2]
        pct = (latest - prev) / prev * 100
        insights.append(f"• 🔺 Revenue change last month vs prior: **{pct:.1f}%**")

    # Top location
    top_loc = df.groupby("customer_location")["order_value"].sum().idxmax()
    insights.append(f"• 🗺️ Highest revenue from location: **{top_loc}**")

    # Return rate by category
    ret = (
        df.assign(is_returned=lambda d: d['return_status'].str.lower() == 'yes')
          .groupby("product_category")["is_returned"]
          .mean()
    )
    worst_ret_cat = ret.idxmax()
    rate = ret.max() * 100
    insights.append(f"• ⚠️ Highest return rate in **{worst_ret_cat}** at **{rate:.1f}%**")

    return "\n".join(insights)
