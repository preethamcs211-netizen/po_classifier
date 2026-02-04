import json
import streamlit as st
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("PO L1-L2-L3 Classifier")
st.caption("Classify a purchase order description into L1/L2/L3 using the fixed taxonomy.")

SAMPLES = [
    {
        "label": "DocuSign subscription",
        "po": "DocuSign Inc - eSignature Enterprise Pro Subscription",
        "supplier": "DocuSign Inc",
    },
    {
        "label": "Business travel flight",
        "po": "Flight ticket for business travel",
        "supplier": "Indigo Airlines",
    },
    {
        "label": "Office chairs",
        "po": "Ergonomic office chairs for new hires",
        "supplier": "Herman Miller",
    },
    {
        "label": "Cloud hosting",
        "po": "Monthly cloud hosting charges for production workloads",
        "supplier": "AWS",
    },
]

if "po_description" not in st.session_state:
    st.session_state.po_description = ""
if "supplier" not in st.session_state:
    st.session_state.supplier = ""

with st.expander("Load a sample", expanded=False):
    sample_label = st.selectbox("Sample", [s["label"] for s in SAMPLES])
    if st.button("Use sample"):
        selected = next(s for s in SAMPLES if s["label"] == sample_label)
        st.session_state.po_description = selected["po"]
        st.session_state.supplier = selected["supplier"]

with st.form("classify_form"):
    po_description = st.text_area(
        "PO Description",
        height=140,
        placeholder="Example: Annual renewal for endpoint security software",
        key="po_description",
    )
    supplier = st.text_input(
        "Supplier (optional)",
        placeholder="Example: CrowdStrike",
        key="supplier",
    )
    show_raw = st.checkbox("Show raw model response", value=False)
    submitted = st.form_submit_button("Classify")

if submitted:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier or "Not provided")

        try:
            st.json(json.loads(result))
        except Exception:
            st.error("Invalid model response. Showing raw output below.")
            st.text(result)

        if show_raw:
            st.divider()
            st.subheader("Raw response")
            st.code(result, language="json")
