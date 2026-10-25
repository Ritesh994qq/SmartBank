import streamlit as st
import mysql.connector
import pandas as pd
from decimal import Decimal

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="SmartBank | Banking Management",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS DESIGN
# --------------------------------------------------
st.markdown("""
<style>
/* Overall application */
.stApp {
    background: linear-gradient(135deg, #f4f7fc 0%, #eaf1fa 100%);
    color: #172b4d;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main headings */
h1 {
    color: #102a43 !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2, h3 {
    color: #163b65 !important;
    font-weight: 700 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a43 0%, #123f63 100%);
    border-right: 1px solid #244b6b;
}

section[data-testid="stSidebar"] * {
    color: #f3f8ff;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 8px;
}

section[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 9px 12px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(25, 190, 170, 0.20);
    border-color: #26c6b4;
}

/* Dashboard metrics */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #f7fbff);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #dce7f3;
    box-shadow: 0 5px 20px rgba(16, 42, 67, 0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 25px rgba(16, 42, 67, 0.12);
}

[data-testid="stMetricLabel"] {
    color: #58718c !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #078b8c !important;
    font-weight: 800 !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #087f8c, #0ca89b);
    color: #ffffff !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(8, 127, 140, 0.16);
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #066873, #087f8c);
    transform: translateY(-1px);
    border: none;
}

/* Input fields */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 10px;
    border-color: #d2dfed;
    background-color: #ffffff;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within {
    border-color: #0ca89b;
    box-shadow: 0 0 0 2px rgba(12, 168, 155, 0.12);
}

/* Tables */
[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #dce7f3;
    border-radius: 13px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(16, 42, 67, 0.05);
}

/* Forms */
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #dce7f3;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 6px 24px rgba(16, 42, 67, 0.06);
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Captions and dividers */
.stCaption {
    color: #61758a;
}

hr {
    border-color: #dce7f3;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    [data-testid="stMetric"] {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
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

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.markdown("# 🏦 SmartBank")
st.sidebar.caption("SMART BANKING EXPERIENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
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

st.sidebar.divider()
st.sidebar.caption("Bank Management System")
st.sidebar.caption("MCA Data Science Mini Project")


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------
st.title("🏦 SmartBank")
st.markdown(
    "### Banking made simpler, smarter and more secure."
)
st.caption(
    "Bank Management System  |  MCA Mini Project"
)
st.divider()


# --------------------------------------------------
# FETCH DATABASE DATA
# --------------------------------------------------
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
        JOIN customers c
          ON a.customer_id = c.customer_id
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


    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------
    if page == "Dashboard":

        st.subheader("📊 Banking Overview")
        st.caption("A quick summary of your banking database.")

        total_balance = (
            accounts["balance"].sum()
            if not accounts.empty else 0
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "👥 Total Customers",
            f"{len(customers):,}"
        )

        c2.metric(
            "💳 Total Accounts",
            f"{len(accounts):,}"
        )

        c3.metric(
            "💰 Total Balance",
            f"₹{total_balance:,.2f}"
        )

        st.divider()

        st.subheader("💳 Account Summary")

        if accounts.empty:
            st.info("No accounts are available yet.")
        else:
            st.dataframe(
                accounts,
                width="stretch",
                hide_index=True
            )

        st.subheader("🔄 Recent Transactions")

        if transactions.empty:
            st.info("No transactions are available yet.")
        else:
            st.dataframe(
                transactions.head(10),
                width="stretch",
                hide_index=True
            )

        if not accounts.empty:
            st.subheader("📈 Account Balance Chart")
            chart_data = accounts.set_index(
                "account_no"
            )["balance"]

            st.bar_chart(chart_data)

        st.caption(
            "SmartBank | Your banking information at a glance."
        )


    # --------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------
    elif page == "Customers":

        st.subheader("👥 Customer Directory")
        st.caption("View registered customers.")

        st.metric("Registered Customers", len(customers))

        if customers.empty:
            st.info("No customers found.")
        else:
            st.dataframe(
                customers,
                width="stretch",
                hide_index=True
            )


    # --------------------------------------------------
    # ACCOUNTS
    # --------------------------------------------------
    elif page == "Accounts":

        st.subheader("💳 Account Management")
        st.caption("Review account details and available balances.")

        if accounts.empty:
            st.info("No accounts are available.")
        else:
            st.dataframe(
                accounts,
                width="stretch",
                hide_index=True
            )

            st.divider()
            st.markdown("#### 🔎 Check Account Balance")

            account_no = st.selectbox(
                "Select account number",
                account_numbers
            )

            if st.button("Check Balance", use_container_width=False):
                row = accounts[
                    accounts["account_no"] == account_no
                ].iloc[0]

                st.metric(
                    f"Available Balance — Account {account_no}",
                    f"₹{row['balance']:,.2f}"
                )


    # --------------------------------------------------
    # DEPOSIT AND WITHDRAW
    # --------------------------------------------------
    elif page in ["Deposit", "Withdraw"]:

        if page == "Deposit":
            st.subheader("💵 Deposit Money")
            st.caption("Add funds to a selected account.")
        else:
            st.subheader("💸 Withdraw Money")
            st.caption("Withdraw funds from a selected account.")

        if not account_numbers:
            st.warning(
                "No accounts are available for transactions."
            )
        else:
            with st.form("money_form"):
                account_no = st.selectbox(
                    "Select account number",
                    account_numbers
                )

                amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.01,
                    max_value=10000000.00,
                    value=100.00,
                    step=100.00
                )

                submitted = st.form_submit_button(
                    f"Confirm {page}",
                    use_container_width=True
                )

            if submitted:
                try:
                    procedure = (
                        "deposit_money"
                        if page == "Deposit"
                        else "withdraw_money"
                    )

                    call_procedure(
                        procedure,
                        (
                            int(account_no),
                            Decimal(str(amount))
                        )
                    )

                    st.success(f"{page} successful!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Transaction failed: {e}")


    # --------------------------------------------------
    # TRANSFER FUNDS
    # --------------------------------------------------
    elif page == "Transfer":

        st.subheader("🔁 Transfer Funds")
        st.caption(
            "Transfer money between two different accounts."
        )

        if len(account_numbers) < 2:
            st.warning(
                "At least two accounts are required for a transfer."
            )
        else:
            with st.form("transfer_form"):

                from_account = st.selectbox(
                    "From account",
                    account_numbers
                )

                to_options = [
                    a for a in account_numbers
                    if a != from_account
                ]

                to_account = st.selectbox(
                    "To account",
                    to_options
                )

                amount = st.number_input(
                    "Transfer amount (₹)",
                    min_value=0.01,
                    max_value=10000000.00,
                    value=100.00,
                    step=100.00
                )

                submitted = st.form_submit_button(
                    "Confirm Transfer",
                    use_container_width=True
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


    # --------------------------------------------------
    # TRANSACTION HISTORY
    # --------------------------------------------------
    elif page == "Transactions":

        st.subheader("📋 Transaction History")
        st.caption(
            "Review and filter the recorded transactions."
        )

        if transactions.empty:
            st.info("No transactions are available yet.")
        else:
            types = ["All"] + sorted(
                transactions["transaction_type"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_type = st.selectbox(
                "Filter by transaction type",
                types
            )

            filtered_transactions = transactions.copy()

            if selected_type != "All":
                filtered_transactions = (
                    filtered_transactions[
                        filtered_transactions["transaction_type"]
                        == selected_type
                    ]
                )

            st.metric(
                "Transactions Displayed",
                f"{len(filtered_transactions):,}"
            )

            st.dataframe(
                filtered_transactions,
                width="stretch",
                hide_index=True
            )

            st.download_button(
                "⬇️ Download CSV Report",
                filtered_transactions.to_csv(
                    index=False
                ).encode("utf-8"),
                "smartbank_transactions.csv",
                "text/csv",
                use_container_width=True
            )


# --------------------------------------------------
# ERROR HANDLING
# --------------------------------------------------
except Exception as e:

    st.error("Could not load SmartBank.")
    st.code(str(e))

    st.info(
        "Check your MySQL connection, database tables, "
        "stored procedures, and Streamlit secrets."
    )
