import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import os

# Initialize parking lot
rows, cols = 3, 6
lot = [['A', 'B', 'C', 'D', 'E', 'F'],
       ['G', 'H', 'I', 'J', 'K', 'L'],
       ['M', 'N', 'O', 'P', 'Q', 'R']]
occupied_spots = {}
visitors_count = 0
cars_parked = 0

# Functions
def update_parking_display():
    for r in range(rows):
        for c in range(cols):
            spot = lot[r][c]
            btn_text = spot if spot not in occupied_spots else f"{spot}\n(Occupied)"
            buttons[r][c].config(text=btn_text)

def park_car():
    global visitors_count, cars_parked
    visitors_count += 1
    choice = messagebox.askquestion("Park Your Car", "Do you want to park your car?\nParking charges: 20₹/hour")
    if choice == 'yes':
        available_spots = [spot for row in lot for spot in row if spot not in occupied_spots]
        if not available_spots:
            messagebox.showinfo("Parking Full", "Sorry, no parking spots available!")
            return
        selected_spot = simpledialog.askstring("Select Spot", f"Available spots: {', '.join(available_spots)}\n\nEnter spot to park:")
        if selected_spot and selected_spot.upper() in available_spots:
            occupied_spots[selected_spot.upper()] = time.time()
            cars_parked += 1
            messagebox.showinfo("Success", f"Car parked at spot {selected_spot.upper()} successfully!")
            update_parking_display()
        else:
            messagebox.showerror("Invalid Spot", "Invalid or already occupied spot selected.")

def remove_car():
    global cars_parked
    selected_spot = simpledialog.askstring("Remove Car", "Enter spot to remove car from:")
    if selected_spot:
        selected_spot = selected_spot.upper()
        if selected_spot in occupied_spots:
            entry_time = occupied_spots.pop(selected_spot)
            parked_hours = max(1, int((time.time() - entry_time) // 3600))  # At least 1 hour
            total_fee = parked_hours * 20

            receipt_text = f"""
🚗 Yash Parking Lot and Services 🚗
--------------------------------------
Spot: {selected_spot}
Parked Time: {parked_hours} hours
Total Fee: ₹{total_fee}
--------------------------------------
Thank you for visiting our parking lot, please visit again!
"""
            # Save receipt
            if not os.path.exists("receipts"):
                os.makedirs("receipts")
            receipt_filename = f"receipts/receipt_{selected_spot}.txt"
            with open(receipt_filename, "w", encoding="utf-8") as f:
                f.write(receipt_text)

            messagebox.showinfo("Receipt", receipt_text)
            cars_parked -= 1
            update_parking_display()
        else:
            messagebox.showerror("Error", "No car parked at this spot!")

def show_admin_summary():
    available_spots = rows * cols - len(occupied_spots)
    admin_summary = f"""
📊 Admin Parking Lot Summary:

- Total visitors: {visitors_count}
- Total cars parked: {cars_parked}
- Occupied spots: {cars_parked}
- Available spots: {available_spots}
"""
    messagebox.showinfo("Admin Summary", admin_summary)

# GUI
root = tk.Tk()
root.title("🚗 Yash Parking Lot Management 🚗")
root.geometry("900x700")
root.configure(bg="#f0f8ff")

frame = tk.Frame(root)
frame.pack(pady=20)

buttons = []
for r in range(rows):
    row_buttons = []
    for c in range(cols):
        btn = tk.Button(frame, text=lot[r][c], width=10, height=3, font=("Arial", 12))
        btn.grid(row=r, column=c, padx=5, pady=5)
        row_buttons.append(btn)
    buttons.append(row_buttons)

action_frame = tk.Frame(root, bg="#f0f8ff")
action_frame.pack(pady=20)

park_btn = tk.Button(action_frame, text="🚗 Park Car", command=park_car, font=("Arial", 14), bg="#4CAF50", fg="white")
park_btn.grid(row=0, column=0, padx=10)

remove_btn = tk.Button(action_frame, text="🅿️ Remove Car", command=remove_car, font=("Arial", 14), bg="#f44336", fg="white")
remove_btn.grid(row=0, column=1, padx=10)

admin_btn = tk.Button(action_frame, text="🛠️ Admin Summary", command=show_admin_summary, font=("Arial", 14), bg="#2196F3", fg="white")
admin_btn.grid(row=0, column=2, padx=10)

update_parking_display()

root.mainloop()
