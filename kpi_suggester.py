def suggest_kpis(industry: str) -> list:
    industry_kpis = {
        "E-commerce": [
            "Total Revenue",
            "Average Order Value",
            "Top-selling Products",
            "Return Rate",
            "Customer Lifetime Value", 
            "Monthly Trend",
            "Top Locations"

        ],
        "Finance": [
            "Net Profit",
            "Operating Expenses",
            "Customer Acquisition Cost",
            "Loan Default Rate",
            "Revenue Growth"
        ],
        "Pharmaceuticals": [
            "R&D Spending",
            "Clinical Trial Success Rate",
            "Product Pipeline",
            "Revenue by Drug",
            "Regulatory Approval Timeline"
        ],
        # Add other industries similarly...
    }

    return industry_kpis.get(industry, ["Revenue", "Profit", "Customer Count", "Monthly Trend", "Top Locations"])
