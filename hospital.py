import heapq
import json
import os
from datetime import datetime

class Patient:
    def __init__(self, pid, name, condition):
        self.id = pid
        self.name = name
        self.condition = condition  # "Critical" or "Normal"
        self.arrival_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "condition": self.condition,
            "arrival_time": self.arrival_time
        }
class HospitalQueue:
    def __init__(self, history_file="patient_history.json"):
        self.critical_queue = []   
        self.normal_queue = []     
        self.history_file = history_file
        self.history = self.load_history()
# Add patient
    def add_patient(self, patient):
        if patient.condition.lower() == "critical":
# Using heapq: store (priority_time, patient)
            arrival_dt = datetime.strptime(patient.arrival_time, "%Y-%m-%d %H:%M:%S")
            heapq.heappush(self.critical_queue, (arrival_dt, patient))
            print(f"Critical patient added: {patient.name}")
        else:
            self.normal_queue.append(patient)
            print(f"Normal patient added: {patient.name}")

# next patient
    def serve_patient(self):
        if self.critical_queue:
            _, patient = heapq.heappop(self.critical_queue)
            print(f"Serving CRITICAL patient: {patient.name}")
        elif self.normal_queue:
            patient = self.normal_queue.pop(0)
            print(f"Serving NORMAL patient: {patient.name}")
        else:
            print("No patients in queue.")
            return

        wait_time = self.calculate_wait_time(patient.arrival_time)
        print(f"Wait time: {wait_time} minutes")

# Save to history
        self.history.append(patient.to_dict())
        self.save_history()

#Calculate wait time
    def calculate_wait_time(self, arrival_time_str):
        arrival_time = datetime.strptime(arrival_time_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        wait = now - arrival_time
        return round(wait.total_seconds() / 60, 2)

#View queue status
    def view_queue(self):
        print("\nCurrent Queue:")
        print("Critical Patients:")
        for _, p in self.critical_queue:
            print(f"{p.name} (ID: {p.id})")
        print("Normal Patients:")
        for p in self.normal_queue:
            print(f"{p.name} (ID: {p.id})")

#Save history to file
    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=4)

#Load history from file
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []


#Menu
def main():
    hospital = HospitalQueue()
    pid_counter = 1

    while True:
        print("\n====== Hospital Patient Queue ======")
        print("1. Add Patient")
        print("2. Serve Next Patient")
        print("3. View Queue")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter patient name: ")
            condition = input("Enter condition (Critical/Normal): ")
            patient = Patient(pid_counter, name, condition)
            hospital.add_patient(patient)
            pid_counter += 1

        elif choice == "2":
            hospital.serve_patient()

        elif choice == "3":
            hospital.view_queue()

        elif choice == "4":
            print("Exiting!!! History saved.")
            hospital.save_history()
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
