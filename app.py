import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Log Analytics | Monitor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GitHub-hosted CSV dataset
CLOUD_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "RISHIVARDHANRAO/Cloud-Log-Prediction/"
    "refs/heads/main/LogAnalysisProject/data/Hdfs_structured.csv"
)

# Existing Power BI report URL
POWER_BI_URL = "https://app.powerbi.com/groups/me/reports/9febc1ef-321e-4016-bd76-23fd0cf9ceee/22408741f72de1bc088f?experience=power-bi"


# =========================================================
# SESSION STATE
# =========================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# =========================================================
# LOAD DATA FROM GITHUB
# =========================================================

@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv(CLOUD_DATA_URL)

    data["Level"] = data["Level"].fillna("UNKNOWN").astype(str)
    data["Component"] = data["Component"].fillna("Unknown").astype(str)
    data["EventId"] = data["EventId"].fillna("Unknown").astype(str)
    data["EventTemplate"] = data["EventTemplate"].fillna("Unknown").astype(str)
    data["Content"] = data["Content"].fillna("").astype(str)

    return data


try:
    df = load_data()
except Exception as e:
    st.error("Unable to load the dataset from GitHub.")
    st.info(
        "Check that the repository is public, the dataset URL is correct, "
        "and your internet connection is working."
    )
    st.caption(f"Technical details: {e}")
    st.stop()


# =========================================================
# THEME COLORS
# =========================================================

if st.session_state.dark_mode:
    bg = "#0B1020"
    panel = "#121A2B"
    panel_alt = "#182338"
    text = "#F1F5F9"
    muted = "#9AAAC2"
    border = "#26344C"
    accent = "#818CF8"
    grid = "#26344C"
    template = "plotly_dark"
    sidebar_bg = "#0E1628"
