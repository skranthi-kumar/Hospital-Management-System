# Made By Kranthi Kumar

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import webbrowser

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("500x600")

        # Create a connection to the database
        self.conn = sqlite3.connect('hospital.db')
        self.c = self.conn.cursor()

        # Drop the 'patients' table if it already exists
        self.c.execute('DROP TABLE IF EXISTS patients')

        # Create a table for storing patient information
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                address TEXT,
                contact TEXT,
                appointment_date TEXT,
                consultation_department TEXT
            )
        ''')
        self.conn.commit()

        # Customize the GUI style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Create labels and entry widgets
        tk.Label(root, text="Patient Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add more labels and entry widgets as needed...

        tk.Label(root, text="Age:").grid(row=1, column=0, padx=10, pady=10)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(root, text="Gender:").grid(row=2, column=0, padx=10, pady=10)
        gender_frame = tk.Frame(root)
        gender_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        tk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").grid(row=0, column=0, sticky='w')
        tk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").grid(row=0, column=1, sticky='w')

        tk.Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=10)
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(root, text="Contact Number:").grid(row=4, column=0, padx=10, pady=10)
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(root, text="Appointment Date:").grid(row=5, column=0, padx=10, pady=10)
        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='dd-mm-y', 
                                    month_background='darkblue', 
                                    header_background='darkblue', 
                                    weekend_background='white', 
                                    weekend_font=('Arial', 10, 'bold'))
        self.date_entry.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(root, text="Consultation Department:").grid(row=6, column=0, padx=10, pady=10)
        self.department_var = tk.StringVar(root)
        self.department_var.set('Cardio')  # Set the default value
        choices = {'Cardio', 'Gastro', 'Liver', 'ENT'}
        department_dropdown = tk.OptionMenu(root, self.department_var, *choices)
        department_dropdown.config(width=12)
        department_dropdown.grid(row=6, column=1, padx=10, pady=10)

        # Create the submit button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit)
        self.submit_button.grid(row=7, column=1, padx=10, pady=10)

    def submit(self):
        # Retrieve entered data
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()
        address = self.address_entry.get()
        contact = self.contact_entry.get()
        appointment_date = self.date_entry.get_date().strftime('%d-%m-%y')
        department = self.department_var.get()

        # Insert data into the database
        self.c.execute('''
            INSERT INTO patients (name, age, gender, address, contact, appointment_date, consultation_department) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, address, contact, appointment_date, department))

        self.conn.commit()
        print("Data inserted into the database.")

        # Display a thank you message
        messagebox.showinfo("Success", "Your appointment is scheduled. Thank you!")

        # Generate and save the appointment card
        self.generate_appointment_card(name, appointment_date, department)

    def generate_appointment_card(self, name, appointment_date, department):
        # Create a blank image for the appointment card
        img = Image.new('RGB', (400, 200), color=(255, 255, 255))

        # Initialize the drawing context
        d = ImageDraw.Draw(img)

        # Specify the text and font to be displayed
        text = f"Appointment Card for {name}\nDate: {appointment_date}\nDepartment: {department}"
        font = ImageFont.load_default()

        # Draw text on the image
        d.text((10, 10), text, fill=(0, 0, 0), font=font)

        # Save the image in the specified folder as a PNG file
        save_location = "/Users/s.kranthikumarchowdary/Downloads/appointment card"
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        img_path = os.path.join(save_location, "appointment_card.png")
        img.save(img_path)

        # Show a success message
        messagebox.showinfo("Success", "Appointment card generated successfully.")

        # Add a download option
        self.download_button = ttk.Button(self.root, text="Download", command=lambda: self.download_file(img_path))
        self.download_button.grid(row=8, column=1, padx=10, pady=10)

    def download_file(self, file_path):
        webbrowser.open(file_path)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    app.run()
