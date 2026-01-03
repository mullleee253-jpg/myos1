#!/usr/bin/env python3
"""
MyOS Desktop Environment - Windows 11 Style
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from datetime import datetime

class Window:
    """Draggable window with title bar"""
    def __init__(self, desktop, title="Window", width=400, height=300, content=None):
        self.desktop = desktop
        self.frame = tk.Frame(desktop.canvas, bg='#202020', highlightthickness=1, 
                             highlightbackground='#404040')
        
        # Title bar
        self.titlebar = tk.Frame(self.frame, bg='#202020', height=32)
        self.titlebar.pack(fill='x')
        self.titlebar.pack_propagate(False)
        
        self.title_label = tk.Label(self.titlebar, text=title, bg='#202020', 
                                    fg='white', font=('Segoe UI', 10))
        self.title_label.pack(side='left', padx=10)
        
        # Window controls
        btn_style = {'bg': '#202020', 'fg': 'white', 'bd': 0, 'width': 4, 
                    'font': ('Segoe UI', 10), 'activebackground': '#404040'}
        
        tk.Button(self.titlebar, text='✕', command=self.close,
                 activebackground='#e81123', **btn_style).pack(side='right')
        tk.Button(self.titlebar, text='□', command=self.maximize, **btn_style).pack(side='right')
        tk.Button(self.titlebar, text='─', command=self.minimize, **btn_style).pack(side='right')
        
        # Content area
        self.content = tk.Frame(self.frame, bg='#1a1a1a', width=width, height=height-32)
        self.content.pack(fill='both', expand=True)
        self.content.pack_propagate(False)
        
        if content:
            content(self.content)
        
        # Make draggable
        self.titlebar.bind('<Button-1>', self.start_drag)
        self.titlebar.bind('<B1-Motion>', self.drag)
        self.title_label.bind('<Button-1>', self.start_drag)
        self.title_label.bind('<B1-Motion>', self.drag)
        
        # Position
        self.x = 100 + len(desktop.windows) * 30
        self.y = 100 + len(desktop.windows) * 30
        self.window_id = desktop.canvas.create_window(self.x, self.y, window=self.frame, anchor='nw')
        desktop.windows.append(self)
        
    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y
        self.frame.lift()
        
    def drag(self, event):
        self.x += event.x - self.drag_x
        self.y += event.y - self.drag_y
        self.desktop.canvas.coords(self.window_id, self.x, self.y)
        
    def close(self):
        self.desktop.canvas.delete(self.window_id)
        self.frame.destroy()
        if self in self.desktop.windows:
            self.desktop.windows.remove(self)
            
    def minimize(self):
        self.frame.lower()
        
    def maximize(self):
        self.x, self.y = 0, 0
        self.desktop.canvas.coords(self.window_id, 0, 0)
        self.content.config(width=self.desktop.screen_w, height=self.desktop.screen_h-80)


class Desktop:
    """Main desktop environment"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MyOS")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000')
        
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        
        self.windows = []
        self.start_menu_open = False
        
        # Desktop canvas with wallpaper
        self.canvas = tk.Canvas(self.root, bg='#0078d4', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Draw gradient wallpaper (Windows 11 style)
        self.draw_wallpaper()
        
        # Desktop icons
        self.create_desktop_icons()
        
        # Taskbar
        self.create_taskbar()
        
        # Start menu (hidden initially)
        self.create_start_menu()
        
        # Bind keys
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('<Super_L>', lambda e: self.toggle_start_menu())
        
        # Update clock
        self.update_clock()
        
    def draw_wallpaper(self):
        """Draw Windows 11 style gradient wallpaper"""
        for i in range(self.screen_h):
            ratio = i / self.screen_h
            r = int(0 + (30 * ratio))
            g = int(120 - (60 * ratio))
            b = int(212 - (100 * ratio))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, self.screen_w, i, fill=color)
            
    def create_desktop_icons(self):
        """Create desktop icons"""
        icons = [
            ("💻", "This PC", self.open_file_manager),
            ("📁", "Documents", self.open_file_manager),
            ("🗑️", "Recycle Bin", lambda: None),
            ("⚙️", "Settings", self.open_settings),
            ("📝", "Notepad", self.open_notepad),
            ("🖥️", "Terminal", self.open_terminal),
        ]
        
        y = 20
        for icon, name, cmd in icons:
            frame = tk.Frame(self.canvas, bg='')
            frame.configure(bg='#0078d4')
            
            icon_label = tk.Label(frame, text=icon, font=('Segoe UI Emoji', 32), 
                                 bg='#0078d4', fg='white')
            icon_label.pack()
            
            name_label = tk.Label(frame, text=name, font=('Segoe UI', 9), 
                                 bg='#0078d4', fg='white')
            name_label.pack()
            
            self.canvas.create_window(50, y, window=frame, anchor='nw')
            
            # Bind click
            for widget in [frame, icon_label, name_label]:
                widget.bind('<Double-Button-1>', lambda e, c=cmd: c())
                
            y += 90
            
    def create_taskbar(self):
        """Create Windows 11 style centered taskbar"""
        self.taskbar = tk.Frame(self.root, bg='#1f1f1f', height=48)
        self.taskbar.pack(side='bottom', fill='x')
        self.taskbar.pack_propagate(False)
        
        # Center container
        center = tk.Frame(self.taskbar, bg='#1f1f1f')
        center.pack(expand=True)
        
        # Start button (centered like Win11)
        btn_style = {'bg': '#1f1f1f', 'fg': 'white', 'bd': 0, 
                    'font': ('Segoe UI Emoji', 16), 'activebackground': '#3d3d3d',
                    'width': 3, 'height': 1}
        
        self.start_btn = tk.Button(center, text='⊞', command=self.toggle_start_menu, **btn_style)
        self.start_btn.pack(side='left', padx=2)
        
        tk.Button(center, text='🔍', command=self.open_search, **btn_style).pack(side='left', padx=2)
        tk.Button(center, text='📁', command=self.open_file_manager, **btn_style).pack(side='left', padx=2)
        tk.Button(center, text='🌐', command=self.open_browser, **btn_style).pack(side='left', padx=2)
        tk.Button(center, text='📝', command=self.open_notepad, **btn_style).pack(side='left', padx=2)
        tk.Button(center, text='🖥️', command=self.open_terminal, **btn_style).pack(side='left', padx=2)
        
        # System tray (right side)
        tray = tk.Frame(self.taskbar, bg='#1f1f1f')
        tray.pack(side='right', padx=10)
        
        tk.Label(tray, text='🔊 📶 🔋', bg='#1f1f1f', fg='white', 
                font=('Segoe UI Emoji', 12)).pack(side='left', padx=5)
        
        self.clock_label = tk.Label(tray, text='', bg='#1f1f1f', fg='white',
                                   font=('Segoe UI', 10))
        self.clock_label.pack(side='left', padx=10)

        
    def create_start_menu(self):
        """Create Windows 11 style start menu"""
        self.start_menu = tk.Frame(self.root, bg='#202020', width=600, height=500)
        
        # Search bar
        search_frame = tk.Frame(self.start_menu, bg='#202020')
        search_frame.pack(fill='x', padx=20, pady=15)
        
        self.search_entry = tk.Entry(search_frame, bg='#3d3d3d', fg='white', 
                                    font=('Segoe UI', 11), insertbackground='white',
                                    relief='flat', width=50)
        self.search_entry.insert(0, '🔍 Type here to search')
        self.search_entry.pack(fill='x', ipady=8)
        
        # Pinned section
        tk.Label(self.start_menu, text='Pinned', bg='#202020', fg='white',
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=20, pady=(10,5))
        
        pinned = tk.Frame(self.start_menu, bg='#202020')
        pinned.pack(fill='x', padx=20)
        
        apps = [
            ('📁', 'Files', self.open_file_manager),
            ('📝', 'Notepad', self.open_notepad),
            ('🖥️', 'Terminal', self.open_terminal),
            ('⚙️', 'Settings', self.open_settings),
            ('🎨', 'Paint', self.open_paint),
            ('🧮', 'Calculator', self.open_calculator),
        ]
        
        for i, (icon, name, cmd) in enumerate(apps):
            btn = tk.Button(pinned, text=f'{icon}\n{name}', bg='#202020', fg='white',
                          font=('Segoe UI', 9), bd=0, width=8, height=3,
                          activebackground='#3d3d3d', command=lambda c=cmd: [c(), self.toggle_start_menu()])
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
            
        # Recommended section
        tk.Label(self.start_menu, text='Recommended', bg='#202020', fg='white',
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=20, pady=(20,5))
        
        # Power button
        power_frame = tk.Frame(self.start_menu, bg='#202020')
        power_frame.pack(side='bottom', fill='x', padx=20, pady=15)
        
        tk.Label(power_frame, text='👤 User', bg='#202020', fg='white',
                font=('Segoe UI', 10)).pack(side='left')
        
        tk.Button(power_frame, text='⏻', bg='#202020', fg='white', bd=0,
                 font=('Segoe UI', 14), activebackground='#3d3d3d',
                 command=self.show_power_menu).pack(side='right')
                 
    def toggle_start_menu(self):
        """Show/hide start menu"""
        if self.start_menu_open:
            self.start_menu.place_forget()
        else:
            x = (self.screen_w - 600) // 2
            y = self.screen_h - 48 - 500
            self.start_menu.place(x=x, y=y)
        self.start_menu_open = not self.start_menu_open
        
    def update_clock(self):
        """Update taskbar clock"""
        now = datetime.now()
        self.clock_label.config(text=now.strftime('%H:%M\n%d.%m.%Y'))
        self.root.after(1000, self.update_clock)
        
    def show_power_menu(self):
        """Show power options"""
        result = messagebox.askquestion("Power", "Shut down MyOS?")
        if result == 'yes':
            self.root.quit()
            
    # Application launchers
    def open_file_manager(self):
        def content(parent):
            tk.Label(parent, text='📁 This PC', bg='#1a1a1a', fg='white',
                    font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=10, pady=10)
            
            items = ['💾 Local Disk (C:)', '💿 DVD Drive (D:)', '📁 Documents', 
                    '📁 Downloads', '📁 Pictures', '📁 Music']
            for item in items:
                tk.Label(parent, text=item, bg='#1a1a1a', fg='white',
                        font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=2)
                        
        Window(self, "File Explorer", 500, 400, content)
        
    def open_notepad(self):
        def content(parent):
            text = tk.Text(parent, bg='#1e1e1e', fg='white', font=('Consolas', 11),
                          insertbackground='white', relief='flat')
            text.pack(fill='both', expand=True, padx=2, pady=2)
            
        Window(self, "Notepad", 500, 400, content)
        
    def open_terminal(self):
        def content(parent):
            text = tk.Text(parent, bg='#0c0c0c', fg='#cccccc', font=('Consolas', 11),
                          insertbackground='white', relief='flat')
            text.pack(fill='both', expand=True)
            text.insert('1.0', 'MyOS Terminal v1.0\n© 2024 MyOS\n\nC:\\Users\\User> ')
            
        Window(self, "Terminal", 600, 400, content)
        
    def open_settings(self):
        def content(parent):
            tk.Label(parent, text='⚙️ Settings', bg='#1a1a1a', fg='white',
                    font=('Segoe UI', 16, 'bold')).pack(anchor='w', padx=20, pady=15)
            
            settings = ['🖥️ System', '📱 Devices', '📶 Network', '🎨 Personalization',
                       '🔒 Privacy', '🔄 Update']
            for s in settings:
                btn = tk.Button(parent, text=s, bg='#2d2d2d', fg='white',
                              font=('Segoe UI', 10), bd=0, anchor='w', padx=15,
                              activebackground='#3d3d3d')
                btn.pack(fill='x', padx=10, pady=2)
                
        Window(self, "Settings", 450, 400, content)
        
    def open_search(self):
        self.toggle_start_menu()
        self.search_entry.focus_set()
        
    def open_browser(self):
        def content(parent):
            toolbar = tk.Frame(parent, bg='#2d2d2d', height=40)
            toolbar.pack(fill='x')
            toolbar.pack_propagate(False)
            
            tk.Button(toolbar, text='←', bg='#2d2d2d', fg='white', bd=0).pack(side='left', padx=5)
            tk.Button(toolbar, text='→', bg='#2d2d2d', fg='white', bd=0).pack(side='left')
            tk.Button(toolbar, text='🔄', bg='#2d2d2d', fg='white', bd=0).pack(side='left', padx=5)
            
            url = tk.Entry(toolbar, bg='#1a1a1a', fg='white', font=('Segoe UI', 10),
                          relief='flat', width=40)
            url.pack(side='left', padx=10, ipady=5, fill='x', expand=True)
            url.insert(0, 'https://myos.local')
            
            page = tk.Label(parent, text='🌐\n\nWelcome to MyOS Browser\n\nNo internet connection',
                          bg='#1a1a1a', fg='#888888', font=('Segoe UI', 12))
            page.pack(expand=True)
            
        Window(self, "Browser", 700, 500, content)
        
    def open_paint(self):
        def content(parent):
            canvas = tk.Canvas(parent, bg='white', cursor='crosshair')
            canvas.pack(fill='both', expand=True)
            
            def paint(event):
                x, y = event.x, event.y
                canvas.create_oval(x-2, y-2, x+2, y+2, fill='black', outline='black')
                
            canvas.bind('<B1-Motion>', paint)
            
        Window(self, "Paint", 500, 400, content)
        
    def open_calculator(self):
        def content(parent):
            display = tk.Entry(parent, bg='#1a1a1a', fg='white', font=('Segoe UI', 24),
                             justify='right', relief='flat')
            display.pack(fill='x', padx=5, pady=10, ipady=10)
            display.insert(0, '0')
            
            btns = tk.Frame(parent, bg='#1a1a1a')
            btns.pack(fill='both', expand=True, padx=5, pady=5)
            
            buttons = [
                ['C', '±', '%', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '.', '=']
            ]
            
            for i, row in enumerate(buttons):
                for j, btn in enumerate(row):
                    colspan = 2 if btn == '0' else 1
                    tk.Button(btns, text=btn, bg='#3d3d3d', fg='white',
                            font=('Segoe UI', 14), bd=0, width=4, height=2,
                            activebackground='#505050').grid(row=i, column=j, 
                            columnspan=colspan, padx=2, pady=2, sticky='ew')
                            
        Window(self, "Calculator", 250, 350, content)
        
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    desktop = Desktop()
    desktop.run()
