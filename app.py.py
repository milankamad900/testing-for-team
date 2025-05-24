import streamlit as st
import pandas as pd

# ✅ Page configuration must be first
st.set_page_config(page_title="Invoice and PO Lookup", layout="wide")

# Load data once
@st.cache_data
def load_data():
    file_path = "C:/Users/Milan/Downloads/Bill Payment File.xlsx"
    sheet_name = "BillsandRelatedBillPaymentsTSL"
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    rename_map = {
        'Document Number': 'Invoice',
        'Subsidiary (no hierarchy)': 'Subsidiary',
        'Name': 'Name',
        'Date': 'Date',
        'Type': 'Type',
        'Status': 'Status',
        'Amount': 'Amount',
        'Amount (Foreign Currency)': 'Canada Amt',
        'Payment Hold': 'Payment Hold',
        'Vendor Bill Date': 'Vendor Bill Date',
        'Received Bill Date': 'Received Bill Date',
        'Due Date/Receive By': 'Due Date',
        'Created By 810 EDI Script': 'EDI',
        'Added by ShortPay': 'Accurate Pay',
        'Location': 'Location',
        'Created By': 'Created By',
        'Date Created': 'Date Created',
        'Payment Date': 'Payment Date',
        'Account (Main)': 'Account'
    }
    df.rename(columns=rename_map, inplace=True)

    def extract_po_number(value):
        if isinstance(value, str) and "Purchase Order #" in value:
            return value.split("Purchase Order #")[-1].strip()
        return ""

    df['PO'] = df['Created From'].apply(extract_po_number)
    return df

# Load data
df = load_data()

# Desired columns to show in output
columns_to_show = [
    'Invoice', 'Subsidiary', 'Name', 'Date', 'Type', 'Status', 'Amount', 'Canada Amt',
    'Payment Hold', 'Vendor Bill Date', 'Received Bill Date', 'Due Date', 'EDI',
    'Accurate Pay', 'Location', 'Created By', 'Date Created', 'Payment Date', 'Account'
]

# Styling and UI
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stButton>button { background-color: #4CAF50; color: white; padding: 10px 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Invoice and PO Lookup")
st.markdown("Search by Invoice or PO Number. Use filters below for more precision.")

# Input fields
with st.expander("🔍 Search Filters", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        invoice_input = st.text_input("Enter Invoice Number")
        po_input = st.text_input("Enter PO Number")

    with col2:
        selected_subsidiary = st.selectbox("Select Subsidiary (optional)", options=["All"] + sorted(df['Subsidiary'].dropna().unique().tolist()))
        selected_status = st.selectbox("Select Status (optional)", options=["All"] + sorted(df['Status'].dropna().unique().tolist()))

# Filter logic
if st.button("🔎 Search"):
    invoice_input = invoice_input.strip()
    po_input = po_input.strip()
    result = df.copy()

    if invoice_input:
        result = result[result['Invoice'] == invoice_input]
    if po_input:
        result = result[result['PO'] == po_input]
    if selected_subsidiary != "All":
        result = result[result['Subsidiary'] == selected_subsidiary]
    if selected_status != "All":
        result = result[result['Status'] == selected_status]

    if result.empty:
        st.warning("⚠️ No records found with the given filters.")
    else:
        st.success(f"✅ Found {len(result)} record(s). Displaying results:")
        st.dataframe(result[columns_to_show], use_container_width=True)
else:
    st.info("👆 Enter your search terms and click 'Search' to begin.")
