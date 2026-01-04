#!/usr/bin/env python3
"""
QR Code Generator for St. Anthony Volunteer System
This script generates QR codes for punch in/out that volunteers can scan
"""

import argparse
import socket
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def create_qr_code(url, filename, title):
    """Generate QR code with title"""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    # Ensure QR image is in RGB mode before pasting onto an RGB background
    try:
        qr_img = qr_img.convert("RGB")
    except Exception:
        pass
    
    # Create a larger image with title
    img_width = 400
    img_height = 500
    img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Paste QR code in center
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_x = (img_width - qr_size) // 2
    qr_y = 80
    img.paste(qr_img, (qr_x, qr_y))
    
    # Add title text
    draw = ImageDraw.Draw(img)
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 20), title, fill="black", font=font_large)
    
    # Instructions
    instructions = [
        "1. Scan this QR code with your phone camera",
        "2. Fill in your name ",
        "3. Complete the punch in/out process",
        "",
        "St. Anthony Coptic Orthodox Church",
        "Volunteer System"
    ]
    
    y_pos = qr_y + qr_size + 20
    for instruction in instructions:
        if instruction:  # Skip empty lines
            inst_bbox = draw.textbbox((0, 0), instruction, font=font_small)
            inst_width = inst_bbox[2] - inst_bbox[0]
            inst_x = (img_width - inst_width) // 2
            draw.text((inst_x, y_pos), instruction, fill="black", font=font_small)
        y_pos += 25
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Generated: {filename}")

