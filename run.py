import core  # core.so ဖိုင် ရှိရန်လိုအပ်သည်
import os
import sys
import time
import hashlib
import shutil

# --- [ UI COLORS ] ---
C_RED, C_CYAN, C_GREEN, C_YELLOW, C_RESET, C_BOLD = '\033[91m', '\033[96m', '\033[92m', '\033[93m', '\033[0m', '\033[1m'
SECRET_SALT = "ohmygod@123"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    """ဖုန်း Screen အကျယ်ကို တိုင်းတာရန်"""
    return shutil.get_terminal_size().columns

def print_center(text, color=C_RESET):
    """စာသားများကို Screen အလယ်တည့်တည့်သို့ ပို့ပေးရန်"""
    width = get_terminal_width()
    for line in text.split('\n'):
        print(f"{color}{line.center(width)}{C_RESET}")

def display_smns_banner(did, key="N/A", expiry="N/A", status="PENDING"):
    """စတိုင်ကျသော SMNS Banner နှင့် User Info ကို ပြသရန်"""
    os.system('clear')
    width = get_terminal_width()
    
    # SMNS ASCII Logo
    smns_logo = """
 ██████╗███╗   ███╗███╗   ██╗███████╗
██╔════╝████╗ ████║████╗  ██║██╔════╝
╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗
 ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║
██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║
╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"""

    # ဘောင်မျဉ်းများကို ဘယ်ညာအညီ ချိန်ညှိခြင်း
    border_line = "═" * (width - 4)
    print(f"{C_CYAN}╔{border_line}╗{C_RESET}")
    print_center(smns_logo, C_GREEN + C_BOLD)
    print_center("SMNS TECHNOLOGY TOOLKIT", C_YELLOW + C_BOLD)
    print(f"{C_CYAN}╠{border_line}╣{C_RESET}")
    
    # Device ID, Key, Expire Date ပြသရန် (ဘယ်ညာ ညီအောင် Padding ထည့်ထားသည်)
    info_pad = 20
    print(f"{C_CYAN}║ {C_YELLOW}DEVICE ID : {C_WHITE}{str(did).ljust(width - info_pad)}{C_CYAN} ║")
    print(f"{C_CYAN}║ {C_YELLOW}KEY       : {C_WHITE}{str(key).ljust(width - info_pad)}{C_CYAN} ║")
    print(f"{C_CYAN}║ {C_YELLOW}EXPIRE    : {C_WHITE}{str(expiry).ljust(width - info_pad)}{C_CYAN} ║")
    print(f"{C_CYAN}║ {C_YELLOW}STATUS    : {C_GREEN if status != 'PENDING' else C_RED}{str(status).ljust(width - info_pad)}{C_CYAN} ║")
    
    print(f"{C_CYAN}╚{border_line}╝{C_RESET}")

if __name__ == "__main__":
    try:
        # core ထဲမှ Device ID ယူခြင်း
        did = core.get_device_id()
        
        if not core.check_time_manipulation():
            os.system('clear')
            print_center("FATAL ERROR: System time manipulation detected!", C_RED)
            sys.exit(1)

        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # License စစ်ဆေးခြင်း
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            
            is_valid, msg, exp = core.validate_key(did, current_key)
            if is_valid:
                authorized, status, expiry = True, msg, exp
            elif core.verify_legacy_user(current_key):
                lt_exp = "212601010000"
                raw_new = f"{did}{lt_exp}{SECRET_SALT}"
                new_k = f"{hashlib.sha256(raw_new.encode()).hexdigest()[:12].upper()}{lt_exp}"
                with open(LICENSE_FILE, "w") as f: f.write(new_k)
                authorized, status, current_key, expiry = True, "VERIFIED_LIFETIME", new_k, "LIFETIME"

        display_smns_banner(did, current_key, expiry, status)
        
        # Activation Key တောင်းခံခြင်း
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_input = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            
            v, m, e = core.validate_key(did, key_input)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_input)
                display_smns_banner(did, key_input, e, m)
                authorized = True
            else:
                print_center("Invalid Activation Key!", C_RED)
                sys.exit(1)

        if authorized:
            # အောင်မြင်ပါက ပင်မ လုပ်ဆောင်ချက်ကို စတင်ရန်
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] STOPPED BY USER.{C_RESET}")
