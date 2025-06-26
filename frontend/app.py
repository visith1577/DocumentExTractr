import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import requests

UPLOAD_URL = ""
RESPONSE_URL = ""

uploaded = st.file_uploader("Upload resume/email/scientific PDF/image",  type=["pdf","png","jpg","jpeg"])

if not uploaded:
    st.stop()

if st.button("Start processing"):
    files = {"file": (
        uploaded.name,  # pyright: ignore[reportAny]
        uploaded, 
        uploaded.type
    )}
    try:
        with st.spinner("Starting job..."):
            response = requests.post("http://localhost:8000/start-job", files=files, timeout=10)

        if response.status_code == 200:
            _ = st.toast("✅ Job started successfully", icon="🎉")
            st.session_state.started = True
        else:
            _ = st.toast("❌ Failed to start job", icon="⚠️")
            _ =st.error(f"Status: {response.status_code}\nMessage: {response.text}")

    except requests.exceptions.Timeout:
        _ = st.toast("⏳ Request timed out", icon="⏱️")
        _ = st.error("The request timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        _ = st.toast("🔌 Backend unreachable", icon="❌")
        _ = st.error("Could not connect to the backend. Is it running?")

    except Exception as e:
        _ = st.toast("🚨 Unknown error occurred", icon="🚨")
        _ = st.exception(e)


if not st.session_state.get("started", False):
    _ = st.info("Hit ▶️ to start classification / extraction")
    st.stop()

# Placeholders for status
class_ph = st.empty()
extract_ph = st.empty()

# @st.fragment(run_every=10)  # poll every 10s
# def poll_classification(ph: DeltaGenerator):
#     resp = requests.get(UPLOAD_URL).json()
#     status = resp["status"]  # "pending" or "done"
#     if status != "done":
#         ph.info(f"🔎 Classifying… ({resp.get('progress','0%')})")
#     else:
#         st.session_state.doc_type = resp["doc_type"]
#         st.session_state.classified = True
#         # Stop fragment polling and trigger full rerun
#         st.rerun(scope="app")

# if not st.session_state.get("classified", False):
#     poll_classification(class_ph)
#     st.stop()

# if st.session_state.doc_type == "None":
#     st.error("❌ Unrecognized document—please upload a valid one.")
#     st.stop()

# st.success(f"✅ Classified as: {st.session_state.doc_type}")

# @st.fragment(run_every=10)  # poll every 10s
# def poll_extraction(ph: DeltaGenerator):
#     resp = requests.get(RESPONSE_URL, params={"type": st.session_state.doc_type}).json()
#     if not resp["done"]:
#         ph.info(f"🛠️ Extracting info… ({resp.get('progress','0%')})")
#     else:
#         # Final data arrived—render UI for this doc_type
#         data = resp["extracted"]
#         if st.session_state.doc_type == "resume":
#             st.subheader("👤 Candidate Profile")
#             st.write(data["name"], data["email"], data["skills"])
#         elif st.session_state.doc_type == "email":
#             st.subheader("✉️ Email Metadata")
#             st.write(data["from"], data["to"], data["subject"])
#         else:  # scientific publication
#             st.subheader("📑 Publication Details")
#             st.write(data["title"], data["authors"], data["abstract"])
#         ph.empty()  # clear spinner
#         # Extraction done: stop this fragment
#         st.rerun(scope="app")

# poll_extraction(extract_ph)