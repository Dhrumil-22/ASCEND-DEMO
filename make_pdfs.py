import markdown
from xhtml2pdf import pisa
import os

# Define input paths (Artifacts)
summary_path = r"C:\Users\91940\.gemini\antigravity\brain\812cffc3-b5e6-4226-b5fe-010ff63812a3\project_summary.md"
sitemap_path = r"C:\Users\91940\.gemini\antigravity\brain\812cffc3-b5e6-4226-b5fe-010ff63812a3\ui_sitemap.md"

# Define output paths (Current Directory)
summary_out = "ASCEND_Project_Summary.pdf"
sitemap_out = "ASCEND_UI_Sitemap.pdf"

def convert_md_to_pdf(input_path, output_path):
    print(f"Converting {input_path} to {output_path}...")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        # Convert MD to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Add basic styling
        full_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Helvetica, sans-serif; font-size: 12pt; }}
                h1 {{ color: #2563EB; border-bottom: 2px solid #2563EB; padding-bottom: 10px; }}
                h2 {{ color: #10B981; margin-top: 20px; }}
                h3 {{ color: #4B5563; }}
                code {{ background-color: #F3F4F6; padding: 2px 4px; border-radius: 4px; font-family: Courier New, monospace; }}
                pre {{ background-color: #F3F4F6; padding: 10px; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .shadow {{ box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        with open(output_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)
            
        if pisa_status.err:
            print(f"Error converting {input_path}")
        else:
            print(f"Successfully created {output_path}")
            
    except Exception as e:
        print(f"Failed to convert: {str(e)}")

# Run conversions
convert_md_to_pdf(summary_path, summary_out)
convert_md_to_pdf(sitemap_path, sitemap_out)
