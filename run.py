import core  # core.so ဖိုင်ရှိရန် လိုအပ်ပါသည်
import os
import sys
import time
import hashlib
import shutil

# --- [ UI COLORS ] ---
C_RED, C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RESET, C_BOLD = '\033[91m', '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[0m', '\033[1m'
SECRET_SALT = "ohmygod@123"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    """Terminal ရဲ့ လက်ရှိအကျယ်ကို ယူရန်"""
    return shutil.get_terminal_size().columns

def display_smns_banner(did, key="N/A", expiry="N/A", status="PENDING"):
    """လေးထောင့်ဘောင်များ သေသပ်စွာ ချိန်ညှိထားသော Banner"""
    os.system('clear')
    w = get_terminal_width()
    
    # ASCII Logo Section
    logo = [
        " ██████╗███╗   ███╗███╗   ██╗███████╗",
        "██╔════╝████╗ ████║████╗  ██║██╔════╝",
        "╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗",
        " ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║",
        "██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║",
        "╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"
    ]

    # Top Border
    print(f"{C_CYAN}┌{'─'*(w-2)}┐{C_RESET}")
    for line in logo:
        print(f"{C_CYAN}│{C_GREEN}{C_BOLD}{line.center(w-2)}{C_CYAN}│{C_RESET}")
    
    print(f"{C_CYAN}│{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w-2)}{C_CYAN}│{C_RESET}")
    print(f"{C_CYAN}├{'─'*(w-2)}┤{C_RESET}")

    # Info Section (ဘယ်ညာ အညီဖြစ်အောင် ညှိထားပါသည်)
    infos = [
        (f"DEVICE ID", did),
        (f"KEY", key),
        (f"EXPIRE", expiry),
        (f"STATUS", status)
    ]

    for label, value in infos:
        # စာသားအရှည်ကို တွက်ချက်ပြီး Space ဖြည့်ခြင်း
        color = C_GREEN if "VERIFIED" in str(value) else C_WHITE
        content = f" {C_YELLOW}{label:<10} : {color}{value}"
        # စာသားနောက်က ပိုနေသော space များကို ဘောင်ညီအောင် ဖြည့်သည်
        clean_len = len(label) + len(str(value)) + 4
        padding = " " * (w - clean_len - 3)
        print(f"{C_CYAN}│{content}{padding}│{C_RESET}")

    # Bottom Border
    print(f"{C_CYAN}└{'─'*(w-2)}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # Device ID နှင့် ပတ်သက်သော အချက်အလက်များကို core မှ ယူပါမည်
        did = core.get_device_id()
        
        # System Time စစ်ဆေးခြင်း
        if not core.check_time_manipulation():
            print(f"{C_RED}[!] Time Manipulation Detected!{C_RESET}")
            sys.exit(1)

        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # License File ရှိမရှိ စစ်ဆေးခြင်း
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            
            is_valid, msg, exp = core.validate_key(did, current_key)
            if is_valid:
                authorized, status, expiry = True, msg, exp

        # Banner ပြသခြင်း
        display_smns_banner(did, current_key, expiry, status)
        
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_in = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            v, m, e = core.validate_key(did, key_in)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_in)
                display_smns_banner(did, key_in, e, m)
                authorized = True
            else:
                print(f"{C_RED}[X] Invalid Key!{C_RESET}")
                sys.exit(1)

        if authorized:
            # Main process စတင်ခြင်း
            print(f"\n{C_YELLOW}[*] STAGE 1: EXECUTING INSTANT BYPASS...{C_RESET}")
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")
