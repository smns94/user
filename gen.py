import hashlib
import os
import shutil

# --- [ CONFIGURATION ] ---
SECRET_SALT = "ohmygod@123"
KEY_FILE = "keys.txt"

# --- [ UI COLORS ] ---
C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RED, C_RESET, C_BOLD = '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[91m', '\033[0m', '\033[1m'

def get_width():
    return shutil.get_terminal_size().columns

def print_banner():
    os.system('clear')
    w = get_width()
    banner = f"""
{C_GREEN}{C_BOLD} ██████╗███╗   ███╗███╗   ██╗███████╗
██╔════╝████╗ ████║████╗  ██║██╔════╝
╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗
 ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║
██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║
╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝{C_RESET}
    """
    for line in banner.split('\n'):
        print(line.center(w))
    print(f"{C_YELLOW}{'SMNS ADMIN KEY GENERATOR'.center(w)}{C_RESET}")
    print(f"{C_CYAN}{'═' * (w-4)}{C_RESET}".center(w))

def make_key():
    print_banner()
    raw_did = input(f"{C_YELLOW}[?] Enter Device ID (TRB or SMNS): {C_WHITE}").strip()
    
    # TRB ပါခဲ့ရင် SMNS လို့ အလိုအလျောက် ပြောင်းပေးမည့် logic
    did = raw_did.replace("TRB-", "SMNS-")
    if not did.startswith("SMNS-"):
        did = f"SMNS-{did}"

    expiry = input(f"{C_YELLOW}[?] Expiry Date (YYYYMMDDHHMM): {C_WHITE}").strip()
    
    # Key Generation Logic
    raw = f"{did}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    final_key = f"{auth_hash[:12].upper()}{expiry}"
    
    # Save to keys.txt
    with open(KEY_FILE, "a") as f:
        f.write(f"Device: {did} | Key: {final_key} | Exp: {expiry}\n")
    
    print(f"\n{C_GREEN}[✔] SUCCESS! KEY GENERATED & SAVED TO {KEY_FILE}{C_RESET}")
    print(f"{C_CYAN}┌──────────────────────────────────────────┐")
    print(f"│ {C_YELLOW}NEW DEVICE ID : {C_WHITE}{did:<24}{C_CYAN} │")
    print(f"│ {C_YELLOW}FINAL KEY     : {C_GREEN}{final_key:<24}{C_CYAN} │")
    print(f"└──────────────────────────────────────────┘{C_RESET}")
    input(f"\n{C_WHITE}Press Enter to return to menu...")

def clear_keys():
    print_banner()
    confirm = input(f"{C_RED}[!] ARE YOU SURE TO DELETE ALL KEYS? (y/n): {C_WHITE}").strip().lower()
    if confirm == 'y':
        if os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
            print(f"\n{C_GREEN}[✔] All keys have been deleted successfully!{C_RESET}")
        else:
            print(f"\n{C_YELLOW}[*] No key file found to delete.{C_RESET}")
    time.sleep(2)

if __name__ == "__main__":
    import time
    while True:
        print_banner()
        print(f"{C_WHITE}[1] {C_GREEN}GENERATE NEW SMNS KEY")
        print(f"{C_WHITE}[2] {C_RED}CLEAR ALL SAVED KEYS")
        print(f"{C_WHITE}[3] {C_YELLOW}EXIT")
        
        opt = input(f"\n{C_CYAN}root@smns_gen:~# {C_WHITE}").strip()
        
        if opt == '1': make_key()
        elif opt == '2': clear_keys()
        elif opt == '3': break
