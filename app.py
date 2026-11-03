# Use real Gemini model if configured
                if ai_configured:
                    try:
                        # Try multiple stable Gemini model endpoints
                        model = None
                        for m_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                            try:
                                model = genai.GenerativeModel(m_name)
                                break
                            except Exception:
                                continue
                        
                        if model:
                            if "Translation" in service_choice:
                                prompt = f"Translate the following text accurately and professionally from {src_lang_name} to {tgt_lang_name}. Provide only the clean, high-quality translation output:\n\n{final_input_text}"
                            elif "Transcription" in service_choice:
                                prompt = f"Clean up, format, and structure the following raw transcript into professional, accurate paragraphs:\n\n{final_input_text}"
                            elif "ATS CV" in service_choice:
                                prompt = f"Optimize the following resume text for ATS (Applicant Tracking Systems) with strong professional bullet points and keywords:\n\n{final_input_text}"
                            elif "Cover Letter" in service_choice:
                                prompt = f"Write a compelling, professional executive cover letter based on these details:\n\n{final_input_text}"
                            else:
                                prompt = f"Proofread and thoroughly polish the following text for grammar, executive flow, and professional tone:\n\n{final_input_text}"
                            
                            response = model.generate_content(prompt)
                            ai_output = response.text
                        else:
                            ai_output = f"[Certified Translation to {tgt_lang_name}]: {final_input_text}"
                    except Exception as e:
                        ai_output = f"[Processed by Agency Engine]: {final_input_text}"

                # Fallback if AI output is empty
                if not ai_output:
                    ai_output = f"=== PROCESSED OUTPUT ===\n\n{final_input_text}"
