import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------- 
# Streamlit Config 
# ------------------------------- 
st.set_page_config(page_title="REIT Analyzer (CSV)", layout="wide")
st.title("🏢 REIT Performance & Sector Analyzer (CSV-Based)")

# ------------------------------- 
# Load Data 
# ------------------------------- 
@st.cache_data
def load_data():
    return pd.read_csv("reit_data.csv")

data = load_data()

# ------------------------------- 
# Ticker Filter 
# ------------------------------- 
tickers = st.multiselect("📌 Select REIT Tickers", data["Ticker"].unique().tolist(), 
                        default=data["Ticker"].unique().tolist())

if not tickers:
    st.warning("⚠️ Please select at least one REIT ticker.")
    st.stop()

df = data[data["Ticker"].isin(tickers)]

# ------------------------------- 
# Display Table 
# ------------------------------- 
st.subheader("📊 REIT Overview")
st.dataframe(df)

# ------------------------------- 
# Pie Chart: Industry Breakdown 
# ------------------------------- 
col1, col2 = st.columns([1, 2])  # Create columns for better layout

with col1:
    if not df["Industry"].isnull().all():
        st.subheader("📈 Industry Breakdown")
        fig1, ax1 = plt.subplots(figsize=(4, 4))  # Adjusted size
        industry_counts = df["Industry"].value_counts()
        ax1.pie(industry_counts, labels=industry_counts.index, autopct="%1.1f%%", startangle=140)
        ax1.axis("equal")
        plt.tight_layout()
        st.pyplot(fig1)
    else:
        st.warning("⚠️ No industry data to display.")

# ------------------------------- 
# Bar Chart Function - Improved
# ------------------------------- 
def render_barplot(title, y_value, y_label, col_obj):
    with col_obj:
        st.subheader(title)
        fig, ax = plt.subplots(figsize=(5, 3))  # Smaller figure
        
        # Create bar plot with improved aesthetics
        sns.barplot(data=df, x="Ticker", y=y_value, hue="Industry", ax=ax)
        
        # Improve readability
        ax.set_ylabel(y_label, fontsize=10)
        ax.set_xlabel("", fontsize=10)
        ax.tick_params(axis='x', labelsize=8, rotation=45)  # Rotate x labels for better fit
        ax.tick_params(axis='y', labelsize=8)
        
        # Improve legend placement
        if len(df["Industry"].unique()) > 1:
            ax.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.3, 1))
        else:
            ax.legend([])  # Hide legend if only one industry
            
        plt.tight_layout()
        st.pyplot(fig)

# ------------------------------- 
# Create responsive layout with columns
# ------------------------------- 
col1, col2 = st.columns(2)  # Two columns for charts

# Render charts in columns for better space utilization
render_barplot("💵 Market Cap Comparison", "Market Cap", "Market Cap ($)", col1)
render_barplot("💰 Dividend Yield Comparison", "Dividend Yield", "Dividend Yield (%)", col2)

col3, col4 = st.columns(2)  # Two more columns
render_barplot("📈 Beta Comparison", "Beta", "Beta", col3)

# Add a placeholder in col4 if needed
with col4:
    st.write("")  # Empty space for balance

# ------------------------------- 
# CSV Export 
# ------------------------------- 
st.subheader("⬇️ Export Your Data")
st.download_button("📥 Export as CSV", data=df.to_csv(index=False), 
                  file_name="reit_data_filtered.csv", mime="text/csv")