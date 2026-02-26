from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, gender, disease):
        self.patient_id = self.validate_id(patient_id)
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self.gender = self.validate_gender(gender)
        self.disease = disease
        self.visit_history = []

    def validate_id(self, patient_id):
        if not isinstance(patient_id, str) or not patient_id.strip():
            raise ValueError("Patient ID must be a non-empty string.")
        return patient_id.strip()

    def validate_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        return name.strip()

    def validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        return age

    def validate_gender(self, gender):
        if gender.lower() not in ["male", "female"]:
            raise ValueError("Gender must be Male or Female.")
        return gender.capitalize()

    def update_info(self, name=None, age=None, gender=None, disease=None):
        if name:
            self.name = self.validate_name(name)
        if age:
            self.age = self.validate_age(age)
        if gender:
            self.gender = self.validate_gender(gender)
        if disease:
            self.disease = disease

    def to_string(self):
        # For saving to file using "|" as separator
        return f"{self.patient_id}|{self.name}|{self.age}|{self.gender}|{self.disease}"

    @staticmethod
    def from_string(data_str):
        # For loading from file
        parts = data_str.strip().split("|")
        return Patient(parts[0], parts[1], int(parts[2]), parts[3], parts[4])

    def __str__(self):
        return f"ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Disease: {self.disease}"


class Doctor:
    def __init__(self, doctor_id, name, age, gender, specialty, availability=True):
        self.doctor_id = self.validate_id(doctor_id)
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self.gender = self.validate_gender(gender)
        self.specialty = specialty
        self.availability = availability  # True if available, False otherwise

    def validate_id(self, doctor_id):
        if not isinstance(doctor_id, str) or not doctor_id.strip():
            raise ValueError("Doctor ID must be a non-empty string.")
        return doctor_id.strip()

    def validate_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        return name.strip()

    def validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        return age

    def validate_gender(self, gender):
        if gender.lower() not in ["male", "female"]:
            raise ValueError("Gender must be Male or Female.")
        return gender.capitalize()

    def update_info(self, name=None, age=None, gender=None, specialty=None, availability=None):
        if name:
            self.name = self.validate_name(name)
        if age:
            self.age = self.validate_age(age)
        if gender:
            self.gender = self.validate_gender(gender)
        if specialty:
            self.specialty = specialty
        if availability is not None:
            self.availability = availability

    def to_string(self):
        return f"{self.doctor_id}|{self.name}|{self.age}|{self.gender}|{self.specialty}|{self.availability}"

    @staticmethod
    def from_string(data_str):
        parts = data_str.strip().split("|")
        avail = parts[5].strip().lower() == "true"
        return Doctor(parts[0], parts[1], int(parts[2]), parts[3], parts[4], avail)

    def __str__(self):
        return f"ID: {self.doctor_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}, Specialty: {self.specialty}, Available: {self.availability}"


class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, appointment_date):
        self.appointment_id = self.validate_id(appointment_id)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = self.validate_date(appointment_date)

    def validate_id(self, appointment_id):
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID must be a non-empty string.")
        return appointment_id.strip()

    def validate_date(self, date_str):
        try:
            # check if date is in YYYY-MM-DD format
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    def to_string(self):
        return f"{self.appointment_id}|{self.patient_id}|{self.doctor_id}|{self.appointment_date}"

    @staticmethod
    def from_string(data_str):
        parts = data_str.strip().split("|")
        return Appointment(parts[0], parts[1], parts[2], parts[3])

    def __str__(self):
        return f"Appointment ID: {self.appointment_id}, Patient ID: {self.patient_id}, Doctor ID: {self.doctor_id}, Date: {self.appointment_date}"


