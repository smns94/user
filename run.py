import core  # core.so ဖိုင်ရှိရန် လိုအပ်သည်
import os
import sys
import shutil

# --- [ UI COLORS ] ---
C_RED, C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RESET, C_BOLD = '\033[91m', '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[0m', '\033[1m'

def get_terminal_width():
    """Terminal width ကိုယူပြီး အနည်းဆုံး ၅၀ ထားပါမည်"""
    w = shutil.get_terminal_size().columns
    return w if w > 50 else 50

def display_smns_banner(did, key="N/A", expiry="N/A", status="PENDING"):
    """ဒေါင်လိုက်ဘောင်များ တည့်မတ်စွာ ချိန်ညှိထားသော Banner"""
    os.system('clear')
    w = get_terminal_width()
    inner_w = w - 4  # ဘေးဘောင် ၂ ဖက်စာ နုတ်ထားသော အကျယ်
    
    logo = [
        " ██████╗███╗   ███╗███╗   ██╗███████╗",
        "██╔════╝████╗ ████║████╗  ██║██╔════╝",
        "╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗",
        " ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║",
        "██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║",
        "╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"
    ]

    # (1) အပေါ်ဆုံးဘောင်
    print(f"{C_CYAN}┌{'─' * (w-2)}┐{C_RESET}")
    
    # (2) Logo အပိုင်း (အလယ်တည့်တည့်)
    for line in logo:
        print(f"{C_CYAN}│{C_GREEN}{C_BOLD}{line.center(w-2)}{C_CYAN}│{C_RESET}")
    
    # (3) Title အပိုင်း
    print(f"{C_CYAN}│{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w-2)}{C_CYAN}│{C_RESET}")
    
    # (4) အလယ်ပိုင်း မျဉ်းတား
    print(f"{C_CYAN}├{'─' * (w-2)}┤{C_RESET}")

    # (5) Info Section (ဒေါင်လိုက်ဘောင်များ ညီအောင် တွက်ချက်ခြင်း)
    # Label များကို ၁၀ စာလုံးစာ အကွာအဝေး ပုံသေ သတ်မှတ်ပါသည်
    def draw_info_line(label, value, val_color=C_WHITE):
        # စာသား စုစုပေါင်း အရှည်ကို တွက်သည် (label(10) + separator(3) + value)
        label_part = f"{label:<10} : "
        # value color code များသည် string length ထဲဝင်နေသဖြင့် length တွက်လျှင် ဖယ်တွက်ရသည်
        clean_val = str(value)
        content_len = 1 + len(label_part) + len(clean_val) + 1 # spaces padding အတွက်
        
        padding_count = (w - 2) - content_len
        if padding_count < 0: padding_count = 0
        
        padding = " " * padding_count
        print(f"{C_CYAN}│ {C_YELLOW}{label_part}{val_color}{clean_val}{padding} {C_CYAN}│{C_RESET}")

    # Status အရောင် သတ်မှတ်ခြင်း
    stat_color = C_GREEN if "VERIFIED" in str(status).upper() else C_RED
    
    # အချက်အလက်များ ထုတ်ပြခြင်း
    draw_info_line("DEVICE ID", did)
    draw_info_line("KEY", key)
    draw_info_line("EXPIRE", expiry)
    draw_info_line("STATUS", status, stat_color)

    # (6) အောက်ဆုံးဘောင်
    print(f"{C_CYAN}└{'─' * (w-2)}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # core မှ device data များယူခြင်း
        did = core.get_device_id()
        # ပုံမှန်အတိုင်း License စစ်ဆေးသည့် logic ထည့်ပါ (အပေါ်က code အတိုင်း)
        
        # ဥပမာပြသရန် (အစ်ကို့ code ထဲတွင် အောက်ပါအတိုင်း ပြန်သုံးပါ)
        display_smns_banner(did, "5A6FD9F6A14C202704131225", "2027-04-13 12:25:00", "VERIFIED")
        
        print(f"\n{C_YELLOW}[*] STAGE 1: EXECUTING INSTANT BYPASS...{C_RESET}")
        core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped by user.{C_RESET}")
