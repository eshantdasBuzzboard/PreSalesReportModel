import streamlit as st
import asyncio
from datetime import datetime
from presale_strategy_report import generate_report_async, generate_slide_8_content
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import io
import json

st.title("Presale Strategy Report Generator")

# File uploader
uploaded_file = st.file_uploader("Upload your .txt or .py file", type=["txt", "py"])

if uploaded_file is not None:
    # Read the file
    content = uploaded_file.read().decode("utf-8")

    # Execute the code to load variables
    namespace = {}
    exec(content, namespace)

    # Store all variables
    seller_company_name = namespace.get("seller_company_name", "N/A")
    seller_product_details = namespace.get("seller_product_details", "N/A")
    prospect_company_name = namespace.get("prospect_company_name", "N/A")
    Website_URL = namespace.get("Website_URL", "N/A")
    Website_Content_Scrapped = namespace.get("Website_Content_Scrapped", "N/A")
    BB_Category_Primary = namespace.get("BB_Category_Primary", "N/A")
    BB_Category_Secondary = namespace.get("BB_Category_Secondary", "N/A")
    All_Signals_Data = namespace.get("All_Signals_Data", "N/A")
    Reviews_local_and_social = namespace.get("Reviews_local_and_social", "N/A")

    Business_Name_Comp_1 = namespace.get("Business_Name_Comp_1", "N/A")
    Website_URL_Comp_1 = namespace.get("Website_URL_Comp_1", "N/A")
    Website_Content_Scrapped_Comp_1 = namespace.get(
        "Website_Content_Scrapped_Comp_1", "N/A"
    )
    Competitor_Signals_Comp_1 = namespace.get("Competitor_Signals_Comp_1", "N/A")
    BB_Category_Primary_Comp_1 = namespace.get("BB_Category_Primary_Comp_1", "N/A")
    Reviews_local_and_social_Comp_1 = namespace.get(
        "Reviews_local_and_social_Comp_1", "N/A"
    )
    BB_Category_Secondary_Comp_1 = namespace.get("BB_Category_Secondary_Comp_1", "N/A")

    Business_Name_Comp_2 = namespace.get("Business_Name_Comp_2", "N/A")
    Website_URL_Comp_2 = namespace.get("Website_URL_Comp_2", "N/A")
    Website_Content_Scrapped_Comp_2 = namespace.get(
        "Website_Content_Scrapped_Comp_2", "N/A"
    )
    Competitor_Signals_Comp_2 = namespace.get("Competitor_Signals_Comp_2", "N/A")
    BB_Category_Primary_Comp_2 = namespace.get("BB_Category_Primary_Comp_2", "N/A")
    Reviews_local_and_social_Comp_2 = namespace.get(
        "Reviews_local_and_social_Comp_2", "N/A"
    )
    BB_Category_Secondary_Comp_2 = namespace.get("BB_Category_Secondary_Comp_2", "N/A")

    Business_Name_Comp_3 = namespace.get("Business_Name_Comp_3", "N/A")
    Website_URL_Comp_3 = namespace.get("Website_URL_Comp_3", "N/A")
    Website_Content_Scrapped_Comp_3 = namespace.get(
        "Website_Content_Scrapped_Comp_3", "N/A"
    )
    Competitor_Signals_Comp_3 = namespace.get("Competitor_Signals_Comp_3", "N/A")
    BB_Category_Primary_Comp_3 = namespace.get("BB_Category_Primary_Comp_3", "N/A")
    Reviews_local_and_social_Comp_3 = namespace.get(
        "Reviews_local_and_social_Comp_3", "N/A"
    )
    BB_Category_Secondary_Comp_3 = namespace.get("BB_Category_Secondary_Comp_3", "N/A")

    slide_8_input_content = namespace.get("slide_8_input_content", "N/A")

    # Button to generate report
    st.subheader("Generate Report")
    if st.button("Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            try:
                result = asyncio.run(
                    generate_report_async(
                        seller_company_name,
                        seller_product_details,
                        prospect_company_name,
                        Website_URL,
                        Website_Content_Scrapped,
                        BB_Category_Primary,
                        BB_Category_Secondary,
                        All_Signals_Data,
                        Reviews_local_and_social,
                        Business_Name_Comp_1,
                        Website_URL_Comp_1,
                        Website_Content_Scrapped_Comp_1,
                        Competitor_Signals_Comp_1,
                        BB_Category_Primary_Comp_1,
                        Reviews_local_and_social_Comp_1,
                        BB_Category_Secondary_Comp_1,
                        Business_Name_Comp_2,
                        Website_URL_Comp_2,
                        Website_Content_Scrapped_Comp_2,
                        Competitor_Signals_Comp_2,
                        BB_Category_Primary_Comp_2,
                        Reviews_local_and_social_Comp_2,
                        BB_Category_Secondary_Comp_2,
                        Business_Name_Comp_3,
                        Website_URL_Comp_3,
                        Website_Content_Scrapped_Comp_3,
                        Competitor_Signals_Comp_3,
                        BB_Category_Primary_Comp_3,
                        Reviews_local_and_social_Comp_3,
                        BB_Category_Secondary_Comp_3,
                    )
                )

                # Unpack results
                (
                    report_json,
                    Business_Overview,
                    SWOT_Analysis,
                    Customer_Sentiment,
                    Competitive_Benchmarking,
                    ROI_Impact_Projections,
                    Recommendations,
                    report,
                    executive_summary,
                ) = result

                st.success("✅ Report generated successfully!")

                # Store in session state for PDF generation
                st.session_state.report_data = {
                    "report_json": report_json,
                    "Business_Overview": Business_Overview,
                    "SWOT_Analysis": SWOT_Analysis,
                    "Customer_Sentiment": Customer_Sentiment,
                    "Competitive_Benchmarking": Competitive_Benchmarking,
                    "ROI_Impact_Projections": ROI_Impact_Projections,
                    "Recommendations": Recommendations,
                    "report": report,
                    "executive_summary": executive_summary,
                }

            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")

        # Generate Slide 8 content
        with st.spinner("Generating Target Audience content..."):
            try:
                target_audience = asyncio.run(
                    generate_slide_8_content(slide_8_input_content)
                )
                st.session_state.report_data["target_audience"] = target_audience
                st.success("✅ Target Audience content generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating target audience: {str(e)}")

    # Display results if available
    if "report_data" in st.session_state:
        st.markdown("---")
        st.header("📊 Report Results")

        data = st.session_state.report_data

        # Executive Summary
        st.subheader("📄 Executive Summary")
        st.write(data.get("executive_summary", "N/A"))

        st.markdown("---")

        # Business Overview
        st.subheader("🏢 Business Overview")
        st.write(data.get("Business_Overview", "N/A"))

        st.markdown("---")

        # SWOT Analysis
        st.subheader("📈 SWOT Analysis")
        st.write(data.get("SWOT_Analysis", "N/A"))

        st.markdown("---")

        # Customer Sentiment
        st.subheader("💬 Customer Sentiment")
        st.write(data.get("Customer_Sentiment", "N/A"))

        st.markdown("---")

        # Competitive Benchmarking
        st.subheader("🎯 Competitive Benchmarking")
        st.write(data.get("Competitive_Benchmarking", "N/A"))

        st.markdown("---")

        # ROI Impact Projections
        st.subheader("💰 ROI Impact Projections")
        st.write(data.get("ROI_Impact_Projections", "N/A"))

        st.markdown("---")

        # Recommendations
        st.subheader("✨ Recommendations")
        st.write(data.get("Recommendations", "N/A"))

        st.markdown("---")

        # Target Audience
        if "target_audience" in data:
            st.subheader("👥 Target Audience")
            st.write(data.get("target_audience", "N/A"))

            st.markdown("---")

        # Full Report
        st.subheader("📑 Full Report")
        with st.expander("Click to view full report"):
            st.write(data.get("report", "N/A"))

        # Report JSON
        st.subheader("🔧 Report JSON")
        with st.expander("Click to view report JSON"):
            st.json(data.get("report_json", {}))

        # PDF Download Button
        st.markdown("---")
        st.subheader("⬇️ Download Report")

        def create_pdf(data):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            # Container for the 'Flowable' objects
            elements = []

            # Define styles
            styles = getSampleStyleSheet()
            styles.add(
                ParagraphStyle(
                    name="CustomTitle",
                    parent=styles["Heading1"],
                    fontSize=24,
                    textColor="#1f4788",
                    spaceAfter=30,
                    alignment=TA_CENTER,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="CustomHeading",
                    parent=styles["Heading2"],
                    fontSize=16,
                    textColor="#1f4788",
                    spaceAfter=12,
                    spaceBefore=12,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="CustomBody",
                    parent=styles["BodyText"],
                    fontSize=11,
                    alignment=TA_JUSTIFY,
                    spaceAfter=12,
                )
            )

            # Helper function to clean and format text
            def clean_text(text):
                if text is None:
                    return "N/A"
                if isinstance(text, dict):
                    text = json.dumps(text, indent=2)
                text = str(text)
                # Replace problematic characters
                text = text.replace("&", "&amp;")
                text = text.replace("<", "&lt;")
                text = text.replace(">", "&gt;")
                # Replace smart quotes and dashes with regular ones
                text = text.replace("\u2018", "'").replace("\u2019", "'")
                text = text.replace("\u201c", '"').replace("\u201d", '"')
                text = text.replace("\u2013", "-").replace("\u2014", "-")
                text = text.replace("\u2022", "*")  # bullet points
                return text

            # Add title
            title = Paragraph("Presale Strategy Report", styles["CustomTitle"])
            elements.append(title)
            elements.append(Spacer(1, 0.3 * inch))

            # Add sections
            sections = [
                ("Executive Summary", data.get("executive_summary")),
                ("Business Overview", data.get("Business_Overview")),
                ("SWOT Analysis", data.get("SWOT_Analysis")),
                ("Customer Sentiment", data.get("Customer_Sentiment")),
                ("Competitive Benchmarking", data.get("Competitive_Benchmarking")),
                ("ROI Impact Projections", data.get("ROI_Impact_Projections")),
                ("Recommendations", data.get("Recommendations")),
            ]

            if "target_audience" in data:
                sections.append(("Target Audience", data.get("target_audience")))

            sections.append(("Full Report", data.get("report")))

            for section_title, section_content in sections:
                # Add section heading
                heading = Paragraph(section_title, styles["CustomHeading"])
                elements.append(heading)

                # Add section content
                cleaned_content = clean_text(section_content)

                # Split into paragraphs and add each
                paragraphs = cleaned_content.split("\n\n")
                for para in paragraphs:
                    if para.strip():
                        # Handle bullet points
                        lines = para.split("\n")
                        for line in lines:
                            if line.strip():
                                p = Paragraph(line, styles["CustomBody"])
                                elements.append(p)

                elements.append(Spacer(1, 0.2 * inch))

            # Build PDF
            doc.build(elements)

            # Get the value of the BytesIO buffer
            pdf_data = buffer.getvalue()
            buffer.close()

            return pdf_data

        try:
            pdf_data = create_pdf(st.session_state.report_data)

            st.download_button(
                label="📥 Download Full Report as PDF",
                data=pdf_data,
                file_name=f"presale_strategy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="primary",
            )
        except Exception as e:
            st.error(f"Error creating PDF: {str(e)}")
            st.info(
                "You can copy the content from the sections above if PDF generation fails."
            )

else:
    st.info("👆 Please upload a .txt or .py file to get started")