def create_single_qr_pdf(qr_file, title, color_theme, base_url, output_file):
    """Create a single QR code PDF layout"""
    
    # Create PDF canvas
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    # Color schemes
    if color_theme == "green":
        theme_color = (0.16, 0.65, 0.27)  # Green
        bg_color = (0.97, 1.0, 0.97)      # Light green
        accent_color = (0.08, 0.35, 0.15)  # Dark green
    else:  # red
        theme_color = (0.86, 0.21, 0.27)  # Red
        bg_color = (1.0, 0.97, 0.97)      # Light red
        accent_color = (0.45, 0.11, 0.15)  # Dark red
    
    # Background
    c.setFillColorRGB(*bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Title
    c.setFillColorRGB(*accent_color)
    c.setFont("Helvetica-Bold", 32)
    title_width = c.stringWidth(title, "Helvetica-Bold", 32)
    c.drawString((width - title_width) / 2, height - 1.2*inch, title)
    
    # Subtitle
    c.setFont("Helvetica", 18)
    subtitle_text = "St. Anthony Volunteer System"
    subtitle_width = c.stringWidth(subtitle_text, "Helvetica", 18)
    c.drawString((width - subtitle_width) / 2, height - 1.8*inch, subtitle_text)
    
    # Main QR Code section with border
    qr_section_size = 5*inch
    qr_x = (width - qr_section_size) / 2
    qr_y = (height - qr_section_size) / 2 - 0.5*inch
    
    # Draw decorative border
    c.setStrokeColorRGB(*theme_color)
    c.setLineWidth(4)
    c.rect(qr_x - 0.3*inch, qr_y - 0.3*inch, qr_section_size + 0.6*inch, qr_section_size + 0.6*inch, fill=0, stroke=1)
    
    # Add QR code image
    if os.path.exists(qr_file):
        qr_size = 4*inch
        qr_img_x = qr_x + (qr_section_size - qr_size) / 2
        qr_img_y = qr_y + (qr_section_size - qr_size) / 2
        c.drawImage(qr_file, qr_img_x, qr_img_y, width=qr_size, height=qr_size)
    
    # Instructions
    instructions = [
        "Instructions:",
        "1. Point your phone camera at the QR code above",
        "2. Tap the notification to open the volunteer system",
        "3. Enter your full name when prompted",
        "4. Complete the process to record your time",
        "",
        f"Direct URL: {base_url}"
    ]
    
    c.setFillColorRGB(*accent_color)
    y_pos = qr_y - 0.8*inch
    for i, instruction in enumerate(instructions):
        if instruction.startswith("Instructions:"):
            c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(*accent_color)
        elif instruction.startswith("Direct URL:"):
            c.setFont("Helvetica", 12)
            c.setFillColorRGB(0.3, 0.3, 0.3)
        else:
            c.setFont("Helvetica", 14)
            c.setFillColorRGB(0.1, 0.1, 0.1)
        
        if instruction:
            inst_width = c.stringWidth(instruction, "Helvetica", 14)
            c.drawString((width - inst_width) / 2, y_pos, instruction)
        y_pos -= 0.3*inch
    
    # Footer
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica", 10)
    footer_text = "St. Anthony Coptic Orthodox Church - Generated " + str(os.popen('date +"%B %d, %Y"').read().strip())
    footer_width = c.stringWidth(footer_text, "Helvetica", 10)
    c.drawString((width - footer_width) / 2, 0.5*inch, footer_text)
    
    # Save PDF
    c.save()
    print(f"📄 Generated single PDF: {output_file}")

def create_printable_pdf(punch_in_file, punch_out_file, base_url, output_file="qr_codes/volunteer_qr_codes.pdf"):
    """Create a printable PDF layout with both QR codes"""
    
    # Create PDF canvas
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    title_text = "St. Anthony Volunteer System"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 24)
    c.drawString((width - title_width) / 2, height - 1*inch, title_text)
    
    # Subtitle
    c.setFont("Helvetica", 16)
    subtitle_text = "QR Code Punch In/Out System"
    subtitle_width = c.stringWidth(subtitle_text, "Helvetica", 16)
    c.drawString((width - subtitle_width) / 2, height - 1.5*inch, subtitle_text)
    
    # Instructions
    c.setFont("Helvetica", 12)
    instructions = [
        "Instructions for Volunteers:",
        "1. Scan the appropriate QR code below with your phone camera",
        "2. Fill in your name and select your service area",
        "3. Complete the punch in/out process",
        "",
        f"App URL: {base_url}"
    ]
    
    y_pos = height - 2.2*inch
    for instruction in instructions:
        if instruction.startswith("Instructions"):
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 12)
        
        if instruction:  # Skip empty lines for spacing
            inst_width = c.stringWidth(instruction, "Helvetica", 12)
            c.drawString((width - inst_width) / 2, y_pos, instruction)
        y_pos -= 0.25*inch
    
    # QR Code sections
    qr_section_width = 3.5*inch
    qr_section_height = 4*inch
    left_x = (width / 4) - (qr_section_width / 2)
    right_x = (3 * width / 4) - (qr_section_width / 2)
    qr_y = y_pos - qr_section_height - 0.5*inch
    
    # Draw section borders
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(1)
    c.rect(left_x, qr_y, qr_section_width, qr_section_height)
    c.rect(right_x, qr_y, qr_section_width, qr_section_height)
    
    # Punch In section (left)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 18)
    punch_in_text = "🟢 PUNCH IN"
    punch_in_width = c.stringWidth(punch_in_text, "Helvetica-Bold", 18)
    c.drawString(left_x + (qr_section_width - punch_in_width) / 2, qr_y + qr_section_height - 0.5*inch, punch_in_text)
    
    # Add QR code image (Punch In)
    if os.path.exists(punch_in_file):
        qr_size = 2.5*inch
        qr_x = left_x + (qr_section_width - qr_size) / 2
        qr_img_y = qr_y + (qr_section_height - qr_size) / 2
        c.drawImage(punch_in_file, qr_x, qr_img_y, width=qr_size, height=qr_size)
    
    # Punch Out section (right)
    c.setFont("Helvetica-Bold", 18)
    punch_out_text = "🔴 PUNCH OUT"
    punch_out_width = c.stringWidth(punch_out_text, "Helvetica-Bold", 18)
    c.drawString(right_x + (qr_section_width - punch_out_width) / 2, qr_y + qr_section_height - 0.5*inch, punch_out_text)
    
    # Add QR code image (Punch Out)
    if os.path.exists(punch_out_file):
        qr_size = 2.5*inch
        qr_x = right_x + (qr_section_width - qr_size) / 2
        qr_img_y = qr_y + (qr_section_height - qr_size) / 2
        c.drawImage(punch_out_file, qr_x, qr_img_y, width=qr_size, height=qr_size)
    
    # Footer
    c.setFont("Helvetica", 10)
    footer_text = "St. Anthony Coptic Orthodox Church - Generated on " + str(os.popen('date').read().strip())
    footer_width = c.stringWidth(footer_text, "Helvetica", 10)
    c.drawString((width - footer_width) / 2, 0.5*inch, footer_text)
    
    # Save PDF
    c.save()
    print(f"📄 Generated printable PDF: {output_file}")

