import html
import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.app.services.exporters import (
    format_docx,
    format_pdf,
    format_txt,
    
)
from backend.app.utils.text import format_html_preview


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
)

GENERATE_URL = f"{BACKEND_URL}/generate"


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 17px;
    margin-bottom: 25px;
}

.preview-card {
    background: #111827;
    color: #f9fafb;
    padding: 30px;
    border-radius: 15px;
    max-height: 650px;
    overflow-y: auto;
    border: 1px solid #374151;
    line-height: 1.7;
}

.preview-card h1 {
    color: #ffffff;
    font-size: 28px;
}

.preview-card h2 {
    color: #ffffff;
    font-size: 22px;
    margin-top: 20px;
}

.preview-card h3 {
    color: #ffffff;
    font-size: 18px;
    margin-top: 18px;
}

.preview-card p {
    margin-bottom: 12px;
}

.preview-card .bullet {
    padding-left: 10px;
}

.preview-card .numbered {
    margin-left: 5px;
}

.warning-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff7ed;
    border: 1px solid #fdba74;
    color: #7c2d12;
}

</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

left, center, right = st.columns(
    [1, 2, 1]
)

with center:

    logo_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "legalese_logo.png",
    )

    if os.path.exists(logo_path):
        st.image(
            logo_path,
            width=130,
        )

    st.markdown(
        '<div class="main-title">LegalEase</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="subtitle">
        AI-Powered Legal Document Generator
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
<div class="warning-box">
<strong>Important:</strong>
LegalEase generates AI-assisted legal document drafts.
The generated document should be reviewed by a qualified legal
professional before signing or relying upon it.
</div>
""",
    unsafe_allow_html=True,
)

st.write("")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Document Settings")

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "Partnership Agreement",
            "General Agreement",
            "Custom Legal Document",
        ],
    )

    st.caption(
        "Choose the closest document type for your requirements."
    )

    st.divider()

    st.subheader("Backend")

    st.code(
        BACKEND_URL,
        language="text",
    )

    st.caption(
        "Make sure the FastAPI server is running before generating."
    )


# ---------------------------------------------------------
# Input form
# ---------------------------------------------------------

st.header("1. Enter Document Details")

col1, col2 = st.columns(2)

with col1:

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider)\n"
            "TechNova Inc. (Client)"
        ),
        height=160,
    )

with col2:

    effective_date = st.date_input(
        "Effective Date",
        value=date.today(),
    )

    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Optional instructions for the AI..."
        ),
        height=100,
    )


terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Enter each term on a separate line.\n\n"
        "Example:\n"
        "Payment to be made within 30 days of invoice.\n"
        "The provider agrees to deliver work by the agreed deadline.\n"
        "Confidentiality must be maintained.\n"
        "Either party may terminate with 15 days notice."
    ),
    height=220,
)


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

generate_button = st.button(
    "✨ Generate Legal Document",
    type="primary",
    use_container_width=True,
)


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": effective_date.strftime(
                "%B %d, %Y"
            ),
            "additional_instructions": (
                additional_instructions
            ),
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    GENERATE_URL,
                    json=payload,
                    timeout=180,
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.generated_document = (
                        data["content"]
                    )

                    st.session_state.document_type = (
                        document_type
                    )

                    st.success(
                        "Document generated successfully."
                    )

                else:

                    try:
                        error_data = response.json()
                        detail = error_data.get(
                            "detail",
                            "Unknown backend error.",
                        )
                    except Exception:
                        detail = response.text

                    st.error(
                        f"Generation failed: {detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend. "
                    "Start the backend using:\n\n"
                    "`uvicorn backend.app.main:app --reload`"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "Please try again."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ---------------------------------------------------------
# Generated document
# ---------------------------------------------------------

if st.session_state.generated_document:

    st.divider()

    st.header("2. Document Preview & Editing")

    tab_preview, tab_edit = st.tabs(
        [
            "📄 Preview",
            "✏️ Edit Document",
        ]
    )

    with tab_preview:

        preview_html = format_html_preview(
            st.session_state.generated_document
        )

        st.markdown(
            f"""
            <div class="preview-card">
                {preview_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_edit:

        edited_document = st.text_area(
            "Edit your document",
            value=st.session_state.generated_document,
            height=650,
            key="document_editor",
        )

        if st.button(
            "Save Edits",
            use_container_width=True,
        ):

            st.session_state.generated_document = (
                edited_document
            )

            st.success(
                "Your edits have been saved."
            )

            st.rerun()


    # -----------------------------------------------------
    # Downloads
    # -----------------------------------------------------

    st.divider()

    st.header("3. Download Document")

    final_text = st.session_state.generated_document

    document_name = (
        st.session_state.document_type
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
    )

    txt_data = format_txt(
        final_text,
        st.session_state.document_type,
    )

    docx_data = format_docx(
        final_text,
        st.session_state.document_type,
    )

    pdf_data = format_pdf(
        final_text,
        st.session_state.document_type,
    )

    d1, d2, d3 = st.columns(3)

    with d1:

        st.download_button(
            label="⬇️ Download TXT",
            data=txt_data,
            file_name=f"{document_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with d2:

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_data,
            file_name=f"{document_name}.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with d3:

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name=f"{document_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
<div style="text-align:center;color:#888;">
LegalEase • AI-Powered Legal Document Generator
<br>
AI-generated drafts should be reviewed by a qualified legal professional.
</div>
""",
    unsafe_allow_html=True,
)