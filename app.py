with col_b:
        if HAS_DOCX:
            doc = Document()
            doc.add_heading("Global Professional Services Hub", level=1)
            doc.add_heading(f"Service Category: {service_choice}", level=2)
            doc.add_paragraph(output_text)
            doc.add_paragraph("\n--- Verified Agency Payment & Bank Details ---\nCBE Leamare Branch (Addis Ababa): 1000296269488\nTelebirr Wallet: 0916884912 | Holder: Belayhun Adefrese Metaferia")
            
            doc_io = io.BytesIO()
            doc.save(doc_io)
            doc_io.seek(0)

            str_lit.download_button(
                label="📝 Download Formatted Document (.DOCX)",
                data=doc_io,
                file_name="professional_deliverable.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            str_lit.info("Word document exporter loading...")
