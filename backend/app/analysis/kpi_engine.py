import pandas as pd
from typing import Dict, Any, List
from app.analysis.utils import get_columns_by_type

def calculate_kpis(df: pd.DataFrame, dataset_type: str, column_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a semantic dictionary of key business metrics based on the dataset domain category.
    """
    kpis = {}
    
    # Extract columns categorized by features
    numeric_cols = get_columns_by_type(column_metadata, "is_numeric")
    currency_cols = get_columns_by_type(column_metadata, "is_currency")
    categorical_cols = get_columns_by_type(column_metadata, "is_categorical")
    id_cols = get_columns_by_type(column_metadata, "is_primary_key")
    
    print("KPI ENGINE COLUMNS:")
    print("  numeric_cols:", numeric_cols)
    print("  currency_cols:", currency_cols)
    print("  categorical_cols:", categorical_cols)
    print("  id_cols:", id_cols)
    
    # Helper: Find first matching column name containing any of the keywords
    def find_col(keywords: List[str], pool: List[str]) -> Optional[str]:
        for col in pool:
            col_lower = str(col).lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None

    if dataset_type == "Sales":
        # 1. Total Revenue
        rev_col = find_col(["revenue", "sales_amount", "sales", "revenue_usd", "amount", "total"], currency_cols + numeric_cols)
        total_revenue = float(df[rev_col].sum()) if rev_col else 0.0
        
        # 2. Total Orders / Transactions
        order_col = find_col(["order_id", "transaction_id", "sales_id", "id"], id_cols + numeric_cols + categorical_cols)
        total_orders = int(df[order_col].nunique()) if order_col else len(df)
        
        # 3. Average Order Value
        aov = total_revenue / total_orders if total_orders > 0 else 0.0
        
        # 4. Profit & Profit Margin
        profit_col = find_col(["profit", "margin", "gain"], currency_cols + numeric_cols)
        cost_col = find_col(["cost", "expense", "spent"], currency_cols + numeric_cols)
        
        if profit_col:
            total_profit = float(df[profit_col].sum())
        elif rev_col and cost_col:
            total_profit = float((df[rev_col] - df[cost_col]).sum())
        else:
            # Fallback to estimate: 20% margin
            total_profit = total_revenue * 0.20
            
        profit_margin = (total_profit / total_revenue) * 100.0 if total_revenue > 0 else 0.0
        
        # 5. Total Customers
        cust_col = find_col(["customer_id", "customer_name", "customer", "client", "user_id"], numeric_cols + categorical_cols + id_cols)
        total_customers = int(df[cust_col].nunique()) if cust_col else 0
        
        kpis = {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "average_order_value": round(aov, 2),
            "total_profit": round(total_profit, 2),
            "profit_margin": round(profit_margin, 1),
            "total_customers": total_customers
        }
        
    elif dataset_type == "HR":
        # 1. Total Headcount
        emp_col = find_col(["employee_id", "employee_name", "id", "staff_id"], numeric_cols + categorical_cols + id_cols)
        headcount = int(df[emp_col].nunique()) if emp_col else len(df)
        
        # 2. Average Salary
        salary_col = find_col(["salary", "pay", "wage", "compensation"], currency_cols + numeric_cols)
        avg_salary = float(df[salary_col].mean()) if salary_col else 0.0
        
        # 3. Attrition Rate
        attrition_col = find_col(["attrition", "status", "terminated", "active"], categorical_cols)
        attrition_rate = 0.0
        if attrition_col:
            # Check if values contain 'yes' or 'terminated' or 'exit'
            vals = df[attrition_col].astype(str).str.lower()
            terminated_count = int(vals.str.contains("yes|terminated|exit|left|inactive").sum())
            attrition_rate = (terminated_count / len(df)) * 100.0
            
        kpis = {
            "employee_count": headcount,
            "average_salary": round(avg_salary, 2),
            "attrition_rate": round(attrition_rate, 1)
        }
        
    elif dataset_type == "Finance":
        # 1. Income
        income_col = find_col(["income", "revenue", "receipt", "credit"], currency_cols + numeric_cols)
        total_income = float(df[income_col].sum()) if income_col else 0.0
        
        # 2. Expense
        expense_col = find_col(["expense", "cost", "spending", "debit"], currency_cols + numeric_cols)
        total_expense = float(df[expense_col].sum()) if expense_col else 0.0
        
        # 3. Net Profit
        net_profit = total_income - total_expense
        profit_margin = (net_profit / total_income) * 100.0 if total_income > 0 else 0.0
        
        kpis = {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_profit": round(net_profit, 2),
            "profit_margin": round(profit_margin, 1)
        }
        
    else:
        # Generic Spreadsheet KPIs
        # Calculate sum of largest numeric column as "Total Sum", and counts
        total_sum = 0.0
        avg_value = 0.0
        largest_num_col = None
        
        if numeric_cols:
            # Find numeric col with largest sum
            largest_sum = -1.0
            for col in numeric_cols:
                # Ignore ID columns
                if col in id_cols or "id" in str(col).lower():
                    continue
                col_sum = float(df[col].sum())
                if col_sum > largest_sum:
                    largest_sum = col_sum
                    largest_num_col = col
            
            if largest_num_col:
                total_sum = largest_sum
                avg_value = float(df[largest_num_col].mean())
                
        kpis = {
            "total_records": len(df),
            "columns_count": len(df.columns),
            "primary_metric": largest_num_col or "None",
            "sum_value": round(total_sum, 2),
            "average_value": round(avg_value, 2)
        }
        
    return kpis

# Optional import helper since FastAPI parameters Form might yield None
from typing import Optional
