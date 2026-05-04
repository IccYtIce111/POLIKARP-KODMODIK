import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import webbrowser
from datetime import datetime

FAVORITES_FILE = "favorites.json"

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, indent=4, ensure_ascii=False)

def refresh_favorites_listbox(favorites_listbox, favorites):
    favorites_listbox.delete(0, tk.END)
    for user in favorites:
        display = f"⭐ {user['login']} — {user.get('name', 'Без имени')} (Реп.: {user['public_repos']}, Подп.: {user['followers']})"
        favorites_listbox.insert(tk.END, display)

def search_user(search_entry, results_listbox):
    username = search_entry.get().strip()
    
    if not username:
        messagebox.showwarning("Ошибка ввода", "Поле поиска не должно быть пустым!")
        return
    
    results_listbox.delete(0, tk.END)
    
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        
        if response.status_code == 200:
            user_data = response.json()
            display_text = f"{user_data['login']} — {user_data.get('name', 'Имя не указано')} (Репозиториев: {user_data['public_repos']})"
            results_listbox.insert(tk.END, display_text)
            results_listbox.current_user = user_data
        elif response.status_code == 404:
            messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден на GitHub.")
        else:
            messagebox.showerror("Ошибка API", f"Ошибка {response.status_code}: {response.text}")
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Сетевая ошибка", f"Не удалось соединиться с GitHub API: {e}")

def add_to_favorites(results_listbox, favorites, favorites_listbox):
    if not hasattr(results_listbox, 'current_user') or not results_listbox.current_user:
        messagebox.showinfo("Инфо", "Сначала найдите пользователя.")
        return
    
    user = results_listbox.current_user
    user_id = user['id']
    user_login = user['login']
    
    if any(fav['id'] == user_id for fav in favorites):
        messagebox.showinfo("Инфо", f"Пользователь @{user_login} уже в избранном.")
        return
    
    favorite = {
        'id': user_id,
        'login': user_login,
        'name': user.get('name', ''),
        'html_url': user['html_url'],
        'public_repos': user['public_repos'],
        'followers': user['followers'],
        'added_at': datetime.now().isoformat()
    }
    favorites.append(favorite)
    save_favorites(favorites)
    refresh_favorites_listbox(favorites_listbox, favorites)
    messagebox.showinfo("Успех", f"Пользователь @{user_login} добавлен в избранное!")

def remove_from_favorites(favorites_listbox, favorites, favorites_listbox_widget):
    selection = favorites_listbox.curselection()
    if not selection:
        messagebox.showwarning("Внимание", "Выберите пользователя для удаления.")
        return
    
    index = selection[0]
    removed = favorites.pop(index)
    save_favorites(favorites)
    refresh_favorites_listbox(favorites_listbox_widget, favorites)
    messagebox.showinfo("Успех", f"Пользователь @{removed['login']} удалён из избранного.")

def on_select_favorite(event, favorites):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        user = favorites[index]
        webbrowser.open(user['html_url'])

root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("700x600")
root.resizable(False, False)

favorites = load_favorites()

title = tk.Label(root, text="GitHub User Finder", font=("Arial", 18, "bold"))
title.pack(pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Введите имя пользователя:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=5)

results_listbox = tk.Listbox(root, height=10, font=("Arial", 11))
results_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

search_button = tk.Button(search_frame, text="Поиск", command=lambda: search_user(search_entry, results_listbox), bg="#2ea44f", fg="white", font=("Arial", 10, "bold"))
search_button.pack(side=tk.LEFT, padx=5)

search_entry.bind("<Return>", lambda event: search_user(search_entry, results_listbox))

add_fav_button = tk.Button(root, text="★ Добавить в избранное", command=lambda: add_to_favorites(results_listbox, favorites, favorites_listbox), bg="#ffc107", font=("Arial", 10, "bold"))
add_fav_button.pack(pady=5)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, pady=10, padx=20)

fav_label = tk.Label(root, text="Избранные пользователи", font=("Arial", 14, "bold"))
fav_label.pack()

favorites_listbox = tk.Listbox(root, height=8, font=("Arial", 11))
favorites_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
favorites_listbox.bind("<<ListboxSelect>>", lambda event: on_select_favorite(event, favorites))

remove_fav_button = tk.Button(root, text="✖ Удалить из избранного", command=lambda: remove_from_favorites(favorites_listbox, favorites, favorites_listbox), bg="#dc3545", fg="white", font=("Arial", 10, "bold"))
remove_fav_button.pack(pady=5)

refresh_favorites_listbox(favorites_listbox, favorites)

root.mainloop()
