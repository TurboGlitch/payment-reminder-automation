from fpdf import FPDF


def generate_pdf(client):
    pdf = FPDF()

    pdf.add_page() 
    pdf.set_font("Helvetica", size=26,style="B")
    pdf.cell(0, 50, "Payment Reminder", ln=True, align="C")

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"To: {client["Client Name"]}", ln=True)
    pdf.cell(0, 8, f"Service/Item: {client["Service/Item"]}", ln=True)
    pdf.cell(0, 8, f"Amount Due: {client['Amount']}", ln=True)
    pdf.cell(0, 8, f"Due Date: {client['Due Date']}", ln=True)

    pdf.set_y(-20)
    pdf.set_font("Arial", size=10,style="I")
    pdf.cell(0,0,"Turbo Tech",ln=True,align="C")

    pdf.output(f"output/{client["Client Name"]} Reminder.pdf")

if __name__ == "__main__":
    generate_pdf()