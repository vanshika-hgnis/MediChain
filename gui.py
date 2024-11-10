import time
import tkinter as tk
from tkinter import ttk, messagebox
from user_manager import UserManager
from database import Database
from blockchain import HealthcareBlockchain


class PatientPage:
    def __init__(self, root, blockchain):
        self.blockchain = blockchain
        self.top = tk.Toplevel(root)
        self.top.title("Patient Page")

        tk.Label(self.top, text="Enter Data:").pack()
        self.data_entry = tk.Entry(self.top)
        self.data_entry.pack()

        tk.Button(self.top, text="Add Data to Blockchain", command=self.add_data).pack()

    def add_data(self):
        data = self.data_entry.get()
        self.blockchain.add_block(data)
        messagebox.showinfo("Success", "Data added to blockchain!")


class DoctorPage:
    def __init__(self, root, blockchain):
        self.blockchain = blockchain
        self.top = tk.Toplevel(root)
        self.top.title("Doctor Page")

        tk.Label(self.top, text="Enter Patient ID to Access Data:").pack()
        self.patient_id_entry = tk.Entry(self.top)
        self.patient_id_entry.pack()

        tk.Button(self.top, text="Request Access", command=self.request_access).pack()

    def request_access(self):
        patient_id = self.patient_id_entry.get()
        if self.blockchain.has_access(patient_id, "doctor", "doctor_id"):
            messagebox.showinfo("Access Granted", "Viewing patient data.")
        else:
            messagebox.showwarning(
                "Access Denied", "You do not have permission to view this data."
            )


class HospitalPage:
    def __init__(self, root, blockchain):
        self.blockchain = blockchain
        self.top = tk.Toplevel(root)
        self.top.title("Hospital Page")

        tk.Label(self.top, text="Enter Patient ID to Access Data:").pack()
        self.patient_id_entry = tk.Entry(self.top)
        self.patient_id_entry.pack()

        tk.Button(self.top, text="Request Access", command=self.request_access).pack()

    def request_access(self):
        patient_id = self.patient_id_entry.get()
        if self.blockchain.has_access(patient_id, "hospital", "hospital_id"):
            messagebox.showinfo("Access Granted", "Viewing patient data.")
        else:
            messagebox.showwarning(
                "Access Denied", "You do not have permission to view this data."
            )


import tkinter as tk
from tkinter import ttk, messagebox
from user_manager import UserManager
from database import Database
from blockchain import HealthcareBlockchain


class HealthcareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthcare Blockchain System")
        self.root.geometry("800x600")

        self.db = Database()
        self.user_manager = UserManager(self.db)
        self.blockchain = HealthcareBlockchain()

        self.current_user = None
        self.current_user_type = None
        self.logo_image = tk.PhotoImage(file="medichainlogo.png")
        self.setup_main_page()

        # self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logo_label = tk.Label(main_frame, image=self.logo_image)
        logo_label.grid(row=0, column=0, columnspan=2)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Healthcare Blockchain System",
            font=("Helvetica", 16, "bold"),
        )
        title_label.grid(row=0, column=2, columnspan=1, pady=20)

        # Login/Register buttons
        ttk.Button(main_frame, text="Login", command=self.setup_login_page).grid(
            row=1, column=0, pady=10, padx=10
        )
        ttk.Button(main_frame, text="Register", command=self.setup_register_page).grid(
            row=1, column=1, pady=10, padx=10
        )

    def setup_main_page(self):
        self.clear_window()
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logo_label = tk.Label(main_frame, image=self.logo_image)
        logo_label.grid(row=0, column=0, columnspan=2)
        title_label = ttk.Label(
            main_frame,
            text="Healthcare Blockchain System",
            font=("Helvetica", 16, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Login/Register buttons
        ttk.Button(main_frame, text="Login", command=self.setup_login_page).grid(
            row=1, column=0, pady=10, padx=10
        )
        ttk.Button(main_frame, text="Register", command=self.setup_register_page).grid(
            row=1, column=1, pady=10, padx=10
        )

        # self.clear_window()

    def setup_login_page(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logo_image = tk.PhotoImage(
            file="medichainlogo.png"
        )  # Assuming logo is in root dir
        logo_label = tk.Label(frame, image=logo_image)
        logo_label.image = (
            logo_image  # Maintain reference to prevent garbage collection
        )
        logo_label.grid(row=0, column=0, columnspan=2)
        ttk.Label(frame, text="Login", font=("Helvetica", 14, "bold")).grid(
            row=1, column=0, columnspan=2, pady=20
        )
        ttk.Label(frame, text="Username:").grid(row=2, column=0, pady=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(frame, textvariable=username_var)

        username_entry.grid(row=2, column=1, pady=5)
        ttk.Label(frame, text="Password:").grid(row=3, column=0, pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, show="*")
        password_entry.grid(row=3, column=1, pady=5)
        ttk.Button(
            frame,
            text="Login",
            command=lambda: self.handle_login(username_var.get(), password_var.get()),
        ).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=self.setup_main_page).grid(
            row=5, column=0, columnspan=2
        )

    def setup_register_page(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logo_image = tk.PhotoImage(
            file="medichainlogo.png"
        )  # Assuming logo is in root dir
        logo_label = tk.Label(frame, image=logo_image)
        logo_label.image = (
            logo_image  # Maintain reference to prevent garbage collection
        )
        logo_label.grid(row=0, column=0)
        ttk.Label(frame, text="Register", font=("Helvetica", 14, "bold")).grid(
            row=0, column=1, columnspan=2, pady=20
        )

        ttk.Label(frame, text="Username:").grid(row=1, column=0, pady=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(frame, textvariable=username_var)
        username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=2, column=0, pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_var, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="User Type:").grid(row=3, column=0, pady=5)
        user_type_var = tk.StringVar()
        user_type_combo = ttk.Combobox(
            frame, textvariable=user_type_var, values=["patient", "doctor", "hospital"]
        )
        user_type_combo.grid(row=3, column=1, pady=5)

        ttk.Button(
            frame,
            text="Register",
            command=lambda: self.handle_registration(
                username_var.get(), password_var.get(), user_type_var.get()
            ),
        ).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(frame, text="Back", command=self.setup_main_page).grid(
            row=5, column=0, columnspan=2
        )

    def setup_patient_dashboard(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logo_image = tk.PhotoImage(
            file="medichainlogo.png"
        )  # Assuming logo is in root dir
        logo_label = tk.Label(frame, image=logo_image)
        logo_label.image = (
            logo_image  # Maintain reference to prevent garbage collection
        )
        logo_label.grid(row=0, column=0)
        ttk.Label(
            frame,
            text=f"Patient Dashboard - {self.current_user}",
            font=("Helvetica", 14, "bold"),
        ).grid(row=0, column=1, columnspan=2, pady=20)
        ttk.Button(
            frame, text="Add Medical Record", command=self.setup_add_record_page
        ).grid(row=1, column=0, pady=10)
        ttk.Button(frame, text="View My Records", command=self.view_records).grid(
            row=1, column=1, pady=10
        )
        ttk.Button(
            frame, text="Manage Access", command=self.setup_manage_access_page
        ).grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Logout", command=self.logout).grid(
            row=2, column=1, pady=10
        )

    def setup_healthcare_provider_dashboard(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        provider_type = "Doctor" if self.current_user_type == "doctor" else "Hospital"
        ttk.Label(
            frame,
            text=f"{provider_type} Dashboard - {self.current_user}",
            font=("Helvetica", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Button(
            frame, text="View Patient Records", command=self.setup_view_patient_records
        ).grid(row=1, column=0, pady=10)
        ttk.Button(
            frame, text="Request Access", command=self.setup_request_access_page
        ).grid(row=1, column=1, pady=10)
        ttk.Button(frame, text="Logout", command=self.logout).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def setup_add_record_page(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            frame, text="Add Medical Record", font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Record details
        ttk.Label(frame, text="Diagnosis:").grid(row=1, column=0, pady=5)
        diagnosis_var = tk.StringVar()
        diagnosis_entry = ttk.Entry(frame, textvariable=diagnosis_var)
        diagnosis_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Treatment:").grid(row=2, column=0, pady=5)
        treatment_var = tk.StringVar()
        treatment_entry = ttk.Entry(frame, textvariable=treatment_var)
        treatment_entry.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Notes:").grid(row=3, column=0, pady=5)
        notes_text = tk.Text(frame, height=4, width=30)
        notes_text.grid(row=3, column=1, pady=5)

        ttk.Button(
            frame,
            text="Add Record",
            command=lambda: self.add_medical_record(
                diagnosis_var.get(), treatment_var.get(), notes_text.get("1.0", tk.END)
            ),
        ).grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(frame, text="Back", command=self.setup_patient_dashboard).grid(
            row=5, column=0, columnspan=2
        )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def handle_login(self, username: str, password: str):
        success, user_type = self.user_manager.authenticate_user(username, password)
        if success:
            self.current_user = username
            self.current_user_type = user_type
            if user_type == "patient":
                self.setup_patient_dashboard()
            else:
                self.setup_healthcare_provider_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def handle_registration(self, username: str, password: str, user_type: str):
        if not all([username, password, user_type]):
            messagebox.showerror("Error", "All fields are required")
            return

        if self.user_manager.register_user(username, password, user_type):
            self.blockchain.add_user(username, user_type, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.setup_login_page()
        else:
            messagebox.showerror("Error", "Username already exists")

    def logout(self):
        self.current_user = None
        self.current_user_type = None
        self.setup_main_page()

    def add_medical_record(self, diagnosis: str, treatment: str, notes: str):
        # self.blockchain.add_user(self.current_user, self.current_user_typ,self.p)
        if not all([diagnosis, treatment]):
            messagebox.showerror("Error", "Diagnosis and treatment are required")
            return

        record_data = {
            "diagnosis": diagnosis,
            "treatment": treatment,
            "notes": notes.strip(),
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        if self.blockchain.add_medical_record(self.current_user, record_data):
            messagebox.showinfo("Success", "Medical record added successfully")
            self.setup_patient_dashboard()
        else:
            messagebox.showerror("Error", "Failed to add medical record")

    def view_records(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Medical Records", font=("Helvetica", 14, "bold")).grid(
            row=0, column=0, pady=20
        )

        # Create Treeview
        tree = ttk.Treeview(
            frame, columns=("Date", "Diagnosis", "Treatment", "Notes"), show="headings"
        )

        tree.heading("Date", text="Date")
        tree.heading("Diagnosis", text="Diagnosis")
        tree.heading("Treatment", text="Treatment")
        tree.heading("Notes", text="Notes")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Get and display records
        records = self.blockchain.get_patient_records(
            self.current_user, self.current_user
        )
        for record in records:
            medical_data = record
            tree.insert(
                "",
                "end",
                values=(
                    medical_data["date"],
                    medical_data["diagnosis"],
                    medical_data["treatment"],
                    medical_data["notes"],
                ),
            )

        tree.grid(row=1, column=0, pady=10)
        scrollbar.grid(row=1, column=1, sticky="ns")

        ttk.Button(frame, text="Back", command=self.setup_patient_dashboard).grid(
            row=2, column=0, pady=10
        )

    def setup_manage_access_page(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            frame, text="Manage Access Permissions", font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Healthcare provider selection
        ttk.Label(frame, text="Healthcare Provider:").grid(row=1, column=0, pady=5)
        provider_var = tk.StringVar()
        providers = [
            user
            for user, data in self.blockchain.users.items()
            if data["type"] in ["doctor", "hospital"]
        ]
        provider_combo = ttk.Combobox(
            frame, textvariable=provider_var, values=providers
        )
        provider_combo.grid(row=1, column=1, pady=5)

        ttk.Button(
            frame,
            text="Grant Access",
            command=lambda: self.grant_access(provider_var.get()),
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Display current access permissions
        ttk.Label(
            frame, text="Current Access Permissions:", font=("Helvetica", 12)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        permissions_frame = ttk.Frame(frame)
        permissions_frame.grid(row=4, column=0, columnspan=2, pady=10)

        current_permissions = self.blockchain.access_permissions.get(
            self.current_user, []
        )
        for i, provider in enumerate(current_permissions):
            ttk.Label(permissions_frame, text=provider).grid(row=i, column=0, pady=2)
            ttk.Button(
                permissions_frame,
                text="Revoke",
                command=lambda p=provider: self.revoke_access(p),
            ).grid(row=i, column=1, pady=2)

        ttk.Button(frame, text="Back", command=self.setup_patient_dashboard).grid(
            row=5, column=0, columnspan=2, pady=20
        )

    def grant_access(self, provider: str):
        if not provider:
            messagebox.showerror("Error", "Please select a healthcare provider")
            return

        if self.blockchain.grant_access(self.current_user, provider):
            messagebox.showinfo("Success", f"Access granted to {provider}")
            self.setup_manage_access_page()
        else:
            messagebox.showerror("Error", "Failed to grant access")

    def revoke_access(self, provider: str):
        if provider in self.blockchain.access_permissions[self.current_user]:
            self.blockchain.access_permissions[self.current_user].remove(provider)
            messagebox.showinfo("Success", f"Access revoked for {provider}")
            self.setup_manage_access_page()
        else:
            messagebox.showerror("Error", "Failed to revoke access")

    def setup_view_patient_records(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            frame, text="View Patient Records", font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Patient selection
        ttk.Label(frame, text="Select Patient:").grid(row=1, column=0, pady=5)
        patient_var = tk.StringVar()
        patients = [
            user
            for user, data in self.blockchain.users.items()
            if data["type"] == "patient"
            and self.blockchain.has_access(user, self.current_user)
        ]
        patient_combo = ttk.Combobox(frame, textvariable=patient_var, values=patients)
        patient_combo.grid(row=1, column=1, pady=5)

        def show_patient_records():
            patient = patient_var.get()
            if not patient:
                messagebox.showerror("Error", "Please select a patient")
                return

            records = self.blockchain.get_patient_records(patient, self.current_user)

            # Clear previous records if any
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Treeview):
                    widget.destroy()

            # Create Treeview for records
            tree = ttk.Treeview(
                frame,
                columns=("Date", "Diagnosis", "Treatment", "Notes"),
                show="headings",
            )
            tree.heading("Date", text="Date")
            tree.heading("Diagnosis", text="Diagnosis")
            tree.heading("Treatment", text="Treatment")
            tree.heading("Notes", text="Notes")

            for record in records:
                medical_data = record
                tree.insert(
                    "",
                    "end",
                    values=(
                        medical_data["date"],
                        medical_data["diagnosis"],
                        medical_data["treatment"],
                        medical_data["notes"],
                    ),
                )

            tree.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(frame, text="View Records", command=show_patient_records).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        ttk.Button(
            frame, text="Back", command=self.setup_healthcare_provider_dashboard
        ).grid(row=4, column=0, columnspan=2, pady=20)

    def setup_request_access_page(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(
            frame, text="Request Patient Access", font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frame, text="Select Patient:").grid(row=1, column=0, pady=5)
        patient_var = tk.StringVar()
        patients = [
            user
            for user, data in self.blockchain.users.items()
            if data["type"] == "patient"
            and not self.blockchain.has_access(user, self.current_user)
        ]
        patient_combo = ttk.Combobox(frame, textvariable=patient_var, values=patients)
        patient_combo.grid(row=1, column=1, pady=5)

        def request_access():
            patient = patient_var.get()
            if not patient:
                messagebox.showerror("Error", "Please select a patient")
                return

            messagebox.showinfo(
                "Request Sent",
                f"Access request sent to {patient}. Please wait for approval.",
            )

        ttk.Button(frame, text="Request Access", command=request_access).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        ttk.Button(
            frame, text="Back", command=self.setup_healthcare_provider_dashboard
        ).grid(row=3, column=0, columnspan=2, pady=20)
