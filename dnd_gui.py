import json
import tkinter as tk
from tkinter import ttk


def load_data(filename="dnd_data.json"):
    with open(filename, "r") as file:
        return json.load(file)


def get_party_name(party):
    return party.get("name", party.get("party_name", "Unnamed Party"))


def show_party(event=None):
    selected = party_listbox.curselection()

    if not selected:
        return

    index = selected[0]
    party_id = party_ids[index]
    party = data["parties"][party_id]

    party_title.config(text=get_party_name(party))

    for row in member_table.get_children():
        member_table.delete(row)

    for character_id in party["members"]:
        character = data["characters"][character_id]

        member_table.insert(
            "",
            "end",
            values=(
                character.get("name", ""),
                character.get("race", ""),
                character.get("class", ""),
                character.get("level", ""),
                character.get("hp", ""),
                character.get("ac", ""),
                character.get("notes", "")
            )
        )


data = load_data()

root = tk.Tk()
root.title("D&D Party Manager")
root.geometry("900x500")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

left_frame = ttk.Frame(main_frame)
left_frame.pack(side="left", fill="y")

right_frame = ttk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

ttk.Label(left_frame, text="Parties").pack(anchor="w")

party_listbox = tk.Listbox(left_frame, width=30)
party_listbox.pack(fill="y", expand=True)

party_ids = list(data["parties"].keys())

for party_id in party_ids:
    party = data["parties"][party_id]
    party_listbox.insert(tk.END, get_party_name(party))

party_listbox.bind("<<ListboxSelect>>", show_party)

party_title = ttk.Label(right_frame, text="Select a party", font=("Arial", 16, "bold"))
party_title.pack(anchor="w", pady=(0, 10))

columns = ("Name", "Race", "Class", "Level", "HP", "AC", "Notes")

member_table = ttk.Treeview(right_frame, columns=columns, show="headings")

for col in columns:
    member_table.heading(col, text=col)
    member_table.column(col, width=100)

member_table.column("Notes", width=250)

member_table.pack(fill="both", expand=True)

root.mainloop()