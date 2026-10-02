import time

from services.resume_parser import extract_text_from_pdf
from services.resume_extractor import extract_resume_data


pdf_path = r"C:\Users\Likhita\Downloads\likky_resume 1st (2).pdf"

print("\n===== RESUME PROCESSING PERFORMANCE TEST =====")

start_time = time.perf_counter()

text = extract_text_from_pdf(pdf_path)

text_extraction_time = time.perf_counter()

resume_data = extract_resume_data(text)

end_time = time.perf_counter()

text_time = text_extraction_time - start_time
total_time = end_time - start_time

print("\nText extraction time:",
      round(text_time * 1000, 2), "ms")

print("Total resume processing time:",
      round(total_time * 1000, 2), "ms")

print("\nResume processing completed successfully.")
print("Extracted fields:", resume_data)