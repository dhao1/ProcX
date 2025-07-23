
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

from procx.io.loader import load_ocel_json
from procx.preprocessing.transformer import flatten_ocel
from procx.ocpm.model_builder import build_object_graph

st.set_page_config(page_title="ProcX Dashboard", layout="wide")
st.title("🧠 ProcX Dashboard: Object-Centric Process Mining")

# Upload section
st.sidebar.header("1. Upload")
uploaded_file = st.sidebar.file_uploader("Upload your OCEL JSON file", type=["json"])

if uploaded_file:
    events, objects = load_ocel_json(uploaded_file)
    st.success("✅ File successfully loaded!")

    # Timestamp conversion
    if not pd.api.types.is_datetime64_any_dtype(events["ocel:timestamp"]):
        events["ocel:timestamp"] = pd.to_datetime(events["ocel:timestamp"])

    # Sidebar filters
    st.sidebar.header("2. Filtering")
    object_types = sorted({oid.split("_")[0] for row in events["ocel:omap"] for oid in row})
    selected_type = st.sidebar.selectbox("Select object type to flatten", object_types)

    min_date, max_date = events["ocel:timestamp"].min(), events["ocel:timestamp"].max()
    date_range = st.sidebar.date_input("Select date range", (min_date.date(), max_date.date()))
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    events = events[(events["ocel:timestamp"] >= start) & (events["ocel:timestamp"] <= end)]

    activity_options = sorted(events["ocel:activity"].unique())
    selected_activities = st.sidebar.multiselect("Select activities to include", activity_options, default=activity_options)
    events = events[events["ocel:activity"].isin(selected_activities)]

    if selected_type:
        st.header("📄 Flattened Event Log")
        flat_df = flatten_ocel(events, selected_type)
        st.dataframe(flat_df.head(10), use_container_width=True)

        st.download_button("⬇️ Download Flattened Log (CSV)", flat_df.to_csv(index=False).encode("utf-8"),
                           f"{selected_type}_flattened.csv", "text/csv")

        st.header("🔁 Variant Frequency")
        variants = flat_df.groupby("object_id")["activity"].apply(list)
        variant_freq = variants.value_counts().reset_index()
        variant_freq.columns = ["activity_sequence", "frequency"]
        st.dataframe(variant_freq.head(10), use_container_width=True)

        st.download_button("⬇️ Download Variants (CSV)", variant_freq.to_csv(index=False).encode("utf-8"),
                           "variants.csv", "text/csv")

        st.header("🔗 Object-Centric Graph")
        G = build_object_graph(flat_df)
        fig, ax = plt.subplots(figsize=(10, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, ax=ax)
        st.pyplot(fig)

        st.header("📊 Graph Metrics")
        st.markdown(f"- **Nodes:** {G.number_of_nodes()}")
        st.markdown(f"- **Edges:** {G.number_of_edges()}")
        st.markdown(f"- **Avg. Degree:** {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    else:
        st.warning("Please select a valid object type.")
else:
    st.info("Upload an OCEL JSON file to get started.")
