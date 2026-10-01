from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Netflix Insights | StreamScope", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

# ---------------------------- Premium dark UI ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --red:#e50914; --red2:#ff3944; --bg:#09090d; --panel:#15151c; --line:rgba(255,255,255,.085); --muted:#a2a2b1; }
.stApp { background: radial-gradient(ellipse at 85% 0%, rgba(105,12,24,.28), transparent 35%), #09090d; color:#f7f7fb; font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(9,9,13,.78); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#121218,#0c0c11); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#f3f3f7; }
.block-container { max-width:1550px; padding-top:1.5rem; padding-bottom:3rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif!important; letter-spacing:-.7px; color:#fff; }
h1 { font-weight:800!important; letter-spacing:-1.6px!important; }
h2 { font-size:1.35rem!important; font-weight:750!important; }
h3 { font-size:1.02rem!important; }
p, label, .stMarkdown { color:#e9e9ef; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#1b1b24,#121218); border:1px solid #292933; border-radius:17px; padding:1.1rem 1.2rem; box-shadow:0 12px 35px rgba(0,0,0,.14); min-height:118px; }
[data-testid="stMetricLabel"] { color:#aaaab8!important; font-size:.82rem!important; font-weight:600!important; }
[data-testid="stMetricValue"] { color:#fff!important; font-family:'Manrope',sans-serif; font-weight:800!important; }
[data-testid="stMetricDelta"] { color:#b9b9c5!important; }
[data-testid="stPlotlyChart"] { background:#131319; border:1px solid var(--line); border-radius:16px; padding:8px 8px 0; }
[data-testid="stDataFrame"] { border:1px solid #2b2b35; border-radius:13px; }
[data-testid="stFileUploader"] { background:#17171e; border:1px dashed #484853; border-radius:12px; }
[data-baseweb="select"] > div, [data-testid="stSidebar"] input { background:#1a1a22!important; border-color:#343440!important; border-radius:9px!important; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background:#a80710!important; }
.stButton > button, .stDownloadButton > button { background:linear-gradient(100deg,#e50914,#b20710); color:white; border:0; border-radius:10px; font-weight:700; padding:.55rem 1rem; }
.stButton > button:hover, .stDownloadButton > button:hover { border:1px solid #ff737a; color:white; }
.stTabs [data-baseweb="tab-list"] { gap:8px; background:#121218; padding:7px; border:1px solid var(--line); border-radius:13px; }
.stTabs [data-baseweb="tab"] { border-radius:9px; padding:9px 18px; color:#bcbcc8; }
.stTabs [aria-selected="true"] { background:#2a171b!important; color:#fff!important; }
hr { border-color:var(--line); }
.hero { position:relative; overflow:hidden; background:linear-gradient(110deg,rgba(39,13,19,.97),rgba(19,19,27,.95) 57%,rgba(45,12,19,.78)); border:1px solid rgba(229,9,20,.28); border-radius:22px; padding:28px 32px; margin-bottom:22px; }
.hero:after { content:'N'; position:absolute; right:36px; top:-53px; font-family:Arial,sans-serif; font-size:230px; font-weight:900; color:rgba(229,9,20,.09); line-height:1; pointer-events:none; }
.kicker { color:#ff6870; text-transform:uppercase; letter-spacing:2.2px; font-size:.7rem; font-weight:800; margin-bottom:8px; }
.hero-sub { color:#b7b7c4; font-size:.98rem; max-width:720px; }
.section-note { color:#9292a1; font-size:.82rem; margin-top:-8px; margin-bottom:14px; }
.pill { display:inline-block; padding:5px 10px; background:rgba(229,9,20,.13); border:1px solid rgba(229,9,20,.25); color:#ff8b91; border-radius:999px; font-size:.75rem; font-weight:700; }
div[data-testid="stExpander"] { background:#14141b; border:1px solid var(--line); border-radius:13px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------- Header ----------------------------
logo_path = Path(__file__).with_name("images.png")
with st.container():
    logo_col, title_col = st.columns([1, 5], vertical_alignment="center")
    with logo_col:
        if logo_path.exists():
            st.image(str(logo_path), width=125)
        else:
            st.markdown("<h1 style='color:#e50914'>N</h1>", unsafe_allow_html=True)
    with title_col:
        st.markdown('<div class="kicker">STREAMING INTELLIGENCE • ANALYTICS STUDIO</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="margin:0;font-size:2.35rem">Netflix Insights</h1>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">A clear, interactive view of audience activity, subscription revenue and content performance.</div>', unsafe_allow_html=True)

st.write("")

required_columns = {"Watch_Date", "Region", "Monthly_Revenue", "Subscription_Plan", "Rating", "Category"}
local_csv = Path(__file__).with_name("netflix.csv")
with st.sidebar:
    st.markdown("# 🎛️ Control room")
    st.caption("Use the filters to update the entire dashboard.")
    uploaded_csv = st.file_uploader("Upload a dataset (CSV)", type=["csv"])

try:
    if uploaded_csv is not None:
        data = pd.read_csv(uploaded_csv)
        source_name = uploaded_csv.name
    elif local_csv.exists():
        data = pd.read_csv(local_csv)
        source_name = local_csv.name
    else:
        st.info("Upload a CSV file from the sidebar to get started.")
        st.stop()
except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error(f"Could not read the CSV: {error}")
    st.stop()

missing = required_columns - set(data.columns)
if missing:
    st.error("The dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

data = data.copy()
data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
data["Monthly_Revenue"] = pd.to_numeric(data["Monthly_Revenue"], errors="coerce")
data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
if "Watch_Time_Minutes" in data.columns:
    data["Watch_Time_Minutes"] = pd.to_numeric(data["Watch_Time_Minutes"], errors="coerce")
data = data.dropna(subset=["Watch_Date"])
if data.empty:
    st.warning("No valid dates were found in Watch_Date.")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.divider()
    st.markdown("### Refine results")
    def multiselect_if_present(label, column):
        if column in data.columns:
            return st.multiselect(label, sorted(data[column].dropna().astype(str).unique()))
        return []
    regions = multiselect_if_present("🌍 Region", "Region")
    plans = multiselect_if_present("💳 Subscription plan", "Subscription_Plan")
    categories = multiselect_if_present("🎭 Genre / category", "Category")
    languages = multiselect_if_present("🗣️ Language", "Language")
    devices = multiselect_if_present("📱 Device", "Device")
    types = multiselect_if_present("🎞️ Content type", "Type")
    min_date, max_date = data["Watch_Date"].min().date(), data["Watch_Date"].max().date()
    date_range = st.date_input("📅 Viewing period", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    st.divider()
    st.caption(f"Dataset: {source_name} · {len(data):,} rows")

filtered = data.copy()
for col, chosen in [("Region", regions), ("Subscription_Plan", plans), ("Category", categories), ("Language", languages), ("Device", devices), ("Type", types)]:
    if chosen and col in filtered.columns:
        filtered = filtered[filtered[col].astype(str).isin(chosen)]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[filtered["Watch_Date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1))]
if filtered.empty:
    st.warning("No records match these filters. Try widening the date range or clearing a filter.")
    st.stop()

# Plotly theme helpers
PLOT_BG = "#131319"
GRID = "rgba(255,255,255,.07)"
RED = "#e50914"
PALETTE = ["#e50914", "#ff5964", "#9f0710", "#6c6c7c", "#c4c4d0", "#7b3440", "#ed8a90"]
def polish(fig, height=330):
    fig.update_layout(template="plotly_dark", paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color="#e9e9ef", size=12),
        margin=dict(l=18, r=18, t=45, b=18), height=height,
        title=dict(font=dict(size=15, color="#f7f7fb"), x=0.02),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.2))
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID)
    return fig

revenue = filtered["Monthly_Revenue"].sum(skipna=True)
avg_rating = filtered["Rating"].mean()
watch_hours = filtered["Watch_Time_Minutes"].sum(skipna=True) / 60 if "Watch_Time_Minutes" in filtered.columns else None
unique_titles = filtered["Title"].nunique() if "Title" in filtered.columns else (filtered["Movie_ID"].nunique() if "Movie_ID" in filtered.columns else None)

st.markdown('<div class="pill">● LIVE FILTERED VIEW</div>', unsafe_allow_html=True)
st.markdown("")
metrics = st.columns(4)
metrics[0].metric("Dataset records", f"{len(filtered):,}")
metrics[1].metric("Total revenue", f"${revenue:,.0f}")
metrics[2].metric("Average rating", f"{avg_rating:.2f} / 5" if pd.notna(avg_rating) else "N/A")
metrics[3].metric("Watch time", f"{watch_hours:,.0f} hrs" if watch_hours is not None else "N/A")
st.markdown(f'<div class="section-note">Showing {len(filtered):,} records from <b>{source_name}</b> · {filtered["Watch_Date"].min():%d %b %Y} – {filtered["Watch_Date"].max():%d %b %Y}</div>', unsafe_allow_html=True)

# Tabs keep the dashboard tidy and make the content easier to present.
overview_tab, content_tab, data_tab = st.tabs(["✨ Overview", "🎬 Content & audience", "📋 Data explorer"])
with overview_tab:
    st.subheader("Performance at a glance")
    st.caption("Explore how revenue and audience activity vary across regions and time.")
    left, right = st.columns(2, gap="large")
    with left:
        region_rev = filtered.groupby("Region", dropna=False)["Monthly_Revenue"].sum().sort_values().reset_index()
        fig = px.bar(region_rev, x="Monthly_Revenue", y="Region", orientation="h", text_auto=".2s", title="Revenue by region", color="Monthly_Revenue", color_continuous_scale=[[0,"#641018"],[1,RED]])
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Revenue", yaxis_title="")
        st.plotly_chart(polish(fig), use_container_width=True)
    with right:
        monthly = filtered.assign(Month=filtered["Watch_Date"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False)["Monthly_Revenue"].sum()
        fig = px.area(monthly, x="Month", y="Monthly_Revenue", title="Revenue trend over time", markers=True)
        fig.update_traces(line_color=RED, fillcolor="rgba(229,9,20,.16)", marker=dict(size=6, color=RED))
        fig.update_layout(xaxis_title="", yaxis_title="Revenue")
        st.plotly_chart(polish(fig), use_container_width=True)
    left, right = st.columns(2, gap="large")
    with left:
        if "Subscription_Plan" in filtered.columns:
            plan_rev = filtered.groupby("Subscription_Plan", as_index=False)["Monthly_Revenue"].sum()
            fig = px.pie(plan_rev, names="Subscription_Plan", values="Monthly_Revenue", hole=.62, title="Revenue mix by plan", color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="outside", textinfo="percent+label", marker=dict(line=dict(color=PLOT_BG, width=3)))
            st.plotly_chart(polish(fig, 340), use_container_width=True)
    with right:
        if "Device" in filtered.columns:
            device_counts = filtered["Device"].value_counts().rename_axis("Device").reset_index(name="Records")
            fig = px.bar(device_counts, x="Device", y="Records", title="Viewing by device", color="Device", color_discrete_sequence=PALETTE)
            fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Records")
            st.plotly_chart(polish(fig, 340), use_container_width=True)

with content_tab:
    st.subheader("Content & audience insights")
    st.caption("See which categories and titles appear most often in the selected dataset.")
    left, right = st.columns(2, gap="large")
    with left:
        if "Category" in filtered.columns:
            cat = filtered["Category"].value_counts().rename_axis("Category").reset_index(name="Records").sort_values("Records")
            fig = px.bar(cat, x="Records", y="Category", orientation="h", title="Records by category", text="Records", color="Records", color_continuous_scale=[[0,"#641018"],[1,RED]])
            fig.update_layout(coloraxis_showscale=False, xaxis_title="Records", yaxis_title="")
            st.plotly_chart(polish(fig, 380), use_container_width=True)
    with right:
        if "Title" in filtered.columns:
            titles_df = filtered["Title"].value_counts().head(10).rename_axis("Title").reset_index(name="Records").sort_values("Records")
            fig = px.bar(titles_df, x="Records", y="Title", orientation="h", title="Top 10 titles in dataset", text="Records", color="Records", color_continuous_scale=[[0,"#641018"],[1,RED]])
            fig.update_layout(coloraxis_showscale=False, xaxis_title="Records", yaxis_title="")
            st.plotly_chart(polish(fig, 380), use_container_width=True)
    if "Rating" in filtered.columns and "Subscription_Plan" in filtered.columns:
        rating_plan = filtered.groupby("Subscription_Plan", as_index=False)["Rating"].mean()
        fig = px.bar(rating_plan, x="Subscription_Plan", y="Rating", title="Average rating by subscription plan", text_auto=".2f", color="Subscription_Plan", color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False, yaxis_title="Average rating", xaxis_title="", yaxis_range=[0,5])
        st.plotly_chart(polish(fig, 320), use_container_width=True)

with data_tab:
    st.subheader("Explore the underlying records")
    search = st.text_input("Search records", placeholder="Search title, region, category, language…")
    view = filtered.copy()
    searchable = [c for c in ["Title", "Region", "Category", "Language", "Subscription_Plan", "Device", "Type"] if c in view.columns]
    if search and searchable:
        mask = pd.Series(False, index=view.index)
        for col in searchable:
            mask |= view[col].astype(str).str.contains(search, case=False, na=False)
        view = view[mask]
    sort_col = st.selectbox("Sort records by", [c for c in ["Watch_Date", "Monthly_Revenue", "Rating", "Watch_Count", "Watch_Time_Minutes"] if c in view.columns], index=0)
    view = view.sort_values(sort_col, ascending=(sort_col == "Watch_Date"), na_position="last")
    st.caption(f"{len(view):,} records found")
    st.dataframe(view, use_container_width=True, hide_index=True, height=420)
    st.download_button("⬇️ Download filtered CSV", data=view.to_csv(index=False).encode("utf-8"), file_name="netflix_filtered_data.csv", mime="text/csv")

st.divider()
footer_left, footer_right = st.columns([3, 1])
with footer_left:
    st.caption(" NETFLIX INSIGHTS · College data analytics project")
with footer_right:
    st.caption("Built with Python by Tejas Kasure")
