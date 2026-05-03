import json
import uuid
import os

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer number.")

def get_yes_no(prompt):
    while True:
        answer = input(prompt).lower().strip()

        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please enter yes or no.")

def create_character():
    character_id = str(uuid.uuid4())

    character = {
        "name": input("Character name: "),
        "race": input("Race: "),
        "class": input("Class: "),
        "level": get_int("Level: "),
        "hp": get_int("HP: "),
        "ac": get_int("AC: "),
        "notes": input("Notes/roles: ")
    }

    print("\nPlease confirm this character:")
    display_character(character)

    if get_yes_no("Is this correct? y/n: "):
        return character_id, character

    print("\nOkay, let's enter the character again.")

def create_party(characters):
    party_id = str(uuid.uuid4())

    party = {
        "party_name": input("Party name: "),
        "members": []
    }

    while True:
        print("\nCreate a party member:")
        character_id, character = create_character()

        characters[character_id] = character
        party["members"].append(character_id)

        if not get_yes_no("Add another member? y/n: "):
            break

    return party_id, party

def save_data(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved to {filename}")

def load_data(filename):
    # file doesn't exist -> create it
    if not os.path.exists(filename):
        print(f"{filename} not found. Creating new file...")

        data = {
            "characters": {},
            "parties": {}
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        return data
    
    # file exists -> load it
    with open(filename, "r") as file:
        return json.load(file)
    
def display_party(party, characters):
    print(f"\nParty: {party['party_name']}")

    for character_id in party["members"]:
        character = characters[character_id]

        print(f"""
Name: {character['name']}
Species: {character['race']}
Class: {character['class']}
Level: {character['level']}
HP: {character['hp']}
AC: {character['ac']}
Notes: {character['notes']}
""")
        
def select_party(data):
    parties = data["parties"]

    if not parties:
        print("No parties available.")
        return None

    party_ids = list(parties.keys())

    print("\nAvailable Parties:")
    for i, pid in enumerate(party_ids):
        print(f"{i + 1}. {parties[pid]['party_name']}")

    choice = int(input("Select a party: ")) - 1

    if 0 <= choice < len(party_ids):
        return party_ids[choice]
    else:
        print("invalid selection.")
        return None

def add_member_to_party(data):
    party_id = select_party(data)
    if not party_id:
        return
    
    party = data["parties"][party_id]

    print("\nCreating new character:")
    character_id, character = create_character()

    # store character globally
    data["characters"][character_id] = character

    # link to party
    party["members"].append(character_id)

    print(f"{character['name']} added to {party['party_name']}")

def delete_member_from_party(data):
    party_id = select_party(data)
    if not party_id:
        return
    
    party = data["parties"][party_id]
    members = party["members"]

    if not members:
        print("This party has no members.")
        return
    
    print("\nParty Members:")
    for i, cid in enumerate(members):
        char = data["characters"][cid]
        print(f"{i + 1}. {char['name']} ({char['class']})")

    choice = int(input("Select member to remove: ")) - 1

    if 0 <= choice < len(members):
        removed_id = members.pop(choice)
        removed_char = data["characters"][removed_id]

        print(f"{removed_char['name']} removed from party.")

    else:
        print("Invalid selection.")
        
def display_menu(data, active_party_id):
    while True:
        print("""
Display Menu
1. Display active party
2. Display saved party
3. Display character
4. Back
""")

        choice = input("Choose an option: ")

        if choice == "1":
            if not active_party_id:
                print("No active party selected.")
            else:
                display_party(data["parties"][active_party_id], data["characters"])

        elif choice == "2":
            party_id = select_party(data)
            if party_id:
                display_party(data["parties"][party_id], data["characters"])

        elif choice == "3":
            display_character_menu(data)

        elif choice == "4":
            break

        else:
            print("Invalid choice.")

def select_character(data):
    characters = data["characters"]

    if not characters:
        print("No characters available.")
        return None

    character_ids = list(characters.keys())

    print("\nAvailable Characters:")
    for i, cid in enumerate(character_ids):
        character = characters[cid]
        print(f"{i + 1}. {character['name']} ({character['class']})")

    choice = get_int("Select a character: ") - 1

    if 0 <= choice < len(character_ids):
        return character_ids[choice]

    print("Invalid selection.")
    return None

def display_character(character):
    print(f"""
Name: {character['name']}
Race: {character['race']}
Class: {character['class']}
Level: {character['level']}
HP: {character['hp']}
AC: {character['ac']}
Notes: {character['notes']}
""")

def display_character_menu(data):
    while True:
        print("""
Display Character
1. Select party first
2. List all characters alphabetically
3. Back
""")

        choice = input("Choose an option: ")

        if choice == "1":
            display_character_from_party(data)

        elif choice == "2":
            display_character_from_all(data)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

def display_character_from_party(data):
    party_id = select_party(data)
    if not party_id:
        return

    party = data["parties"][party_id]
    member_ids = party["members"]

    if not member_ids:
        print("This party has no members.")
        return

    sorted_member_ids = sorted(
        member_ids,
        key=lambda cid: data["characters"][cid]["name"].lower()
    )

    print(f"\nCharacters in {party['party_name']}:")
    for i, cid in enumerate(sorted_member_ids):
        character = data["characters"][cid]
        print(f"{i + 1}. {character['name']} ({character['class']})")

    choice = get_int("Select a character: ") - 1

    if 0 <= choice < len(sorted_member_ids):
        character_id = sorted_member_ids[choice]
        display_character(data["characters"][character_id])
    else:
        print("Invalid selection.")

def display_character_from_all(data):
    characters = data["characters"]

    if not characters:
        print("No characters available.")
        return

    sorted_character_ids = sorted(
        characters.keys(),
        key=lambda cid: characters[cid]["name"].lower()
    )

    print("\nAll Characters:")
    for i, cid in enumerate(sorted_character_ids):
        character = characters[cid]
        print(f"{i + 1}. {character['name']} ({character['class']})")

    choice = get_int("Select a character: ") - 1

    if 0 <= choice < len(sorted_character_ids):
        character_id = sorted_character_ids[choice]
        display_character(characters[character_id])
    else:
        print("Invalid selection.")

def edit_menu(data):
    while True:
        print("""
Edit Menu
1. Add party member
2. Remove party member
3. Edit party name
4. Edit character information
5. Back
""")

        choice = input("Choose an option: ")

        if choice == "1":
            add_member_to_party(data)

        elif choice == "2":
            delete_member_from_party(data)

        elif choice == "3":
            edit_party_name(data)

        elif choice == "4":
            edit_character_information(data)

        elif choice == "5":
            break

        else:
            print("Invalid choice.")

def edit_party_name(data):
    party_id = select_party(data)
    if not party_id:
        return

    party = data["parties"][party_id]
    old_name = party.get("name", party.get("party_name", "Unnamed Party"))

    print(f"Current party name: {old_name}")
    new_name = input("New party name: ")

    party["name"] = new_name

    if "party_name" in party:
        del party["party_name"]

    print("Party name updated.")

def edit_character_information(data):
    character_id = select_character(data)
    if not character_id:
        return

    character = data["characters"][character_id]

    while True:
        display_character(character)

        print("""
Edit Character
1. Name
2. Race
3. Class
4. Level
5. HP
6. AC
7. Notes
8. Back
""")

        choice = input("Choose field to edit: ")

        if choice == "1":
            character["name"] = input("New name: ")

        elif choice == "2":
            character["race"] = input("New race: ")

        elif choice == "3":
            character["class"] = input("New class: ")

        elif choice == "4":
            character["level"] = get_int("New level: ")

        elif choice == "5":
            character["hp"] = get_int("New HP: ")

        elif choice == "6":
            character["ac"] = get_int("New AC: ")

        elif choice == "7":
            character["notes"] = input("New notes: ")

        elif choice == "8":
            break

        else:
            print("Invalid choice.")

def dms_tools_menu(data, active_party_id):
    while True:
        print("""
DM's Tools
1. Generate Random Encounter
2. Generate Random Loot
3. Back
""")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_random_encounter_menu(data, active_party_id)

        elif choice == "2":
            generate_random_loot(data, active_party_id)

        elif choice == "3":
            break

        else:
            print("Invalid choice.")

def generate_random_encounter_menu(data, active_party_id):
    if not active_party_id:
        print("No active party selected. Load/select a party first.")
        return

    while True:
        print("""
Generate Random Encounter
1. Easy
2. Normal
3. Challenging
4. Back
""")

        choice = input("Choose difficulty: ")

        if choice == "1":
            print("Random Encounter function under construction. Please stand by for updates.")

        elif choice == "2":
            print("Random Encounter function under construction. Please stand by for updates.")

        elif choice == "3":
            print("Random Encounter function under construction. Please stand by for updates.")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")

def generate_random_loot(data, active_party_id):
    if not active_party_id:
        print("No active party selected. Load/select a party first.")
        return

    print("Random Loot function under construction. Please stand by for updates.")

def main():
    data = load_data("dnd_data.json")
    active_party_id = None

    while True:
        print("""
1. Create new party
2. Load/select active party
3. Display options (active party, other parties, individual characters)
4. Edit options (Add character to party, remove character from party, change party name, edit character info)
5. DM's Tools
6. Save and quit
""")
        choice = input("Choose an option: ")

        if choice == "1":
            party_id, party = create_party(data["characters"])
            data["parties"][party_id] = party

        elif choice == "2":
            party_id = select_party(data)
            if party_id:
                active_party_id = party_id
                print(f"{data['parties'][party_id]['party_name']} is now the active party.")
                display_party(data["parties"][party_id], data["characters"])

        elif choice == "3":
            display_menu(data, active_party_id)

        elif choice == "4":
            edit_menu(data)

        elif choice == "5":
            dms_tools_menu(data, active_party_id)

        elif choice == "6":
            save_data(data, "dnd_data.json")
            while True:
                next_action = input("1. Continue\n2. Quit\nChoose: ")

                if next_action == "1":
                    break  # goes back to main menu loop

                elif next_action == "2":
                    print("Goodbye!")
                    return  # exits main()

                else:
                    print("Invalid choice.")

        else:
            print("invalid choice.")


main()