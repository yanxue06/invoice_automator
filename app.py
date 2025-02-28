import tkinter as tk
from tkinter import ttk, Text, messagebox
import json
from datetime import datetime, timedelta
import os
from jinja2 import Template
from xhtml2pdf import pisa  

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SKYNET Invoice Generator")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        
        # Create main container with scrollbar support
        main_container = ttk.Frame(root)
        main_container.pack(fill="both", expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame for content
        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TEntry", padding=5)
        style.configure("TButton", padding=5)
        style.configure("Save.TButton",
                       padding=10,
                       font=("Arial", 11, "bold"))
        
        # Company Header Frame
        self.header_frame = ttk.Frame(content_frame)
        self.header_frame.pack(fill="x", padx=10, pady=5)
        
        # SKYNET Logo (as text for now)
        title_label = ttk.Label(self.header_frame, text="SKYNET", font=("Arial", 24, "bold"))
        title_label.pack(side="left")
        
        invoice_label = ttk.Label(self.header_frame, text="INVOICE", font=("Arial", 18), foreground="orange")
        invoice_label.pack(side="right")
        
        # Company Information Frame
        self.company_frame = ttk.Frame(content_frame)
        self.company_frame.pack(fill="x", padx=10)
        
        company_info = [
            "Skynet security system ltd",
            "98 Fell ave, Burnaby,BC, Canada V5B 3Y2",
            "PHONE: (778) 322-7655",
            "Vanipcamera@gmail.com"
        ]
        
        for info in company_info:
            ttk.Label(self.company_frame, text=info).pack(anchor="e")
        
        # Vendor Info Frame
        self.vendor_frame = ttk.Frame(content_frame)
        self.vendor_frame.pack(fill="x", padx=10)
        
        vendor_left = ttk.Frame(self.vendor_frame)
        vendor_left.pack(side="left")
        
        vendor_right = ttk.Frame(self.vendor_frame)
        vendor_right.pack(side="right")
        
        ttk.Label(vendor_right, text="Vendor number:").grid(row=0, column=0, sticky="e")
        self.vendor_number = ttk.Entry(vendor_right, width=15)
        self.vendor_number.grid(row=0, column=1)
        self.vendor_number.insert(0, "130304")
        
        ttk.Label(vendor_right, text="BN:").grid(row=1, column=0, sticky="e")
        self.bn = ttk.Entry(vendor_right, width=15)
        self.bn.grid(row=1, column=1)
        self.bn.insert(0, "817500390BC0001")
        
        # Bill To Frame
        self.bill_frame = ttk.LabelFrame(content_frame, text="BILL TO", padding=10)
        self.bill_frame.pack(fill="x", padx=10, pady=5)
        
        # Left side billing info
        bill_left = ttk.Frame(self.bill_frame)
        bill_left.pack(side="left", fill="x", expand=True)
        
        self.bill_company = ttk.Entry(bill_left, width=40)
        self.bill_company.pack(fill="x")
        
        self.bill_contact = ttk.Entry(bill_left, width=40)
        self.bill_contact.pack(fill="x")
        
        self.bill_address = ttk.Entry(bill_left, width=40)
        self.bill_address.pack(fill="x")
        
        self.bill_street = ttk.Entry(bill_left, width=40)
        self.bill_street.pack(fill="x")
        
        self.bill_phone = ttk.Entry(bill_left, width=40)
        self.bill_phone.pack(fill="x")
        
        self.bill_email = ttk.Entry(bill_left, width=40)
        self.bill_email.pack(fill="x")
        
        # Right side invoice details
        bill_right = ttk.Frame(self.bill_frame)
        bill_right.pack(side="right")
        
        ttk.Label(bill_right, text="INVOICE NBR:").grid(row=0, column=0, sticky="e")
        self.invoice_number = ttk.Entry(bill_right, width=15)
        self.invoice_number.grid(row=0, column=1)
        
        ttk.Label(bill_right, text="INVOICE DATE:").grid(row=1, column=0, sticky="e")
        self.invoice_date = ttk.Entry(bill_right, width=15)
        self.invoice_date.grid(row=1, column=1)
        self.invoice_date.insert(0, datetime.now().strftime("%b %d,%Y"))
        
        ttk.Label(bill_right, text="PAYMENT DUE DATE:").grid(row=2, column=0, sticky="e")
        self.due_date = ttk.Entry(bill_right, width=15)
        self.due_date.grid(row=2, column=1)
        self.due_date.insert(0, (datetime.now() + timedelta(days=11)).strftime("%b %d,%Y"))
        
        # Items Frame
        self.items_frame = ttk.LabelFrame(content_frame, text="Items", padding=10)
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Items Header
        columns = ('ITEMS', 'ORDER NUMBER', 'DESCRIPTION', 'QUANTITY', 'PRICE', 'AMOUNT')
        self.tree = ttk.Treeview(self.items_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True)
        
        # Bind Delete key to tree
        self.tree.bind('<Delete>', lambda e: self.delete_item())
        
        # Add Item Frame
        self.add_item_frame = ttk.Frame(self.items_frame)
        self.add_item_frame.pack(fill="x", pady=5)
        
        # Create labels and entries in a more organized way
        entry_labels = ['Item #', 'Order #', 'Description', 'Quantity', 'Price ($)']
        self.entries = {}
        
        for i, label in enumerate(entry_labels):
            # Create label
            ttk.Label(self.add_item_frame, text=label).pack(side="left", padx=(10 if i > 0 else 2))
            # Create and bind entry
            width = 30 if label == 'Description' else (8 if label in ['Item #', 'Quantity'] else 15)
            entry = ttk.Entry(self.add_item_frame, width=width)
            entry.pack(side="left", padx=2)
            entry.bind('<Return>', lambda e: self.add_item())
            self.entries[label] = entry
        
        # Store references for easy access
        self.item_number = self.entries['Item #']
        self.order_number = self.entries['Order #']
        self.description = self.entries['Description']
        self.quantity = self.entries['Quantity']
        self.price = self.entries['Price ($)']
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.items_frame)
        buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(buttons_frame, text="Add Item", command=self.add_item).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Delete Item", command=self.delete_item).pack(side="left", padx=5)
        
        # Totals Frame
        self.totals_frame = ttk.Frame(content_frame)
        self.totals_frame.pack(fill="x", padx=10, pady=5)
        
        totals_right = ttk.Frame(self.totals_frame)
        totals_right.pack(side="right")
        
        # Subtotal
        ttk.Label(totals_right, text="Subtotal:").grid(row=0, column=0, sticky="e")
        self.subtotal_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_right, textvariable=self.subtotal_var).grid(row=0, column=1, padx=10)
        
        # GST
        ttk.Label(totals_right, text="GST 5%:").grid(row=1, column=0, sticky="e")
        self.gst_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_right, textvariable=self.gst_var).grid(row=1, column=1, padx=10)
        
        # Total
        ttk.Label(totals_right, text="Total:").grid(row=2, column=0, sticky="e")
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_right, textvariable=self.total_var).grid(row=2, column=1, padx=10)
        
        # Amount Due
        ttk.Label(totals_right, text="AMOUNT DUE(CAD):").grid(row=3, column=0, sticky="e")
        self.amount_due_var = tk.StringVar(value="$0.00")
        ttk.Label(totals_right, textvariable=self.amount_due_var).grid(row=3, column=1, padx=10)
        
        # Notes Frame
        self.notes_frame = ttk.LabelFrame(content_frame, text="Notes:", padding=10)
        self.notes_frame.pack(fill="x", padx=10, pady=5)
        
        self.notes_text = Text(self.notes_frame, height=4, width=50)
        self.notes_text.pack(fill="x")
        self.notes_text.insert("1.0", "Commercial Insurance: Policy 501406927\nFSR C-R LOW ENERGY CEL00229270\nELECTRONICS Communication Technician BC CERTIFICATE NUMBER 00001-EE-11")
        
        # Save Button - make it more prominent but compact
        save_frame = ttk.Frame(content_frame)
        save_frame.pack(fill="x", padx=10, pady=5)
        
        save_btn = ttk.Button(
            save_frame, 
            text="Save Invoice 📄",  # Changed to a simpler document icon
            command=self.save_invoice,
            style="Save.TButton"
        )
        save_btn.pack(side="right", padx=10, pady=5)
        
        # Update scroll region when content changes
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Bind mouse wheel to scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def add_item(self):
        try:
            item_num = self.item_number.get()
            order_num = self.order_number.get()
            desc = self.description.get()
            qty = float(self.quantity.get() or 0)
            price = float(self.price.get() or 0)
            amount = qty * price
            
            if not all([item_num, order_num, desc]):  # Basic validation
                return
                
            self.tree.insert('', 'end', values=(
                item_num,
                order_num,
                desc,
                qty,
                f"${price:.2f}",
                f"${amount:.2f}"
            ))
            self.update_totals()
            
            # Clear entries
            for entry in [self.item_number, self.order_number, self.description, self.quantity, self.price]:
                entry.delete(0, 'end')
            
            # Set focus to first entry
            self.item_number.focus()
        except ValueError as e:
            print(f"Error adding item: {e}")  # For debugging
            pass
    
    def update_totals(self):
        subtotal = sum(float(self.tree.item(item)['values'][5].replace('$', '')) for item in self.tree.get_children())
        gst = subtotal * 0.05
        total = subtotal + gst
        
        self.subtotal_var.set(f"${subtotal:.2f}")
        self.gst_var.set(f"${gst:.2f}")
        self.total_var.set(f"${total:.2f}")
        self.amount_due_var.set(f"${total:.2f}")
    
    def generate_pdf(self, filename):
        # Read the HTML template
        with open('invoice_template.html', 'r') as f:
            template_str = f.read()
        
        # Create Jinja2 template
        template = Template(template_str)
        
        # Prepare items data
        items_data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            items_data.append({
                'item_number': values[0],
                'order_number': values[1],
                'description': values[2],
                'quantity': values[3],
                'price': values[4],
                'amount': values[5]
            })
        
        # Prepare template data
        template_data = {
            'company_info': {
                'name': "Skynet security system ltd",
                'address': "98 Fell ave, Burnaby,BC, Canada V5B 3Y2",
                'phone': "(778) 322-7655",
                'email': "Vanipcamera@gmail.com"
            },
            'vendor_number': self.vendor_number.get(),
            'bn': self.bn.get(),
            'bill_to': {
                'company': self.bill_company.get(),
                'contact': self.bill_contact.get(),
                'address': self.bill_address.get(),
                'street': self.bill_street.get(),
                'phone': self.bill_phone.get(),
                'email': self.bill_email.get()
            },
            'invoice_number': self.invoice_number.get(),
            'invoice_date': self.invoice_date.get(),
            'due_date': self.due_date.get(),
            'items': items_data,
            'subtotal': self.subtotal_var.get(),
            'gst': self.gst_var.get(),
            'total': self.total_var.get(),
            'amount_due': self.amount_due_var.get(),
            'notes': self.notes_text.get("1.0", "end-1c")
        }
        
        # Render template
        html_out = template.render(**template_data)
        
        # Convert to PDF using xhtml2pdf
        with open(filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_out, dest=pdf_file)
        
        # Return True on success and False on errors
        return pisa_status.err == 0
    
    def save_invoice(self):
        # Get invoice number and date for filename
        invoice_number = self.invoice_number.get()
        invoice_date = datetime.strptime(self.invoice_date.get(), "%b %d,%Y").strftime("%Y%m%d")
        company_name = self.bill_company.get().replace(" ", "_") if self.bill_company.get() else "unnamed"
        
        # Create filename format: SKYNET_INV_[NUMBER]_[DATE]_[COMPANY]
        filename_base = f"SKYNET_INV_{invoice_number}_{invoice_date}_{company_name}"
        
        # Get desktop path
        desktop_path = os.path.expanduser("~/Desktop")
        
        # Create full file paths
        json_path = os.path.join(desktop_path, f"{filename_base}.json")
        pdf_path = os.path.join(desktop_path, f"{filename_base}.pdf")
        
        # Save JSON
        invoice_data = {
            'company_info': {
                'name': "Skynet security system ltd",
                'address': "98 Fell ave, Burnaby,BC, Canada V5B 3Y2",
                'phone': "(778) 322-7655",
                'email': "Vanipcamera@gmail.com"
            },
            'vendor_number': self.vendor_number.get(),
            'bn': self.bn.get(),
            'bill_to': {
                'company': self.bill_company.get(),
                'contact': self.bill_contact.get(),
                'address': self.bill_address.get(),
                'street': self.bill_street.get(),
                'phone': self.bill_phone.get(),
                'email': self.bill_email.get()
            },
            'invoice_number': invoice_number,
            'invoice_date': self.invoice_date.get(),
            'due_date': self.due_date.get(),
            'items': [
                {
                    'item_number': self.tree.item(item)['values'][0],
                    'order_number': self.tree.item(item)['values'][1],
                    'description': self.tree.item(item)['values'][2],
                    'quantity': self.tree.item(item)['values'][3],
                    'price': self.tree.item(item)['values'][4],
                    'amount': self.tree.item(item)['values'][5]
                }
                for item in self.tree.get_children()
            ],
            'subtotal': self.subtotal_var.get(),
            'gst': self.gst_var.get(),
            'total': self.total_var.get(),
            'amount_due': self.amount_due_var.get(),
            'notes': self.notes_text.get("1.0", "end-1c")
        }
        
        try:
            # Save JSON file
            with open(json_path, 'w') as f:
                json.dump(invoice_data, f, indent=4)
            
            # Generate and save PDF
            pdf_success = self.generate_pdf(pdf_path)
            
            if pdf_success:
                # Show success message
                tk.messagebox.showinfo("Success", f"Invoice saved to Desktop:\n{filename_base}.pdf\n{filename_base}.json")
            else:
                tk.messagebox.showwarning("Warning", f"JSON file saved, but there was an issue generating the PDF.\nCheck {filename_base}.json")
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save invoice: {str(e)}")

    def delete_item(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)
        self.update_totals()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
