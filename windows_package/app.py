import tkinter as tk
from tkinter import ttk, Text, messagebox
from datetime import datetime, timedelta
import os
import sys
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
        
        # Create canvas with scrollbars
        canvas = tk.Canvas(main_container)
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(main_container, orient="horizontal", command=canvas.xview)
        h_scrollbar.pack(side="bottom", fill="x")
        
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
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
            "SKYNET SECURITY SYSTEM LTD",
            "98 Fell ave, Burnaby,BC, Canada V5B 3Y2",
            "(778) 322-7655",
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
        
        # Bind mouse wheel to scroll - improved cross-platform support
        def _on_mousewheel(event):
            # Get the operating system
            import platform
            os_name = platform.system()
            
            # Check if Shift key is pressed for horizontal scrolling
            if event.state & 0x1:  # Shift key
                # Different handling for different OS
                if os_name == "Linux":
                    if event.num == 4:  # Scroll up/left
                        canvas.xview_scroll(-1, "units")
                    elif event.num == 5:  # Scroll down/right
                        canvas.xview_scroll(1, "units")
                else:  # Windows and macOS
                    # Make scrolling smoother on macOS
                    if os_name == "Darwin":  # macOS
                        canvas.xview_scroll(int(-1*(event.delta)), "units")
                    else:  # Windows
                        canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:  # Vertical scrolling (no Shift key)
                # Different handling for different OS
                if os_name == "Linux":
                    if event.num == 4:  # Scroll up
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:  # Scroll down
                        canvas.yview_scroll(1, "units")
                else:  # Windows and macOS
                    # Make scrolling smoother on macOS
                    if os_name == "Darwin":  # macOS
                        canvas.yview_scroll(int(-1*(event.delta)), "units")
                    else:  # Windows
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind for Windows and macOS
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Shift-MouseWheel>", _on_mousewheel)
        # Additional bindings for Linux
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        canvas.bind_all("<Shift-Button-4>", _on_mousewheel)
        canvas.bind_all("<Shift-Button-5>", _on_mousewheel)
        
    def add_item(self):
        try:
            item_num = self.item_number.get()
            order_num = self.order_number.get()
            desc = self.description.get()
            qty = float(self.quantity.get() or 0)
            price = float(self.price.get() or 0)
            amount = qty * price
            
            if not all([item_num, order_num, desc]):  # Basic validation
                messagebox.showwarning("Validation Error", "Please fill in Item #, Order #, and Description fields.")
                return
            
            # Format values for display
            item_num_str = str(item_num)
            order_num_str = str(order_num)
            desc_str = str(desc)
            qty_str = str(qty)
            price_str = f"${price:.2f}"
            amount_str = f"${amount:.2f}"
            
            # Insert item into tree with proper formatting
            item_id = self.tree.insert('', 'end', values=(
                item_num_str,
                order_num_str,
                desc_str,
                qty_str,
                price_str,
                amount_str
            ))
            
            # Debug: Print the item that was added
            print(f"Added item with ID {item_id}: {item_num_str}, {order_num_str}, {desc_str}, {qty_str}, {price_str}, {amount_str}")
            
            # Verify the item was added correctly
            item_values = self.tree.item(item_id)['values']
            print(f"Verification - Item values in tree: {item_values}")
            
            self.update_totals()
            
            # Clear entries
            for entry in [self.item_number, self.order_number, self.description, self.quantity, self.price]:
                entry.delete(0, 'end')
            
            # Set focus to first entry
            self.item_number.focus()
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check your input values: {str(e)}")
            print(f"Error adding item: {e}")  # For debugging
    
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
        try:
            # Get the correct path to the template file
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                template_path = os.path.join(sys._MEIPASS, 'invoice_template.html')
                print(f"Running as executable, looking for template at: {template_path}")
            else:
                # Running as script
                template_path = 'invoice_template.html'
                print(f"Running as script, looking for template at: {template_path}")
                
            # Try to open the template file
            with open(template_path, 'r') as f:
                template_str = f.read()
            print("Successfully read HTML template")
        except Exception as e:
            print(f"Error reading HTML template: {e}")
            # Try alternative locations
            try:
                # Try current directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                template_path = os.path.join(current_dir, 'invoice_template.html')
                print(f"Trying alternative path: {template_path}")
                
                # Try dist directory
                if not os.path.exists(template_path):
                    dist_dir = os.path.join(os.path.dirname(current_dir), 'dist')
                    template_path = os.path.join(dist_dir, 'invoice_template.html')
                    print(f"Trying dist directory path: {template_path}")
                
                with open(template_path, 'r') as f:
                    template_str = f.read()
                print("Successfully read HTML template from alternative location")
            except Exception as alt_e:
                print(f"Error reading from alternative location: {alt_e}")
                messagebox.showerror("Template Error", 
                                    f"Could not find the invoice template file.\n\nError: {e}\n\nPlease make sure 'invoice_template.html' is in the same folder as the application.")
                return False
        
        # Create Jinja2 template
        try:
            template = Template(template_str)
            print("Successfully created Jinja2 template")
        except Exception as e:
            print(f"Error creating Jinja2 template: {e}")
            return False
        
        # Prepare items data
        items_data = []
        try:
            # Get all items from the tree
            all_items = self.tree.get_children()
            print(f"Total items in tree: {len(all_items)}")
            
            for item in all_items:
                values = self.tree.item(item)['values']
                print(f"Processing item values: {values}")
                
                # Make sure we have all the required values and they're properly formatted
                if len(values) >= 6:
                    item_data = {
                        'item_number': str(values[0]),
                        'order_number': str(values[1]),
                        'description': str(values[2]),
                        'quantity': str(values[3]),
                        'price': str(values[4]),
                        'amount': str(values[5])
                    }
                    items_data.append(item_data)
                    print(f"Added item to items_data: {item_data}")
                else:
                    print(f"Warning: Item has incomplete data: {values}")
            
            # Debug: Print items data to console
            print(f"Final items data for PDF: {items_data}")
            if not items_data:
                print("WARNING: No items found in the invoice!")
        except Exception as e:
            print(f"Error preparing items data: {e}")
            import traceback
            traceback.print_exc()
            return False
        
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
        try:
            html_out = template.render(**template_data)
            print("Successfully rendered HTML template")
        except Exception as e:
            print(f"Error rendering template: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # For debugging: Save the generated HTML to a file
        try:
            debug_html_path = os.path.join(os.path.dirname(filename), "debug_invoice.html")
            with open(debug_html_path, "w") as html_file:
                html_file.write(html_out)
            print(f"Debug HTML saved to: {debug_html_path}")
        except Exception as e:
            print(f"Error saving debug HTML: {e}")
        
        # Convert to PDF using xhtml2pdf
        try:
            with open(filename, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_out, dest=pdf_file)
            
            if pisa_status.err:
                print(f"Error creating PDF: {pisa_status.err}")
                return False
            else:
                print(f"PDF successfully created at: {filename}")
                return True
        except Exception as e:
            print(f"Exception during PDF creation: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_invoice(self):
        # Get invoice number and date for filename
        invoice_number = self.invoice_number.get()
        if not invoice_number:
            messagebox.showwarning("Missing Information", "Please enter an invoice number.")
            return
            
        try:
            invoice_date = datetime.strptime(self.invoice_date.get(), "%b %d,%Y").strftime("%Y%m%d")
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please enter a valid invoice date in the format 'MMM DD,YYYY'.")
            return
            
        company_name = self.bill_company.get().replace(" ", "_") if self.bill_company.get() else "unnamed"
        
        # Create filename format: SKYNET_INV_[NUMBER]_[DATE]_[COMPANY]
        filename_base = f"SKYNET_INV_{invoice_number}_{invoice_date}_{company_name}"
        
        # Get desktop path
        desktop_path = os.path.expanduser("~/Desktop")
        
        # Create full file path for PDF only
        pdf_path = os.path.join(desktop_path, f"{filename_base}.pdf")
        
        # Prepare items data for PDF
        items_data = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if len(values) >= 6:
                items_data.append({
                    'item_number': str(values[0]),
                    'order_number': str(values[1]),
                    'description': str(values[2]),
                    'quantity': str(values[3]),
                    'price': str(values[4]),
                    'amount': str(values[5])
                })
        
        # Debug: Print number of items
        print(f"Number of items to save: {len(items_data)}")
        
        if not items_data:
            response = messagebox.askyesno("No Items", "There are no items in this invoice. Do you still want to save it?")
            if not response:
                return
        
        try:
            # Generate and save PDF only
            pdf_success = self.generate_pdf(pdf_path)
            
            if pdf_success:
                # Show success message
                tk.messagebox.showinfo("Success", f"Invoice saved to Desktop:\n{filename_base}.pdf")
            else:
                tk.messagebox.showwarning("Warning", f"There was an issue generating the PDF.")
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save invoice: {str(e)}")
            # Print detailed error for debugging
            import traceback
            traceback.print_exc()

    def delete_item(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)
        self.update_totals()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