else:
    bg = "#F4F7FB"
    panel = "#FFFFFF"
    panel_alt = "#EEF3FA"
    text = "#172033"
    muted = "#65738A"
    border = "#DFE6F0"
    accent = "#4F46E5"
    grid = "#E5EAF2"
    template = "plotly_white"
    sidebar_bg = "#FFFFFF"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>
    :root {{
        --app-bg: {bg};
        --panel: {panel};
        --panel-alt: {panel_alt};
        --text: {text};
        --muted: {muted};
        --border: {border};
        --accent: {accent};
    }}

    .stApp {{
        background: var(--app-bg);
        color: var(--text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid var(--border);
    }}

    [data-testid="stSidebar"] * {{
        color: var(--text);
    }}

    .block-container {{
        padding-top: 1.7rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    h1, h2, h3 {{
        color: var(--text);
        letter-spacing: -0.5px;
    }}

    p, label, .stMarkdown {{
        color: var(--text);
    }}

    .hero {{
        padding: 1.5rem 1.7rem;
        background: linear-gradient(120deg, {panel}, {panel_alt});
        border: 1px solid var(--border);
        border-radius: 20px;
        margin-bottom: 1.5rem;
    }}

    .eyebrow {{
        color: var(--accent);
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 0.6rem;
    }}

    .hero-title {{
        color: var(--text);
        font-size: clamp(1.8rem, 3vw, 2.7rem);
        font-weight: 850;
        letter-spacing: -1.5px;
        line-height: 1.15;
        margin: 0;
    }}

    .hero-description {{
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0;
    }}

    .status-pill {{
        display: inline-block;
        background: {panel_alt};
        border: 1px solid var(--border);
        color: var(--accent);
        border-radius: 999px;
        padding: 0.4rem 0.8rem;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 1rem;
    }}

    .metric-card {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.2rem;
        min-height: 135px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.04);
    }}

    .metric-card:hover {{
        transform: translateY(-3px);
        border-color: var(--accent);
    }}

    .metric-label {{
        color: var(--muted);
        font-size: 0.83rem;
        font-weight: 650;
    }}

    .metric-value {{
        color: var(--text);
        font-size: clamp(1.6rem, 2vw, 2.15rem);
        font-weight: 850;
        letter-spacing: -1px;
        margin-top: 0.65rem;
    }}

    .metric-footer {{
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 0.3rem;
    }}

    div[data-testid="stPlotlyChart"] {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.5rem;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }}

    .stButton button,
    .stDownloadButton button,
    .stLinkButton a {{
        border-radius: 10px;
        font-weight: 700;
    }}

    .footer {{
        text-align: center;
        color: var(--muted);
        padding: 1.5rem 0 0.5rem;
        font-size: 0.8rem;
    }}

    .powerbi-card {{
        background: linear-gradient(120deg, {panel}, {panel_alt});
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}

    .powerbi-title {{
        color: {text};
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }}

    .powerbi-description {{
        color: {muted};
        font-size: 0.95rem;
        line-height: 1.7;
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .hero {{
            padding: 1.1rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER AND THEME SWITCH
# =========================================================

header_col, theme_col = st.columns([5, 1])

with header_col:
    st.markdown(
        f"""
        <div class="eyebrow">OBSERVABILITY PLATFORM</div>
        <div style="color:{muted};font-size:0.85rem;">
            HADOOP · HDFS · LOG INTELLIGENCE
        </div>
        """,
        unsafe_allow_html=True
    )

with theme_col:
    st.toggle(
        "🌙 Dark mode",
        key="dark_mode",
        help="Switch between dark and light dashboard themes."
    )


# Recalculate theme values after the toggle.

if st.session_state.dark_mode:
    bg = "#0B1020"
    panel = "#121A2B"
    panel_alt = "#182338"
    text = "#F1F5F9"
    muted = "#9AAAC2"
    border = "#26344C"
    accent = "#818CF8"
    grid = "#26344C"
    template = "plotly_dark"
else:
    bg = "#F4F7FB"
    panel = "#FFFFFF"
    panel_alt = "#EEF3FA"
    text = "#172033"
    muted = "#65738A"
    border = "#DFE6F0"
    accent = "#4F46E5"
    grid = "#E5EAF2"
    template = "plotly_white"


# =========================================================
# SIDEBAR FILTERS AND POWER BI LINK
# =========================================================

with st.sidebar:
    st.markdown("## 🎛️ Control Center")
    st.caption("Filter and explore your Hadoop logs.")
    st.divider()

    selected_levels = st.multiselect(
        "Log severity",
        options=sorted(df["Level"].unique()),
        default=sorted(df["Level"].unique())
    )

    selected_components = st.multiselect(
        "Hadoop components",
        options=sorted(df["Component"].unique()),
        default=sorted(df["Component"].unique())
    )

    event_ids = sorted(df["EventId"].unique())

    selected_events = st.multiselect(
        "Event IDs",
        options=event_ids,
        default=event_ids
    )

    st.divider()

    st.markdown("### 📊 Power BI Analytics")

    if (
        POWER_BI_URL.startswith("https://")
        and "PASTE_YOUR_POWER_BI_REPORT_URL_HERE" not in POWER_BI_URL
    ):
        st.link_button(
            "🚀 Open Power BI Dashboard",
            POWER_BI_URL,
            use_container_width=True
        )
    else:
        st.info("Add your Power BI report URL in the configuration section.")

    st.divider()

    st.markdown("### Dataset")
    st.write(f"📄 {len(df):,} total records")
    st.write(f"🧩 {df['Component'].nunique()} components")
    st.write(f"🏷️ {df['EventId'].nunique()} event IDs")

    if st.button("Reset filters", use_container_width=True):
        st.session_state.clear()
        st.rerun()


filtered_df = df[
    df["Level"].isin(selected_levels)
    & df["Component"].isin(selected_components)
    & df["EventId"].isin(selected_events)
].copy()


# =========================================================
# HERO
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">SYSTEM OVERVIEW</div>
        <div class="hero-title">Cloud-Based Log Analytics</div>
        <p class="hero-description">
            Explore Hadoop events, monitor warning patterns,
            and uncover insights from structured system logs.
        </p>
        <div class="status-pill">● DATASET LOADED</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI CARDS
# =========================================================

total = len(filtered_df)

info_count = int(
    (filtered_df["Level"].str.upper() == "INFO").sum()
)

warn_count = int(
    (filtered_df["Level"].str.upper() == "WARN").sum()
)

component_count = filtered_df["Component"].nunique()

metrics = [
    (
        "TOTAL LOG ENTRIES",
        f"{total:,}",
        "Records matching current filters"
    ),
    (
        "INFO EVENTS",
        f"{info_count:,}",
        f"{info_count / total * 100:.1f}% of filtered logs"
        if total else "No matching records"
    ),
    (
        "WARNING EVENTS",
        f"{warn_count:,}",
        f"{warn_count / total * 100:.1f}% of filtered logs"
        if total else "No matching records"
    ),
    (
        "ACTIVE COMPONENTS",
        f"{component_count}",
        "Components in current selection"
    )
]

metric_cols = st.columns(4)

for col, (label, value, footer) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-footer">{footer}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")


# =========================================================
# DASHBOARD TABS
# =========================================================

overview_tab, events_tab, records_tab, powerbi_tab = st.tabs(
    [
        "📊 Overview",
        "🔎 Event Explorer",
        "📋 Log Records",
        "📈 Power BI Analytics"
    ]
)


# =========================================================
# CHART HELPER
# =========================================================

def apply_chart_theme(fig, height=350):
    fig.update_layout(
        template=template,
        height=height,
        margin=dict(l=20, r=20, t=35, b=25),
        paper_bgcolor=panel,
        plot_bgcolor=panel,
        font=dict(family="Arial", color=text, size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(font_size=13)
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=grid,
        zerolinecolor=grid
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=grid,
        zerolinecolor=grid
    )

    return fig


# =========================================================
# OVERVIEW TAB
# =========================================================

with overview_tab:

    st.markdown("### Log Activity Overview")

    st.caption(
        "Interactive charts update when you change the sidebar filters."
    )

    chart_left, chart_right = st.columns(2)

    # Severity distribution

    with chart_left:

        st.markdown("#### Severity Distribution")

        level_counts = (
            filtered_df["Level"]
            .value_counts()
            .rename_axis("Level")
            .reset_index(name="Count")
        )

        if not level_counts.empty:

            fig = px.pie(
                level_counts,
                names="Level",
                values="Count",
                hole=0.68,
                color="Level",
                color_discrete_map={
                    "INFO": "#38BDF8",
                    "WARN": "#F59E0B",
                    "ERROR": "#F87171",
                    "FATAL": "#DC2626",
                    "UNKNOWN": "#94A3B8"
                }
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Count: %{value}<br>"
                    "Share: %{percent}<extra></extra>"
                )
            )

            apply_chart_theme(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No records match the selected filters.")

    # Component activity

    with chart_right:

        st.markdown("#### Component Activity")

        component_counts = (
            filtered_df["Component"]
            .value_counts()
            .rename_axis("Component")
            .reset_index(name="Count")
            .sort_values("Count")
        )

        if not component_counts.empty:

            fig = px.bar(
                component_counts,
                x="Count",
                y="Component",
                orientation="h",
                color="Count",
                color_continuous_scale="Blues",
                hover_data={"Count": True}
            )

            fig.update_layout(coloraxis_showscale=False)

            apply_chart_theme(fig, height=390)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No components match the selected filters.")

    # =====================================================
    # 3D LOG ACTIVITY — RECTANGULAR 3D BARS
    # =====================================================

    st.markdown("### 3D Log Activity")

    st.caption(
        "Bar height shows the number of log entries. Hover over a bar "
        "for its component, event ID, and warning count."
    )

    if not filtered_df.empty:

        bar_data = (
            filtered_df.groupby(
                ["Component", "EventId", "EventTemplate"],
                dropna=False
            )
            .agg(
                Total_Events=("LineId", "count"),
                Warning_Events=(
                    "Level",
                    lambda values: values.str.upper().eq("WARN").sum()
                )
            )
            .reset_index()
            .sort_values("Total_Events", ascending=False)
            .head(18)
            .reset_index(drop=True)
        )

        bar_data["Warning_Rate"] = (
            bar_data["Warning_Events"]
            .div(bar_data["Total_Events"])
            .mul(100)
        )

        component_names = list(
            bar_data["Component"].drop_duplicates()
        )

        event_names = list(
            bar_data["EventId"].drop_duplicates()
        )

        component_positions = {
            name: index
            for index, name in enumerate(component_names)
        }

        event_positions = {
            name: index
            for index, name in enumerate(event_names)
        }

        bar_data["X"] = bar_data["Component"].map(
            component_positions
        )

        bar_data["Y"] = bar_data["EventId"].map(
            event_positions
        )

        fig_3d = go.Figure()

        bar_width = 0.32
        bar_depth = 0.32

        color_scale = px.colors.sample_colorscale(
            "Viridis",
            [
                float(value) / 100
                for value in bar_data["Warning_Rate"].clip(0, 100)
            ]
        )

        for index, row in bar_data.iterrows():

            x0 = float(row["X"]) - bar_width / 2
            x1 = float(row["X"]) + bar_width / 2

            y0 = float(row["Y"]) - bar_depth / 2
            y1 = float(row["Y"]) + bar_depth / 2

            z0 = 0.0
            z1 = float(row["Total_Events"])

            xs = [x0, x1, x1, x0, x0, x1, x1, x0]
            ys = [y0, y0, y1, y1, y0, y0, y1, y1]
            zs = [z0, z0, z0, z0, z1, z1, z1, z1]

            i_faces = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
            j_faces = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 0, 4]
            k_faces = [2, 3, 6, 7, 5, 4, 6, 5, 7, 6, 4, 7]

            hover_text = (
                f"Component: {row['Component']}<br>"
                f"Event ID: {row['EventId']}<br>"
                f"Log entries: {int(row['Total_Events'])}<br>"
                f"Warnings: {int(row['Warning_Events'])}<br>"
                f"Warning rate: {row['Warning_Rate']:.2f}%<br>"
                f"Template: {row['EventTemplate']}"
            )

            fig_3d.add_trace(
                go.Mesh3d(
                    x=xs,
                    y=ys,
                    z=zs,
                    i=i_faces,
                    j=j_faces,
                    k=k_faces,
                    color=color_scale[index],
                    opacity=0.95,
                    flatshading=True,
                    hovertext=[hover_text] * 8,
                    hoverinfo="text",
                    showscale=False,
                    name=str(row["EventId"]),
                    showlegend=False
                )
            )

        fig_3d.add_trace(
            go.Scatter3d(
                x=[None, None],
                y=[None, None],
                z=[None, None],
                mode="markers",
                marker=dict(
                    size=0,
                    color=[0, 100],
                    cmin=0,
                    cmax=100,
                    colorscale="Viridis",
                    colorbar=dict(
                        title="Warning %",
                        thickness=12,
                        len=0.65
                    )
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

        max_count = max(
            1,
            int(bar_data["Total_Events"].max())
        )

        fig_3d.update_layout(
            template=template,
            height=590,
            paper_bgcolor=panel,
            font=dict(color=text, family="Arial", size=10),
            margin=dict(l=0, r=0, t=15, b=0),
            showlegend=False,
            scene=dict(
                bgcolor=panel,
                aspectmode="auto",
                xaxis=dict(
                    title="Component",
                    tickmode="array",
                    tickvals=list(range(len(component_names))),
                    ticktext=[
                        name if len(name) <= 16
                        else name[:13] + "..."
                        for name in component_names
                    ],
                    backgroundcolor=panel,
                    gridcolor=grid,
                    zerolinecolor=grid
                ),
                yaxis=dict(
                    title="Event ID",
                    tickmode="array",
                    tickvals=list(range(len(event_names))),
                    ticktext=event_names,
                    backgroundcolor=panel,
                    gridcolor=grid,
                    zerolinecolor=grid
                ),
                zaxis=dict(
                    title="Log Entries",
                    range=[0, max_count * 1.1],
                    backgroundcolor=panel,
                    gridcolor=grid,
                    zerolinecolor=grid
                ),
                camera=dict(
                    eye=dict(x=1.65, y=1.65, z=1.25)
                )
            )
        )

        st.plotly_chart(
            fig_3d,
            use_container_width=True,
            config={
                "scrollZoom": True,
                "displaylogo": False
            }
        )

    else:
        st.info("No component data matches the current filters.")

    # Frequently occurring events

    st.markdown("### Frequently Occurring Events")

    event_counts = (
        filtered_df["EventTemplate"]
        .value_counts()
        .head(8)
        .rename_axis("Event Template")
        .reset_index(name="Count")
        .sort_values("Count")
    )

    if not event_counts.empty:

        fig = px.bar(
            event_counts,
            x="Count",
            y="Event Template",
            orientation="h",
            color="Count",
            color_continuous_scale="Purples",
            hover_data={"Count": True}
        )

        fig.update_layout(coloraxis_showscale=False)

        apply_chart_theme(fig, height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No event patterns match the selected filters.")


# =========================================================
# EVENT EXPLORER TAB
# =========================================================

with events_tab:

    st.markdown("### Explore Event Patterns")

    st.caption(
        "Inspect event identifiers, recurring templates, and warnings."
    )

    if filtered_df.empty:

        st.info("No events match the current filters.")

    else:

        event_left, event_right = st.columns(2)

        with event_left:

            st.markdown("#### Event ID Frequency")

            event_id_counts = (
                filtered_df["EventId"]
                .value_counts()
                .rename_axis("Event ID")
                .reset_index(name="Count")
                .sort_values("Count")
            )

            fig = px.bar(
                event_id_counts,
                x="Count",
                y="Event ID",
                orientation="h",
                color="Count",
                color_continuous_scale="Teal"
            )

            fig.update_layout(coloraxis_showscale=False)

            apply_chart_theme(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with event_right:

            st.markdown("#### Warning Analysis")

            warnings = filtered_df[
                filtered_df["Level"].str.upper() == "WARN"
            ]

            st.metric(
                "Warnings in Current Selection",
                f"{len(warnings):,}"
            )

            if not warnings.empty:

                warning_components = (
                    warnings["Component"]
                    .value_counts()
                    .rename_axis("Component")
                    .reset_index(name="Warnings")
                )

                fig = px.bar(
                    warning_components,
                    x="Component",
                    y="Warnings",
                    color="Warnings",
                    color_continuous_scale="Oranges"
                )

                fig.update_layout(coloraxis_showscale=False)

                apply_chart_theme(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info(
                    "No WARN entries in the current selection."
                )

        st.markdown("#### Event Template Details")

        templates = (
            filtered_df.groupby(
                ["EventId", "EventTemplate"],
                dropna=False
            )
            .size()
            .reset_index(name="Occurrences")
            .sort_values("Occurrences", ascending=False)
        )

        st.dataframe(
            templates,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# LOG RECORDS TAB
# =========================================================

with records_tab:

    st.markdown("### Log Record Explorer")

    st.caption(
        "Search messages and inspect the matching structured records."
    )

    search_query = st.text_input(
        "🔍 Search logs",
        placeholder=(
            "Try an event ID, component, block ID, or message..."
        )
    )

    search_columns = [
        "Content",
        "Component",
        "EventId",
        "EventTemplate",
        "Pid"
    ]

    searchable_df = filtered_df.copy()

    if search_query.strip():

        mask = pd.Series(
            False,
            index=searchable_df.index
        )

        for column in search_columns:

            mask |= searchable_df[column].astype(str).str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )

        searchable_df = searchable_df[mask]

    st.write(
        f"**{len(searchable_df):,} records found**"
    )

    st.dataframe(
        searchable_df,
        use_container_width=True,
        hide_index=True,
        height=480
    )

    download_data = searchable_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Records",
        data=download_data,
        file_name="filtered_hdfs_logs.csv",
        mime="text/csv",
        use_container_width=False
    )


# =========================================================
# POWER BI ANALYTICS TAB
# =========================================================

with powerbi_tab:

    st.markdown("### 📊 Power BI Analytics")

    st.caption(
        "Access the interactive Power BI report for additional "
        "analysis of the Hadoop log dataset."
    )

    st.markdown(
        f"""
        <div class="powerbi-card">
            <div class="eyebrow">BUSINESS INTELLIGENCE</div>
            <div class="powerbi-title">
                Hadoop Log Analytics Dashboard
            </div>
            <div class="powerbi-description">
                Explore log severity distribution, component activity,
                log trends, frequent events, and interactive Power BI
                visualizations.
                <br><br>
                Your report opens in a separate browser tab.
                Sign-in and report permissions may be required.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if (
        POWER_BI_URL.startswith("https://")
        and "PASTE_YOUR_POWER_BI_REPORT_URL_HERE" not in POWER_BI_URL
    ):

        st.link_button(
            "🚀 Open Power BI Dashboard",
            POWER_BI_URL,
            type="primary",
            use_container_width=True
        )

        st.caption(
            "The report is hosted in Power BI Service. "
            "Its access permissions are managed separately."
        )

    else:

        st.warning(
            "The Power BI report URL has not been configured yet."
        )

        st.markdown(
            """
            **To connect your report:**

            1. Open your published report in Power BI Service.
            2. Copy the normal report URL from your browser.
            3. Open the configuration section at the top of this file.
            4. Replace `PASTE_YOUR_POWER_BI_REPORT_URL_HERE` with
               the URL inside the quotation marks.
            5. Save this Python file and rerun Streamlit.
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        CLOUD-BASED LOG ANALYTICS
        &nbsp; · &nbsp;
        HDFS STRUCTURED LOGS
        <br>
        Built with Python, Pandas, Streamlit and Plotly
        <br>
        Power BI Analytics Integration
    </div>
    """,
    unsafe_allow_html=True
)