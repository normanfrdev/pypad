import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import webbrowser
from tkinter import PhotoImage
import datetime

current_file = None  # to get current file

def update_title(file_name=None):
    if file_name:
        root.title(f"{file_name}")
    else:
        root.title("Untitled")

def new_file(event=None):
    if ask_save_before_closing(event=None):
        global current_file
        text_area.delete(1.0, tk.END)
        current_file = None
        update_title()

def open_file(event=None):
    if ask_save_before_closing(event=None):
        file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                               filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    text_area.delete(1.0, tk.END)
                    text_area.insert(tk.END, file.read())
                    global current_file
                    current_file = file_path
                    update_title(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

def save_file(event=None):
    global current_file
    if current_file:
        try:
            with open(current_file, "w") as file:
                file.write(text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    else:
        save_file_as()

def save_file_as(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, tk.END))
                global current_file
                current_file = file_path
                update_title(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

def ask_save_before_closing(event=None):
    if text_area.edit_modified():
        response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
        if response:  # if we wanna save
            save_file()
            return True
        elif response is False:  # if not
            return True
        else:  # if cancel
            return False
    return True

def on_closing(event=None):
    if ask_save_before_closing():
        root.destroy()

# Edit menu
def undo(event=None):
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass

def cut(event=None):
    text_area.event_generate("<<Cut>>")

def copy(event=None):
    text_area.event_generate("<<Copy>>")

def paste(event=None):
    text_area.event_generate("<<Paste>>")

def delete(event=None):
    text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

def search_with_web(event=None):
    query = text_area.selection_get()
    #No you can't change search engine. live with google
    webbrowser.open(f"https://www.google.com/search?q={query}")

def find(event=None):
    find_string = simpledialog.askstring("Find", "Enter text to find:")
    if find_string:
        start_pos = text_area.search(find_string, "1.0", stopindex=tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(find_string)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.tag_config("highlight", background="yellow", foreground="black")
            text_area.mark_set("insert", end_pos)
            text_area.see("insert")

def find_next(event=None):
    find_string = simpledialog.askstring("Find Next", "Enter text to find next:")
    if find_string:
        start_pos = text_area.search(find_string, tk.INSERT, stopindex=tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(find_string)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.tag_config("highlight", background="yellow", foreground="black")
            text_area.mark_set("insert", end_pos)
            text_area.see("insert")

def find_previous(event=None):
    find_string = simpledialog.askstring("Find Previous", "Enter text to find previous:")
    if find_string:
        start_pos = text_area.search(find_string, tk.INSERT, stopindex="1.0", backwards=True)
        if start_pos:
            end_pos = f"{start_pos}+{len(find_string)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.tag_config("highlight", background="yellow", foreground="black")
            text_area.mark_set("insert", start_pos)
            text_area.see("insert")

def replace(event=None):
    find_string = simpledialog.askstring("Replace", "Enter text to find:")
    replace_string = simpledialog.askstring("Replace", "Enter text to replace with:")
    if find_string and replace_string:
        content = text_area.get("1.0", tk.END)
        new_content = content.replace(find_string, replace_string)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", new_content)

def go_to(event=None):
    line = simpledialog.askinteger("Go To", "Enter line number:")
    if line:
        text_area.mark_set("insert", f"{line}.0")
        text_area.see("insert")

def select_all(event=None):
    text_area.tag_add("sel", "1.0", "end")

def time_date(event=None):
    current_time = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")
    text_area.insert(tk.INSERT, current_time)

def change_font(event=None):
    font_choice = simpledialog.askstring("Font", "Enter font name (e.g., Arial):")
    size_choice = simpledialog.askinteger("Font", "Enter font size (e.g., 12):")
    if font_choice and size_choice:
        new_font = font.Font(family=font_choice, size=size_choice)
        text_area.configure(font=new_font)


root = tk.Tk()
root.title("Untitled")


text_area = tk.Text(root, undo=True, wrap='word')
text_area.pack(expand=True, fill='both')
text_area.edit_modified(False)

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File thing
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As...", command=save_file_as, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing, accelerator="Alt+F4")

# Edit thing
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
edit_menu.add_command(label="Delete", command=delete, accelerator="Del")
edit_menu.add_separator()
edit_menu.add_command(label="Search with Web", command=search_with_web, accelerator="Ctrl+E")
edit_menu.add_command(label="Find", command=find, accelerator="Ctrl+F")
edit_menu.add_command(label="Find Next", command=find_next, accelerator="F3")
edit_menu.add_command(label="Find Previous", command=find_previous, accelerator="Shift+F3")
edit_menu.add_command(label="Replace", command=replace, accelerator="Ctrl+H")
edit_menu.add_command(label="Go To", command=go_to, accelerator="Ctrl+G")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
edit_menu.add_command(label="Time/Date", command=time_date, accelerator="F5")
edit_menu.add_separator()
edit_menu.add_command(label="Font", command=change_font)

root.protocol("WM_DELETE_WINDOW", on_closing)

# A bunch of bindings. There is probably easier way to do this but ok.
root.bind_all("<Control-n>", new_file)
root.bind_all("<Control-o>", open_file)
root.bind_all("<Control-s>", save_file)
root.bind_all("<Control-Shift-s>", save_file_as)
root.bind_all("<Control-z>", undo)
root.bind_all("<Control-x>", cut)
root.bind_all("<Control-c>", copy)
root.bind_all("<Control-v>", paste)
root.bind_all("<Delete>", delete)
root.bind_all("<Control-e>", search_with_web)
root.bind_all("<Control-f>", find)
root.bind_all("<F3>", find_next)
root.bind_all("<Shift-F3>", find_previous)
root.bind_all("<Control-h>", replace)
root.bind_all("<Control-g>", go_to)
root.bind_all("<Control-a>", select_all)
root.bind_all("<F5>", time_date)

# Ah yeah. Final line.
root.mainloop()