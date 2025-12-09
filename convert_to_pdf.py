"""
Convert PROJECT_REPORT.md to PDF
"""
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF"""
    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'tables', 'codehilite'])
        
        # Add CSS styling for better PDF appearance
        css_style = """
        <style>
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }
            h1 {
                font-size: 24pt;
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
                page-break-after: avoid;
            }
            h2 {
                font-size: 18pt;
                color: #34495e;
                margin-top: 25px;
                page-break-after: avoid;
            }
            h3 {
                font-size: 14pt;
                color: #555;
                margin-top: 20px;
                page-break-after: avoid;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                page-break-inside: avoid;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
                page-break-inside: avoid;
            }
            blockquote {
                border-left: 4px solid #3498db;
                padding-left: 15px;
                margin: 15px 0;
                color: #666;
            }
            ul, ol {
                margin: 10px 0;
                padding-left: 30px;
            }
            li {
                margin: 5px 0;
            }
            hr {
                border: none;
                border-top: 2px solid #ecf0f1;
                margin: 30px 0;
            }
            .page-break {
                page-break-before: always;
            }
        </style>
        """
        
        # Combine HTML
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {css_style}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        HTML(string=full_html).write_pdf(pdf_file)
        print(f"✅ Successfully converted {md_file} to {pdf_file}")
        return True
        
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("Installing required packages...")
        return False
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # Try to install required packages
    try:
        import markdown
        from weasyprint import HTML
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "weasyprint"])
        import markdown
        from weasyprint import HTML
    
    # Convert
    success = convert_markdown_to_pdf("PROJECT_REPORT.md", "PROJECT_REPORT.pdf")
    
    if success:
        print("\n📄 PDF file created: PROJECT_REPORT.pdf")
    else:
        print("\n⚠️  PDF conversion failed. Trying alternative method...")
        # Alternative: Create HTML file
        try:
            with open("PROJECT_REPORT.md", 'r', encoding='utf-8') as f:
                md_content = f.read()
            html_content = markdown.markdown(md_content, extensions=['extra', 'tables'])
            with open("PROJECT_REPORT.html", 'w', encoding='utf-8') as f:
                f.write(f"<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Project Report</title></head><body>{html_content}</body></html>")
            print("✅ Created PROJECT_REPORT.html - You can open this in a browser and print to PDF")
        except Exception as e:
            print(f"❌ Error: {e}")

