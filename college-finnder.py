import tkinter as tk
from tkinter import messagebox
import sqlite3

class CollegeFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Finder")
        self.root.geometry("800x600")
        self.root.configure(bg='teal')  # Set background color

        # Heading
        self.heading_label = tk.Label(root, text="College Finder", font=("Arial", 20, "bold"), pady=10, bg='teal',
                                      fg='white')
        self.heading_label.pack()

        # Personal Details of student
        self.label_name = tk.Label(root, text="Name:", font=("Arial", 12), pady=5, bg='teal', fg='white')
        self.entry_name = tk.Entry(root, font=("Arial", 12))

        self.label_age = tk.Label(root, text="Age:", font=("Arial", 12), pady=5, bg='teal', fg='white')
        self.entry_age = tk.Entry(root)

        # Gender Selection
        self.label_gender = tk.Label(root, text="Gender:", font=("Arial", 12), pady=5, bg='teal', fg='white')

        # Use a frame to organize the radio buttons
        self.gender_frame = tk.Frame(root, bg='teal')
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        self.radio_male = tk.Radiobutton(self.gender_frame, text="Male", variable=self.gender_var, value="Male",
                                         font=("Arial", 12), bg='teal')
        self.radio_female = tk.Radiobutton(self.gender_frame, text="Female", variable=self.gender_var, value="Female",
                                           font=("Arial", 12), bg='teal')

        # Academic Details of student
        self.label_12th_percentage = tk.Label(root, text="12th Percentage:", font=("Arial", 12), pady=5, bg='teal',
                                              fg='white')
        self.entry_12th_percentage = tk.Entry(root, font=("Arial", 12))

        self.label_pass_out_year = tk.Label(root, text="Year of Passing:", font=("Arial", 12), pady=5, bg='teal',
                                            fg='white')
        self.entry_pass_out_year = tk.Entry(root, font=("Arial", 12))

        # JEE Details
        self.jee_var = tk.IntVar()
        self.jee_var.set(0)
        self.jee_checkbox = tk.Checkbutton(root, text="Attempted JEE?", variable=self.jee_var, font=("Arial", 12),
                                           bg='teal')

        self.label_jee_percentile = tk.Label(root, text="JEE Percentile:", font=("Arial", 12), pady=5, bg='teal',
                                             fg='white')
        self.entry_jee_percentile = tk.Entry(root, font=("Arial", 12))

        # Find Colleges Button
        self.find_colleges_button = tk.Button(root, text="Find Colleges", command=self.find_colleges,
                                              font=("Arial", 14, "bold"), bg='orange', fg='white')

        # Listbox to display colleges with Scrollbar
        self.college_listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Arial", 12), bg='white', fg='teal')
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.college_listbox.yview)
        self.college_listbox.config(yscrollcommand=self.scrollbar.set)

        # Grid layout
        self.label_name.pack(pady=3)
        self.entry_name.pack(pady=3)

        self.label_age.pack(pady=3)
        self.entry_age.pack(pady=3)

        self.label_gender.pack(pady=3)
        self.gender_frame.pack(pady=3)
        self.radio_male.pack(side='left', padx=3)
        self.radio_female.pack(side='left', padx=3)

        self.label_12th_percentage.pack(pady=3)
        self.entry_12th_percentage.pack(pady=3)

        self.label_pass_out_year.pack(pady=3)
        self.entry_pass_out_year.pack(pady=3)

        self.jee_checkbox.pack(pady=3)
        self.label_jee_percentile.pack(pady=3)
        self.entry_jee_percentile.pack(pady=3)

        self.find_colleges_button.pack(pady=6)

        self.college_listbox.pack(pady=5, padx=10, fill='both', expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # SQLite database initialization
        self.conn = sqlite3.connect("college_finder.db")
        self.create_table()

    def create_table(self):
        # Create a table to store information
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                twelfth_percentage REAL,
                pass_out_year INTEGER,
                jee_attempted INTEGER,
                jee_percentile REAL
            )
        ''')
        self.conn.commit()

    def insert_data(self, name, age, gender, twelfth_percentage, pass_out_year, jee_attempted, jee_percentile):
        # Insert data into the database
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO student_info (name, age, gender, twelfth_percentage, pass_out_year, jee_attempted, jee_percentile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, twelfth_percentage, pass_out_year, jee_attempted, jee_percentile))
        self.conn.commit()

    def find_colleges(self):
        try:
            # Gathering user input
            name = self.entry_name.get()
            age = int(self.entry_age.get())
            gender = self.gender_var.get()
            twelfth_percentage = float(self.entry_12th_percentage.get())
            pass_out_year = int(self.entry_pass_out_year.get())
            jee_attempted = self.jee_var.get()
            jee_percentile = float(self.entry_jee_percentile.get()) if jee_attempted == 1 else 0.0

            # Save data to SQLite
            self.insert_data(name, age, gender, twelfth_percentage, pass_out_year, jee_attempted, jee_percentile)

            # College criteria
            colleges = [
                {'name': 'IIT MUMBAI', 'cutoff_percentage': 65, 'jee_cutoff_percentile': 95},
                # ... (rest of the college data)
            ]

            eligible_colleges = []
            if twelfth_percentage > 90:
                eligible_colleges = [college['name'] for college in colleges[5:]]
            elif 80 <= twelfth_percentage <= 89:
                eligible_colleges = [college['name'] for college in colleges[10:]]
            elif 70 <= twelfth_percentage <= 79:
                eligible_colleges = [college['name'] for college in colleges[15:]]
            elif 60 <= twelfth_percentage <= 69:
                eligible_colleges = [college['name'] for college in colleges[20:]]

            # JEE Percentile Criteria
            if self.jee_var.get() == 1 and jee_percentile > 95:
                eligible_colleges = [college['name'] for college in colleges[:25]]

            # Display the results in the listbox
            self.college_listbox.delete(0, tk.END)
            for college in eligible_colleges:
                self.college_listbox.insert(tk.END, college)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")

    def display_saved_data(self):
        # Fetch and display data from the database
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM student_info
        ''')
        data = cursor.fetchall()

        # Display the data in the console
        for row in data:
            print(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CollegeFinderApp(root)

    # Display saved data (optional)
    app.display_saved_data()

    root.mainloop()