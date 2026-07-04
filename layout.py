from tkinter import *
from tkinter import scrolledtext

def get_username(role):
    """Creates a beautiful, custom dialog box for selecting a username."""
    selected_name = []
    
    login_root = Tk()
    login_root.title("Welcome")
    login_root.geometry("350x250")
    login_root.configure(bg="#F0F2F5")
    login_root.resizable(False, False)
    
    screen_width = login_root.winfo_screenwidth()
    screen_height = login_root.winfo_screenheight()
    x = (screen_width // 2) - (350 // 2)
    y = (screen_height // 2) - (250 // 2)
    login_root.geometry(f"350x250+{x}+{y}")
    
    theme_color = "#075E54" if role == "Server" else "#128C7E"

    banner = Label(login_root, text="Welcome to Chat", font=("Helvetica", 14, "bold"), bg=theme_color, fg="white", pady=15)
    banner.pack(fill=X)

    lbl = Label(login_root, text=f"Enter your username ({role}):", font=("Helvetica", 11), bg="#F0F2F5", fg="#333333", pady=10)
    lbl.pack()

    entry = Entry(login_root, font=("Helvetica", 12), bd=0, bg="white", highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor=theme_color, justify="center")
    entry.pack(ipady=6, padx=30, fill=X)
    entry.insert(0, role)
    entry.select_range(0, END)
    entry.focus()

    def on_submit(event=None):
        name = entry.get().strip()
        if name:
            selected_name.append(name)
            login_root.destroy()

    entry.bind("<Return>", on_submit)
    
    btn_submit = Button(login_root, text="Join Room", font=("Helvetica", 11, "bold"), bg=theme_color, fg="white", bd=0, padx=20, pady=8, cursor="hand2", command=on_submit)
    btn_submit.pack(pady=20)

    login_root.mainloop()
    
    return selected_name[0] if selected_name else role

def create_window(title, username, on_typing_cb):
    root = Tk()
    root.title(f"{title} - {username}")
    root.configure(bg="#F0F2F5")

    # Anti-Overlapping logic calculations
    window_width = 460
    window_height = 650 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    y_pos = (screen_height // 2) - (window_height // 2) - 30 
    
    if title == "Server":
        x_pos = (screen_width // 4) - (window_width // 2)
    else:
        x_pos = ((screen_width * 3) // 4) - (window_width // 2)
        
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    theme_color = "#075E54" if title == "Server" else "#128C7E"
    is_dark = [False]  # Track theme state using list closure
    
    # Header user branding frame
    header_frame = Frame(root, bg=theme_color, pady=10)
    header_frame.pack(fill=X)
    
    avatar = Label(header_frame, text=username[0].upper(), font=("Helvetica", 12, "bold"), bg="#FFFFFF", fg=theme_color, width=3, height=1, bd=0)
    avatar.pack(side=LEFT, padx=(15, 10))
    
    header = Label(header_frame, text=username, font=("Helvetica", 12, "bold"), bg=theme_color, fg="white")
    header.pack(side=LEFT)

    # NEW: TOOLBAR ACTION UTILITY ROW (Holds Feature 1, 3, & 4)
    toolbar = Frame(root, bg="#EAEAEA", pady=5, padx=10)
    toolbar.pack(fill=X)

    # Feature 4: Live Message Search Bar Input Box
    search_lbl = Label(toolbar, text="🔍", bg="#EAEAEA", font=("Helvetica", 10))
    search_lbl.pack(side=LEFT)
    
    search_entry = Entry(toolbar, font=("Helvetica", 9), bd=0, bg="white", width=15)
    search_entry.pack(side=LEFT, padx=5, ipady=2)

    def search_keyword(event=None):
        chat_area.tag_remove("match", "1.0", "end")
        query = search_entry.get().strip()
        if query:
            start = "1.0"
            while True:
                pos = chat_area.search(query, start, stopindex="end", nocase=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(query)}c"
                chat_area.tag_add("match", pos, end_pos)
                start = end_pos
            chat_area.tag_config("match", background="yellow", foreground="black")

    search_entry.bind("<KeyRelease>", search_keyword)

    # Feature 3: Clear Visible Chat History Screen
    def clear_chat():
        chat_area.config(state=NORMAL)
        chat_area.delete("1.0", END)
        chat_area.config(state=DISABLED)

    clear_btn = Button(toolbar, text="🗑️ Clear", font=("Helvetica", 9), bg="#D4D4D4", fg="black", bd=0, padx=8, cursor="hand2", command=clear_chat)
    clear_btn.pack(side=RIGHT, padx=5)

    # Core Chat Log display space
    chat_area = scrolledtext.ScrolledText(root, wrap=WORD, state=DISABLED, font=("Helvetica", 11), bg="#E5DDD5")
    chat_area.pack(padx=15, pady=(10, 5), fill=BOTH, expand=True)

    # Typing status label
    typing_label = Label(root, text="", font=("Helvetica", 9, "italic"), bg="#F0F2F5", fg="#555555", anchor="w")
    typing_label.pack(fill=X, padx=20, pady=(0, 2))

    # Input Control panel
    input_frame = Frame(root, bg="#F0F2F5")
    input_frame.pack(fill=X, side=BOTTOM, padx=15, pady=10)

    entry = Entry(input_frame, font=("Helvetica", 12), bd=0, bg="white", highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor=theme_color)
    entry.pack(side=LEFT, fill=X, expand=True, ipady=8, padx=(0, 5))

    # Feature 2: Character Counter Tracker Hook (Max 250 characters limit)
    counter_lbl = Label(root, text="0 / 250", font=("Helvetica", 8), bg="#F0F2F5", fg="#777777", anchor="e")
    counter_lbl.pack(fill=X, padx=20, side=BOTTOM, pady=(0, 5))

    def on_key_action(event):
        # Trigger typing notification callback
        on_typing_cb()
        
        # Enforce text character length limits
        current_text = entry.get()
        if len(current_text) > 250:
            entry.delete(250, END)
            current_text = entry.get()
            
        counter_lbl.config(text=f"{len(current_text)} / 250")

    entry.bind("<KeyRelease>", on_key_action)
    entry.focus()

    send_btn = Button(input_frame, text="Send", font=("Helvetica", 11, "bold"), bg=theme_color, fg="white", bd=0, padx=25, pady=6, cursor="hand2")
    send_btn.pack(side=RIGHT)

    # Message layout custom style tags
    chat_area.tag_configure("self_msg", foreground=theme_color, font=("Helvetica", 10, "bold"))
    chat_area.tag_configure("other_msg", foreground="#555555", font=("Helvetica", 10, "bold"))
    chat_area.tag_configure("text_style", foreground="#000000", font=("Helvetica", 11))
    chat_area.tag_configure("time_style", foreground="#888888", font=("Helvetica", 8, "italic"))
    chat_area.tag_configure("right", justify="right")
    chat_area.tag_configure("left", justify="left")

    # Feature 1: Dark Mode / Light Theme Toggle Function
    def toggle_theme():
        is_dark[0] = not is_dark[0]
        if is_dark[0]:
            # Apply Dark Color Rules
            root.configure(bg="#1E1E1E")
            toolbar.configure(bg="#2D2D2D")
            search_lbl.configure(bg="#2D2D2D", fg="white")
            clear_btn.configure(bg="#3E3E3E", fg="white")
            theme_btn.configure(text="☀️ Light Mode", bg="#3E3E3E", fg="white")
            chat_area.configure(bg="#121212", insertbackground="white")
            chat_area.tag_configure("text_style", foreground="#E0E0E0")
            typing_label.configure(bg="#1E1E1E", fg="#A0A0A0")
            input_frame.configure(bg="#1E1E1E")
            entry.configure(bg="#2D2D2D", fg="white", highlightbackground="#444444", highlightcolor=theme_color, insertbackground="white")
            counter_lbl.configure(bg="#1E1E1E", fg="#A0A0A0")
        else:
            # Revert to Light Theme Rules
            root.configure(bg="#F0F2F5")
            toolbar.configure(bg="#EAEAEA")
            search_lbl.configure(bg="#EAEAEA", fg="black")
            clear_btn.configure(bg="#D4D4D4", fg="black")
            theme_btn.configure(text="🌙 Dark Mode", bg="#D4D4D4", fg="black")
            chat_area.configure(bg="#E5DDD5")
            chat_area.tag_configure("text_style", foreground="#000000")
            typing_label.configure(bg="#F0F2F5", fg="#555555")
            input_frame.configure(bg="#F0F2F5")
            entry.configure(bg="white", fg="black", highlightbackground="#CCCCCC", highlightcolor=theme_color, insertbackground="black")
            counter_lbl.configure(bg="#F0F2F5", fg="#777777")

    theme_btn = Button(toolbar, text="🌙 Dark Mode", font=("Helvetica", 9), bg="#D4D4D4", fg="black", bd=0, padx=8, cursor="hand2", command=toggle_theme)
    theme_btn.pack(side=RIGHT, padx=5)

    return root, chat_area, entry, send_btn, typing_label

def append_message(chat_area, sender, message, side, timestamp, is_self=False):
    chat_area.config(state=NORMAL)
    align_tag = "right" if side == "right" else "left"
    name_tag = "self_msg" if is_self else "other_msg"
    
    chat_area.insert("end", f"{sender}  ", (name_tag, align_tag))
    chat_area.insert("end", f"{timestamp}\n", ("time_style", align_tag))
    chat_area.insert("end", f"{message}\n\n", ("text_style", align_tag))
        
    chat_area.config(state=DISABLED)
    chat_area.see("end")

def load_history_into_ui(chat_area, current_user):
    from database import get_chat_history
    history = get_chat_history()
    for sender, message, timestamp in history:
        if sender == current_user:
            append_message(chat_area, "You", message, "right", timestamp, is_self=True)
        else:
            append_message(chat_area, sender, message, "left", timestamp, is_self=False)