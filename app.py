import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Personal Finance Dashboard", page_icon="💰", layout="wide"
)

st.title("💰 Interactive Personal Finance Dashboard")
st.write(
    "Track your income, categorize your expenses, and monitor your savings effortlessly."
)

# Initialize session state to store transactions
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["Date", "Type", "Category", "Amount", "Description"]
    )

# --- SIDEBAR: Add Transactions ---
st.sidebar.header("Add New Transaction")

with st.sidebar.form("transaction_form", clear_on_submit=True):
    t_date = st.date_input("Date")
    t_type = st.selectbox("Type", ["Income", "Expense"])
    t_category = st.selectbox(
        "Category",
        [
            "Salary",
            "Freelance",
            "Food & Dining",
            "Rent & Housing",
            "Utilities",
            "Entertainment",
            "Shopping",
            "Other",
        ],
    )
    t_amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
    t_desc = st.text_input("Description (Optional)")

    submit_button = st.form_submit_button(label="Add Transaction")

    if submit_button:
        new_data = pd.DataFrame(
            [
                {
                    "Date": t_date,
                    "Type": t_type,
                    "Category": t_category,
                    "Amount": t_amount,
                    "Description": t_desc,
                }
            ]
        )
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, new_data], ignore_index=True
        )
        st.sidebar.success("Transaction added successfully!")

# --- MAIN DASHBOARD ---
df = st.session_state.transactions

if not df.empty:
    # Calculate metrics
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_income - total_expense

    # Display Metrics in Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expense:,.2f}")
    col3.metric(
        "Net Savings",
        f"${net_savings:,.2f}",
        delta=f"${net_savings:,.2f}",
        delta_color="normal" if net_savings >= 0 else "inverse",
    )

    st.markdown("---")

    # Visualizations
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Expenses by Category")
        expense_df = df[df["Type"] == "Expense"]
        if not expense_df.empty:
            category_grouped = expense_df.groupby("Category")[
                "Amount"
            ].sum()
            st.bar_chart(category_grouped)
        else:
            st.info("No expense data available to chart.")

    with col_right:
        st.subheader("📈 Income vs Expenses Over Time")
        time_grouped = df.groupby(["Date", "Type"])["Amount"].sum().unstack().fillna(0)
        st.line_chart(time_grouped)

    # Detailed Table
    st.markdown("---")
    st.subheader("📝 Transaction History")
    st.dataframe(df, use_container_width=True)

    # Clear Data Button
    if st.button("Clear All Data"):
        st.session_state.transactions = pd.DataFrame(
            columns=["Date", "Type", "Category", "Amount", "Description"]
        )
        st.rerun()

else:
    st.info(
        "👈 Use the sidebar to add your first income or expense transaction to get started!"
    )