def main():
    """Generate QR codes for punch in/out"""
    parser = argparse.ArgumentParser(description="Generate QR codes for St. Anthony Volunteer System")
    parser.add_argument("--base-url", dest="base_url", help="Base URL to encode in the QR codes (overrides --lan)")
    parser.add_argument("--lan", dest="use_lan", action="store_true", help="Use local LAN IP (http://<local-ip>:8501) so phones on the same network can reach your app")
    parser.add_argument("--port", dest="port", type=int, default=8501, help="Port used by your Streamlit app (default: 8501)")
    parser.add_argument("--pdf", dest="generate_pdf", action="store_true", help="Generate a printable PDF layout with both QR codes")
    parser.add_argument("--pdf-only", dest="pdf_only", action="store_true", help="Generate only the PDF (skip individual PNG files)")
    parser.add_argument("--separate-pdfs", dest="separate_pdfs", action="store_true", help="Generate separate PDF files for punch in and punch out")
    parser.add_argument("--separate-pdfs-only", dest="separate_pdfs_only", action="store_true", help="Generate only separate PDFs (no PNGs or combined PDF)")
    args = parser.parse_args()

    # Determine base URL
    base_url = "http://localhost:8501"  # default
    if args.base_url:
        base_url = args.base_url
    elif args.use_lan:
        # Get local IP address on LAN
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # doesn't actually send data
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            base_url = f"http://{local_ip}:{args.port}"
        except Exception:
            print("⚠️  Could not determine local IP — falling back to localhost")
            base_url = f"http://localhost:{args.port}"
    
    # You can also use your deployed URL like:
    # base_url = "https://your-app-name.streamlit.app"
    
    punch_in_url = f"{base_url}?action=punch_in"
    punch_out_url = f"{base_url}?action=punch_out"
    
    print("🏗️ Generating QR codes for St. Anthony Volunteer System...")
    print(f"📍 Base URL: {base_url}")
    print()
    
    # Create QR codes directory
    os.makedirs("qr_codes", exist_ok=True)
    
    # Generate individual PNG files (unless pdf-only or separate-pdfs-only mode)
    if not args.pdf_only and not args.separate_pdfs_only:
        # Generate QR codes
        create_qr_code(
            punch_in_url, 
            "qr_codes/punch_in_qr.png", 
            "🟢 PUNCH IN"
        )
        
        create_qr_code(
            punch_out_url, 
            "qr_codes/punch_out_qr.png", 
            "🔴 PUNCH OUT"
        )
    elif args.pdf_only or args.separate_pdfs_only:
        # Generate PNGs temporarily for PDF creation
        create_qr_code(punch_in_url, "qr_codes/temp_punch_in.png", "🟢 PUNCH IN")
        create_qr_code(punch_out_url, "qr_codes/temp_punch_out.png", "🔴 PUNCH OUT")
    
    # Generate combined PDF if requested
    if args.generate_pdf or args.pdf_only:
        punch_in_file = "qr_codes/temp_punch_in.png" if (args.pdf_only or args.separate_pdfs_only) else "qr_codes/punch_in_qr.png"
        punch_out_file = "qr_codes/temp_punch_out.png" if (args.pdf_only or args.separate_pdfs_only) else "qr_codes/punch_out_qr.png"
        
        create_printable_pdf(
            punch_in_file,
            punch_out_file,
            base_url,
            "qr_codes/volunteer_qr_codes.pdf"
        )
    
    # Generate separate PDFs if requested
    if args.separate_pdfs or args.separate_pdfs_only:
        punch_in_file = "qr_codes/temp_punch_in.png" if (args.pdf_only or args.separate_pdfs_only) else "qr_codes/punch_in_qr.png"
        punch_out_file = "qr_codes/temp_punch_out.png" if (args.pdf_only or args.separate_pdfs_only) else "qr_codes/punch_out_qr.png"
        
        # Create separate punch in PDF
        create_single_qr_pdf(
            punch_in_file,
            "🟢 PUNCH IN",
            "green",
            punch_in_url,
            "qr_codes/punch_in.pdf"
        )
        
        # Create separate punch out PDF
        create_single_qr_pdf(
            punch_out_file,
            "🔴 PUNCH OUT",
            "red",
            punch_out_url,
            "qr_codes/punch_out.pdf"
        )
        
    # Clean up temporary files
    if args.pdf_only or args.separate_pdfs_only:
        try:
            os.remove("qr_codes/temp_punch_in.png")
            os.remove("qr_codes/temp_punch_out.png")
        except OSError:
            pass
    
    print()
    print("🎉 QR codes generated successfully!")
    
    if not args.pdf_only and not args.separate_pdfs_only:
        print("📁 Individual PNG files in 'qr_codes' folder:")
        print("   • punch_in_qr.png")
        print("   • punch_out_qr.png")
    
    if args.generate_pdf or args.pdf_only:
        print("📄 Combined PDF layout:")
        print("   • volunteer_qr_codes.pdf")
    
    if args.separate_pdfs or args.separate_pdfs_only:
        print("📄 Separate PDF files:")
        print("   • punch_in.pdf (Green theme - for punch in stations)")
        print("   • punch_out.pdf (Red theme - for punch out stations)")
    
    print()
    print("📋 Next steps:")
    if args.separate_pdfs or args.separate_pdfs_only:
        print("   1. Print punch_in.pdf and post at entry/start stations")
        print("   2. Print punch_out.pdf and post at exit/end stations")
        print("   3. Volunteers scan the appropriate QR code")
        print("   4. Each QR code takes them directly to the right action")
    elif args.generate_pdf or args.pdf_only:
        print("   1. Print the PDF file (volunteer_qr_codes.pdf)")
        print("   2. Post the printed sheet at volunteer stations")
        print("   3. Volunteers scan the appropriate QR code to punch in/out")
    else:
        print("   1. Print these QR codes")
        print("   2. Post them at volunteer stations")
        print("   3. Volunteers scan to punch in/out")
    print("   5. Update base_url in this script when you deploy")

if __name__ == "__main__":
    main()