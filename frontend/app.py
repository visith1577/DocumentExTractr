import io
import json
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_extras.pdf_viewer import pdf_viewer
import requests

UPLOAD_URL = "http://0.0.0.0:3000/classify-docs"
EXTRACTION_URL = "http://0.0.0.0:3000/extraction"

st.set_page_config(page_title="📝 Document Processor", layout="wide")
_ = st.title("📝 Document Classifier and Extractor")

_ = st.subheader("📤 Upload your document")
uploaded = st.file_uploader(
    "Upload resume/email/scientific PDF/image",
    help="upload only images or convert pdf to img",
    type=["png", "jpg", "jpeg"],
)

if uploaded:
    file_bytes = uploaded.read()
    file_type = uploaded.type

    _ = st.markdown("### 📄 Document Preview")
    if "image" in file_type:
        _ = st.image(file_bytes, caption=uploaded.name, use_container_width=True)  # pyright: ignore[reportAny]
    elif "pdf" in file_type:
        pdf_viewer(data=file_bytes, width=None, height=600)
    else:
        _ = st.warning("Unsupported file type.")

    if st.button("🚀 Start Processing"):
        try:
            with st.spinner("Starting classification..."):
                files = {
                    "files": (uploaded.name, io.BytesIO(file_bytes), uploaded.type)  # pyright: ignore[reportAny]
                }
                response = requests.post(UPLOAD_URL, files=files, timeout=60)
                response.raise_for_status()

                result = response.json()  # pyright: ignore[reportAny]
                doc_id: str = result["doc_id"]  # pyright: ignore[reportAny]
                doc_type: str = result["type"]  # pyright: ignore[reportAny]

                if doc_type == "None":
                    _ = st.error("❌ Unable to classify the document.")
                    st.stop()

                _ = st.success(f"✅ Classified as: **{doc_type.upper()}**")
                _ = st.toast("Classification complete 🎯", icon="✅")

                st.session_state.doc_id = doc_id
                st.session_state.doc_type = doc_type
                st.session_state.polling = True  # enable polling

        except Exception as e:
            _ = st.error(f"🚨 Error: {str(e)}")
            st.stop()


status_placeholder = st.empty()
result_placeholder = st.empty()


if st.session_state.get("polling", False):

    @st.fragment(run_every=5)  # 🔥 Poll every 5 seconds
    def poll_extraction(ph: DeltaGenerator):
        doc_id = st.session_state.doc_id  # pyright: ignore[reportAny]
        doc_type = st.session_state.doc_type  # pyright: ignore[reportAny]

        poll_url = f"{EXTRACTION_URL}/{doc_type}/{doc_id}"

        try:
            response = requests.get(poll_url, timeout=10)

            if response.status_code == 200:
                _ = st.toast("✅ Extraction complete", icon="🎉")
                data = response.json()["extraction_results"]  # pyright: ignore[reportAny]

                _ = ph.success("🎯 Extraction complete!")

                with ph.expander("📦 Extraction JSON"):
                    _ = ph.json(data)  # pyright: ignore[reportAny]

                _ = ph.code(json.dumps(data, indent=4), language="json")

                st.session_state.polling = False  # 🛑 Stop polling after success
                st.rerun(scope="app")  # 🔄 Trigger rerun to clean polling UI

            elif response.status_code == 404:
                _ = ph.info("⏳ Extraction in progress...")
            else:
                _ = ph.error(f"❌ Error: {response.status_code} — {response.text}")
                st.session_state.polling = False

        except Exception as e:
            _ = ph.error(f"🚨 Exception: {str(e)}")
            st.session_state.polling = False

    poll_extraction(status_placeholder)
