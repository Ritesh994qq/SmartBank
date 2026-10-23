
import streamlit as st
import mysql.connector
import pandas as pd
from decimal import Decimal

st.set_page_config(
    page_title="SmartBank",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f2f6fc;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #dbe5f0;
}
</style>
""", unsafe_allow_html=True)


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


def read_data(sql):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    finally:
        conn.close()


def call_procedure(name, values):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(name, values)
        for result in cursor.stored_results():
            result.fetchall()
    finally:
        cursor.close()
        conn.close()


st.sidebar.title("🏦 SmartBank")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customers",
        "Accounts",
        "Transactions",
        "Deposit",
        "Withdraw",
        "Transfer"
    ]
)

st.title("🏦 SmartBank")
st.caption("Bank Management System | MCA Mini Project")

try:
    customers = read_data("""
        SELECT customer_id, customer_name, phone
        FROM customers
        ORDER BY customer_id
    """)

    accounts = read_data("""
        SELECT a.account_no, c.customer_name,
               a.account_type, a.balance
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY a.account_no
    """)

    transactions = read_data("""
        SELECT transaction_id, account_no,
               transaction_type, amount,
               transaction_date, remarks
        FROM transactions
        ORDER BY transaction_id DESC
    """)

    account_numbers = accounts["account_no"].tolist()

    if page == "Dashboard":
        st.subheader("Banking Overview")

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Customers", len(customers))
        c2.metric("Total Accounts", len(accounts))
        c3.metric(
            "Total Balance",
            f"₹{accounts['balance'].sum():,.2f}"
        )

        st.subheader("Account Summary")
        st.dataframe(accounts, width="stretch",
                     hide_index=True)

        st.subheader("Recent Transactions")
        st.dataframe(transactions.head(10),
                     width="stretch", hide_index=True)

        if not accounts.empty:
            st.subheader("Account Balance Chart")
            st.bar_chart(
                accounts.set_index("account_no")["balance"]
            )

    elif page == "Customers":
        st.subheader("Customer Directory")
        st.dataframe(customers, width="stretch",
                     hide_index=True)

    elif page == "Accounts":
        st.subheader("Account Management")
        st.dataframe(accounts, width="stretch",
                     hide_index=True)

        if account_numbers:
            account_no = st.selectbox(
                "Select account",
                account_numbers
            )
            if st.button("Check Balance"):
                row = accounts[
                    accounts["account_no"] == account_no
                ].iloc[0]
                st.metric(
                    f"Balance: Account {account_no}",
                    f"₹{row['balance']:,.2f}"
                )

    elif page in ["Deposit", "Withdraw"]:
        st.subheader(f"{page} Money")

        if not account_numbers:
            st.warning("Create an account before transacting.")
        else:
            with st.form("money_form"):
                account_no = st.selectbox(
                    "Account number", account_numbers
                )
                amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.01,
                    max_value=10000000.00,
                    value=100.00,
                    step=100.00
                )
                submitted = st.form_submit_button(
                    f"Confirm {page}"
                )

            if submitted:
                try:
                    procedure = (
                        "deposit_money" if page == "Deposit"
                        else "withdraw_money"
                    )
                    call_procedure(
                        procedure,
                        (int(account_no), Decimal(str(amount)))
                    )
                    st.success(f"{page} successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Transaction failed: {e}")

    elif page == "Transfer":
        st.subheader("Transfer Funds")

        if len(account_numbers) < 2:
            st.warning("At least two accounts are required.")
        else:
            with st.form("transfer_form"):
                from_account = st.selectbox(
                    "From account", account_numbers
                )
                to_options = [
                    a for a in account_numbers
                    if a != from_account
                ]
                to_account = st.selectbox(
                    "To account", to_options
                )
                amount = st.number_input(
                    "Transfer amount (₹)",
                    min_value=0.01,
                    max_value=10000000.00,
                    value=100.00,
                    step=100.00
                )
                submitted = st.form_submit_button(
                    "Confirm Transfer"
                )

            if submitted:
                try:
                    call_procedure(
                        "transfer_funds",
                        (
                            int(from_account),
                            int(to_account),
                            Decimal(str(amount))
                        )
                    )
                    st.success("Transfer successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Transfer failed: {e}")

    elif page == "Transactions":
        st.subheader("Transaction History")

        if not transactions.empty:
            types = ["All"] + sorted(
                transactions["transaction_type"].dropna().unique()
            )
            selected_type = st.selectbox(
                "Filter by transaction type", types
            )

            if selected_type != "All":
                transactions = transactions[
                    transactions["transaction_type"] == selected_type
                ]

        st.dataframe(transactions, width="stretch",
                     hide_index=True)

        st.download_button(
            "Download CSV Report",
            transactions.to_csv(index=False).encode("utf-8"),
            "smartbank_transactions.csv",
            "text/csv"
        )

except Exception as e:
    st.error("Could not load SmartBank.")
    st.code(str(e))
    st.info(
        "Check your MySQL connection, database tables, "
        "stored procedures, and secrets.toml."
    )
