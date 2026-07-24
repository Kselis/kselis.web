import random
import string
import uuid
import json
import os
import hashlib

ROLE_MAPPINGS = {
    'Volunteer': 'V',
    'Admin': 'A',
    'Interns': 'T',
    'Technical': 'D',
    'Managers': 'M'
}

REGISTRY_FILE = "credential_registry.json"

def load_registry():
    """Loads the stored IDs, filenames, counters, and signatures from a local JSON file."""
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r') as file:
            registry = json.load(file)
            # Upgrade older JSON files if they are missing new keys
            if "role_counters" not in registry:
                registry["role_counters"] = {role: 0 for role in ROLE_MAPPINGS}
            if "signatures" not in registry:
                registry["signatures"] = []
            return registry
            
    # If the file doesn't exist yet, return a blank slate
    return {
        "employee_ids": [], 
        "filenames": [],
        "signatures": [],
        "role_counters": {role: 0 for role in ROLE_MAPPINGS}
    }

def save_registry(registry):
    """Saves the updated registry back to the JSON file."""
    with open(REGISTRY_FILE, 'w') as file:
        json.dump(registry, file, indent=4)

def generate_credential_id(role_name, counter, existing_ids):
    """Generates a unique 16-character KSE ID."""
    role_letter = ROLE_MAPPINGS.get(role_name, 'X')
    
    # Expand the counter to 4 digits (e.g., 42 becomes "0042")
    counter_padded = f"{counter % 10000:04d}" 
    
    while True:
        # Expand the random hash to 8 characters
        random_hash = ''.join(random.choices(string.ascii_uppercase, k=8))
        
        # Combine: KSE (3) + Role (1) + Counter (4) + Hash (8) = 16 characters
        employee_id = f"KSE{role_letter}{counter_padded}{random_hash}"
        
        # Check against our stored data to stop duplicacies
        if employee_id not in existing_ids:
            return employee_id

def generate_html_filename(existing_filenames):
    """Generates a unique 32-character filename."""
    while True:
        unique_32_char_hash = uuid.uuid4().hex
        filename = f"{unique_32_char_hash}.html"
        
        if filename not in existing_filenames:
            return filename

def generate_signature(employee_name, employee_id, role):
    """Generates a secure SHA-256 hash based on the employee's exact data."""
    raw_data = f"{employee_name}|{employee_id}|{role}"
    signature = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
    return f"0x{signature[:16]}"

# ==========================================
# Interactive Execution
# ==========================================
if __name__ == "__main__":
    registry = load_registry()
    
    print("--- Kselis Credential Generator ---")
    
    # 1. Ask for the Employee's Name
    while True:
        employee_name = input("Enter the employee's full name: ").strip()
        if employee_name:
            break
        print("Name cannot be blank.")

    # 2. Ask for the Role with validation
    print("\nAvailable roles: Volunteer, Admin, Interns, Technical, Managers")
    while True:
        role = input("Enter the role for this credential: ").strip()
        if role in ROLE_MAPPINGS:
            break
        print("Invalid role. Please type exactly as shown in the list.")
    
    # 3. Automatically fetch and increment the counter
    current_counter = registry["role_counters"][role]
    new_counter = current_counter + 1
            
    # 4. Generate new unique values
    new_id = generate_credential_id(role, new_counter, registry["employee_ids"])
    new_filename = generate_html_filename(registry["filenames"])
    new_signature = generate_signature(employee_name, new_id, role)
    
    # 5. Add the new values to our tracking lists
    registry["employee_ids"].append(new_id)
    registry["filenames"].append(new_filename)
    registry["signatures"].append(new_signature)
    registry["role_counters"][role] = new_counter
    
    # 6. Save the updated data to the JSON file
    save_registry(registry)
    
    # 7. Output the results
    print("\n✅ Successfully generated and stored!")
    print(f"Name:      {employee_name}")
    print(f"Role:      {role} (Auto-assigned counter: {new_counter})")
    print(f"ID:        {new_id}")
    print(f"Filename:  {new_filename}")
    print(f"Signature: {new_signature}")