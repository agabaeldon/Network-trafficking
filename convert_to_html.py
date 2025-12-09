"""
Convert PROJECT_REPORT.md to HTML (can be printed to PDF from browser)
"""
import markdown

def convert_markdown_to_html(md_file, html_file):
    """Convert markdown file to styled HTML"""
    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'tables', 'codehilite'])
        
        # Add professional CSS styling
        css_style = """
        <style>
            @media print {
                @page {
                    size: A4;
                    margin: 2cm;
                }
                body {
                    font-size: 11pt;
                }
                h1 {
                    page-break-after: avoid;
                }
                h2 {
                    page-break-after: avoid;
                }
                table {
                    page-break-inside: avoid;
                }
                pre {
                    page-break-inside: avoid;
                }
            }
            
            body {
                font-family: 'Arial', 'Helvetica', sans-serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
            }
            
            h1 {
                font-size: 28pt;
                color: #2c3e50;
                border-bottom: 4px solid #3498db;
                padding-bottom: 15px;
                margin-top: 30px;
                margin-bottom: 20px;
                font-weight: bold;
            }
            
            h2 {
                font-size: 20pt;
                color: #34495e;
                margin-top: 30px;
                margin-bottom: 15px;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 8px;
            }
            
            h3 {
                font-size: 16pt;
                color: #555;
                margin-top: 25px;
                margin-bottom: 12px;
            }
            
            h4 {
                font-size: 14pt;
                color: #666;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            
            th {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                font-size: 11pt;
            }
            
            td {
                background-color: #fff;
            }
            
            tr:nth-child(even) td {
                background-color: #f8f9fa;
            }
            
            code {
                background-color: #f4f4f4;
                padding: 3px 6px;
                border-radius: 3px;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 10pt;
                color: #e83e8c;
            }
            
            pre {
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 4px solid #3498db;
                margin: 15px 0;
            }
            
            pre code {
                background-color: transparent;
                padding: 0;
                color: #333;
            }
            
            blockquote {
                border-left: 4px solid #3498db;
                padding-left: 20px;
                margin: 20px 0;
                color: #666;
                font-style: italic;
            }
            
            ul, ol {
                margin: 15px 0;
                padding-left: 40px;
            }
            
            li {
                margin: 8px 0;
            }
            
            hr {
                border: none;
                border-top: 3px solid #ecf0f1;
                margin: 40px 0;
            }
            
            p {
                margin: 12px 0;
                text-align: justify;
            }
            
            strong {
                color: #2c3e50;
                font-weight: bold;
            }
            
            a {
                color: #3498db;
                text-decoration: none;
            }
            
            a:hover {
                text-decoration: underline;
            }
            
            .print-button {
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: #3498db;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14pt;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .print-button:hover {
                background-color: #2980b9;
            }
            
            @media print {
                .print-button {
                    display: none;
                }
            }
        </style>
        """
        
        # Combine HTML
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Report - Network Traffic Prediction System</title>
    {css_style}
</head>
<body>
    <button class="print-button" onclick="window.print()">🖨️ Print to PDF</button>
    {html_content}
    <script>
        /* Auto-print option (commented out - uncomment if you want auto-print) */
        /* window.onload = function() {{ window.print(); }} */
    </script>
</body>
</html>"""
        
        # Write HTML file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ Successfully converted {md_file} to {html_file}")
        print(f"\n📄 Open {html_file} in your web browser")
        print("🖨️  Click the 'Print to PDF' button or press Ctrl+P")
        print("💾 Select 'Save as PDF' as the printer")
        return True
        
    except Exception as e:
        print(f"❌ Error converting to HTML: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = convert_markdown_to_html("PROJECT_REPORT.md", "PROJECT_REPORT.html")
    
    if success:
        print("\n" + "="*60)
        print("✅ Conversion Complete!")
        print("="*60)
        print("\nTo create PDF:")
        print("1. Open PROJECT_REPORT.html in your web browser")
        print("2. Click the 'Print to PDF' button (top right)")
        print("   OR press Ctrl+P")
        print("3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
        print("4. Click Save")
        print("\nThe PDF will be professionally formatted and ready for submission!")
    else:
        print("\n❌ Conversion failed. Please check the error messages above.")

