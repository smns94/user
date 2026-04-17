import core
import os
import sys
import shutil

# --- [ UI COLORS ] ---
C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RED, C_RESET, C_BOLD = '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[91m', '\033[0m', '\033[1m'
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    return shutil.get_terminal_size().columns

def display_smns_banner(smns_did, key="N/A", expiry="N/A", status="PENDING"):
    os.system('clear')
    w = get_terminal_width()
    
    logo = [
        " ██████╗███╗   ███╗███╗   ██╗███████╗",
        "██╔════╝████╗ ████║████╗  ██║██╔════╝",
        "╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗",
        " ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║",
        "██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║",
        "╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"
    ]

    print(f"{C_CYAN}┌{'─'*(w-2)}┐{C_RESET}")
    for line in logo:
        print(f"{C_CYAN}│{C_GREEN}{C_BOLD}{line.center(w-2)}{C_CYAN}│{C_RESET}")
    
    print(f"{C_CYAN}│{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w-2)}{C_CYAN}│{C_RESET}")
    print(f"{C_CYAN}├{'─'*(w-2)}┤{C_RESET}")

    # Info Display Section
    info_width = w - 17
    status_color = C_GREEN if "VERIFIED" in str(status) else C_RED
    
    print(f"{C_CYAN}│ {C_YELLOW}DEVICE ID : {C_WHITE}{str(smns_did).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}KEY       : {C_WHITE}{str(key).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}EXPIRE    : {C_WHITE}{str(expiry).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}STATUS    : {status_color}{str(status).ljust(info_width)}{C_CYAN} │")

    print(f"{C_CYAN}└{'─'*(w-2)}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # ၁။ ပထမဦးဆုံး Device ID ကို ယူပြီး SMNS- အဖြစ် ပြောင်းပါမည်
        original_did = core.get_device_id()
        smns_did = str(original_did).replace("TRB-", "SMNS-")
        if not smns_did.startswith("SMNS-"):
            smns_did = f"SMNS-{smns_did}"
        
        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # ၂။ License File ရှိလျှင် စစ်ဆေးပါမည်
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            
            # အရေးကြီး: Key Generator က SMNS- နဲ့ ထုတ်ထားတာဖြစ်လို့ validate လုပ်တဲ့အခါ smns_did ကို သုံးရပါမယ်
            is_valid, msg, exp = core.validate_key(smns_did, current_key)
            if is_valid:
                authorized, status, expiry = True, msg, exp

        display_smns_banner(smns_did, current_key, expiry, status)
        
        # ၃။ Activation တောင်းဆိုခြင်း
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_in = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            
            # ဒီမှာလည်း smns_did ကို သုံးပြီး validate လုပ်ပေးရပါမယ်
            v, m, e = core.validate_key(smns_did, key_in)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_in)
                display_smns_banner(smns_did, key_in, e, m)
                authorized = True
            else:
                # Key မှားရင် ပြသရန်
                print(f"\n{C_RED}[X] Invalid Activation Key for {smns_did}!{C_RESET}")
                sys.exit(1)

        if authorized:
            # ၄။ ပင်မလုပ်ငန်းစဉ်ကို စတင်ပါမည်
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped.{C_RESET}")