class HospitalSystem:
    def __init__(self):
        self.patients = {}       # key: patient_id, value: Patient object
        self.doctors = {}        # key: doctor_id, value: Doctor object
        self.appointments = {}   # key: appointment_id, value: Appointment object
        self.load_data()

    # ---------- File Handling ----------
    def load_data(self):
        # Load patients
        try:
            with open("patients.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        patient = Patient.from_string(line)
                        self.patients[patient.patient_id] = patient
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error loading patients:", e)

        # Load doctors
        try:
            with open("doctors.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        doctor = Doctor.from_string(line)
                        self.doctors[doctor.doctor_id] = doctor
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error loading doctors:", e)

        # Load appointments
        try:
            with open("appointments.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        appointment = Appointment.from_string(line)
                        self.appointments[appointment.appointment_id] = appointment
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error loading appointments:", e)

    def save_data(self):
        try:
            # Save patients
            with open("patients.txt", "w", encoding="utf-8") as f:
                for patient in self.patients.values():
                    f.write(patient.to_string() + "\n")

            # Save doctors
            with open("doctors.txt", "w", encoding="utf-8") as f:
                for doctor in self.doctors.values():
                    f.write(doctor.to_string() + "\n")

            # Save appointments
            with open("appointments.txt", "w", encoding="utf-8") as f:
                for appointment in self.appointments.values():
                    f.write(appointment.to_string() + "\n")
        except IOError as e:
            print("Error saving data:", e)

    # ---------- Patient Operations ----------
    def add_patient(self):
        try:
            patient_id = input("Enter Patient ID: ").strip()
            if not patient_id:
                print("Error: Patient ID cannot be empty.")
                return
            if patient_id in self.patients:
                print("Error: Patient ID already exists.")
                return
            name = input("Enter Name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                return
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (Male/Female): ").strip()
            disease = input("Enter Disease: ").strip()
            if not disease:
                print("Error: Disease cannot be empty.")
                return
            patient = Patient(patient_id, name, age, gender, disease)
            self.patients[patient_id] = patient
            self.save_data()
            print("Patient added successfully.")
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    def delete_patient(self):
        try:
            patient_id = input("Enter Patient ID to delete: ").strip()
            if patient_id not in self.patients:
                print("Error: Patient ID does not exist.")
                return
            # Check if patient has appointments
            has_appointments = any(apt.patient_id == patient_id for apt in self.appointments.values())
            if has_appointments:
                print("Error: Cannot delete patient with active appointments.")
                return
            del self.patients[patient_id]
            self.save_data()
            print("Patient deleted successfully.")
        except Exception as e:
            print("Error:", e)

    # ---------- Doctor Operations ----------
    def add_doctor(self):
        try:
            doctor_id = input("Enter Doctor ID: ").strip()
            if not doctor_id:
                print("Error: Doctor ID cannot be empty.")
                return
            if doctor_id in self.doctors:
                print("Error: Doctor ID already exists.")
                return
            name = input("Enter Name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                return
            age = int(input("Enter Age: "))
            gender = input("Enter Gender (Male/Female): ").strip()
            specialty = input("Enter Specialty: ").strip()
            if not specialty:
                print("Error: Specialty cannot be empty.")
                return
            doctor = Doctor(doctor_id, name, age, gender, specialty, availability=True)
            self.doctors[doctor_id] = doctor
            self.save_data()
            print("Doctor added successfully.")
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    def delete_doctor(self):
        try:
            doctor_id = input("Enter Doctor ID to delete: ").strip()
            if doctor_id not in self.doctors:
                print("Error: Doctor ID does not exist.")
                return
            # Check if doctor has appointments
            has_appointments = any(apt.doctor_id == doctor_id for apt in self.appointments.values())
            if has_appointments:
                print("Error: Cannot delete doctor with active appointments.")
                return
            del self.doctors[doctor_id]
            self.save_data()
            print("Doctor deleted successfully.")
        except Exception as e:
            print("Error:", e)

    # ---------- Appointment Operations ----------
    def create_appointment(self):
        try:
            appointment_id = input("Enter Appointment ID: ").strip()
            if not appointment_id:
                print("Error: Appointment ID cannot be empty.")
                return
            if appointment_id in self.appointments:
                print("Error: Appointment ID already exists.")
                return
            patient_id = input("Enter Patient ID: ").strip()
            if patient_id not in self.patients:
                print("Error: Patient ID does not exist.")
                return
            doctor_id = input("Enter Doctor ID: ").strip()
            if doctor_id not in self.doctors:
                print("Error: Doctor ID does not exist.")
                return
            if not self.doctors[doctor_id].availability:
                print("Error: Doctor is not available.")
                return
            appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ").strip()
            # Validate date format and future date
            appt_datetime = datetime.strptime(appointment_date, "%Y-%m-%d")
            if appt_datetime.date() < datetime.now().date():
                print("Error: Appointment date must be in the future.")
                return
            appointment = Appointment(appointment_id, patient_id, doctor_id, appointment_date)
            self.appointments[appointment_id] = appointment
            self.save_data()
            print("Appointment created successfully.")
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    def cancel_appointment(self):
        try:
            appointment_id = input("Enter Appointment ID to cancel: ").strip()
            if appointment_id not in self.appointments:
                print("Error: Appointment ID does not exist.")
                return
            del self.appointments[appointment_id]
            self.save_data()
            print("Appointment canceled successfully.")
        except Exception as e:
            print("Error:", e)

    # ---------- View Operations ----------
    def view_patients(self):
        if not self.patients:
            print("No patients found.")
        else:
            print("\n--- Patient List ---")
            for patient in self.patients.values():
                print(patient)
            print()

    def view_doctors(self):
        if not self.doctors:
            print("No doctors found.")
        else:
            print("\n--- Doctor List ---")
            for doctor in self.doctors.values():
                print(doctor)
            print()

    def view_appointments(self):
        if not self.appointments:
            print("No appointments found.")
        else:
            print("\n--- Appointment List ---")
            for appointment in self.appointments.values():
                print(appointment)
            print()

    # ---------- Menu System ----------
    def main_menu(self):
        while True:
            print("\n===== Hospital Management System =====")
            print("1. Add Patient")
            print("2. View Patients")
            print("3. Delete Patient")
            print("4. Add Doctor")
            print("5. View Doctors")
            print("6. Delete Doctor")
            print("7. Create Appointment")
            print("8. View Appointments")
            print("9. Cancel Appointment")
            print("10. Exit")

            choice = input("Enter your choice (1-10): ").strip()
            try:
                if choice == "1":
                    self.add_patient()
                elif choice == "2":
                    self.view_patients()
                elif choice == "3":
                    self.delete_patient()
                elif choice == "4":
                    self.add_doctor()
                elif choice == "5":
                    self.view_doctors()
                elif choice == "6":
                    self.delete_doctor()
                elif choice == "7":
                    self.create_appointment()
                elif choice == "8":
                    self.view_appointments()
                elif choice == "9":
                    self.cancel_appointment()
                elif choice == "10":
                    print("Exiting system...")
                    self.save_data()
                    break
                else:
                    print("Invalid choice. Enter a number from 1 to 10.")
            except Exception as e:
                print("An error occurred:", e)


if __name__ == "__main__":
    print("🏥 Welcome to Hospital Management System!")
    print("=" * 50)
    system = HospitalSystem()
    system.main_menu()
