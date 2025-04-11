from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from django.conf import settings
import os

def generate_receipt(order):
    filename = f"receipt_{order.id}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, 'receipts', filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Store Information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, height-20*mm, "PHARMORE DRUGSTORE")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, height-25*mm, "123 Health Street")
    c.drawString(20*mm, height-30*mm, "New Delhi, India 110001")
    c.drawString(20*mm, height-35*mm, "Phone: +91 11 2345 6789")
    
    # Receipt Header
    c.line(20*mm, height-40*mm, width-20*mm, height-40*mm)
    c.setFont("Courier-Bold", 12)
    c.drawString(20*mm, height-45*mm, "RECEIPT")
    c.setFont("Courier", 10)
    c.drawString(20*mm, height-50*mm, f"Date: {order.created_at.strftime('%d/%m/%Y %H:%M')}")
    c.drawString(20*mm, height-55*mm, f"Order ID: #{order.id}")
    
    # Items Table
    y = height - 65*mm
    c.setFont("Courier-Bold", 10)
    c.drawString(20*mm, y, "ITEM")
    c.drawString(100*mm, y, "QTY")
    c.drawString(130*mm, y, "PRICE")
    c.drawString(160*mm, y, "TOTAL")
    
    y -= 5*mm
    c.line(20*mm, y, width-20*mm, y)
    y -= 7*mm
    
    c.setFont("Courier", 10)
    for item in order.orderitem_set.all():
        c.drawString(22*mm, y, item.item.name[:25])
        c.drawString(102*mm, y, str(item.quantity))
        c.drawString(132*mm, y, f"₹{item.price:.2f}")
        c.drawString(162*mm, y, f"₹{item.price * item.quantity:.2f}")
        y -= 5*mm
    
    # Total
    y -= 5*mm
    c.line(20*mm, y, width-20*mm, y)
    y -= 7*mm
    c.setFont("Courier-Bold", 12)
    c.drawString(140*mm, y, "TOTAL:")
    c.drawString(160*mm, y, f"₹{order.total_price:.2f}")
    
    # Footer
    y -= 15*mm
    c.setFont("Courier-Oblique", 8)
    c.drawString(20*mm, y, "Thank you for choosing Pharmore!")
    y -= 5*mm
    c.drawString(20*mm, y, "** Medicines once sold cannot be returned **")
    y -= 5*mm
    c.drawString(20*mm, y, "GSTIN: 07AAACP8819J1Z1")
    
    c.save()
    return filename