#!/usr/bin/env python3
"""
MyOS Desktop Environment - Windows 11 Style
Works with Tkinter on minimal Linux
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
from datetime import datetime
import webbrowser

class Window:
    """Draggable window"""
    windows = []
    
    def __init__(self, desktop, title="Window", width=400, height=300, content_func=None):
        self.desktop = desktop
        self.is_maximized = False
        self.old_pos = None
        
        # Main frame
        self.frame = tk.Frame(desktop.canvas, bg='#202020', 
                             highlightthickness=1, highlightbackground='#404040')
        
        # Title bar
        titlebar = tk.Frame(self.frame, bg='#202020', height=32)
        titlebar.pack(fill='x')
        titlebar.pack_propagate(False)
        
        # Icon and title
        tk.Label(titlebar, text=title, bg='#202020', fg='white', 
                font=('Segoe UI', 10)).pack(side='left', padx=10)
        
        # Window buttons
        btn_cfg = {'bg': '#202020', 'fg': 'white', 'bd': 0, 'width': 4,
                  'font': ('Segoe UI', 10), 'activebackground': '#404040',
                  'cursor': 'hand2'}
        
        close_btn = tk.Button(titlebar, text='✕', command=self.close, **btn_cfg)
        close_btn.pack(side='right')
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg='#e81123'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg='#202020'))
        
        tk.Button(titlebar, text='□', command=self.toggle_maximize, **btn_cfg).pack(side='right')
        tk.Button(titlebar, text='─', command=self.minimize, **btn_cfg).pack(side='right')
        
        # Content
        self.content = tk.Frame(self.frame, bg='#1a1a1a', width=width, height=height-32)
        self.content.pack(fill='both', expand=True)
        self.content.pack_propagate(False)
        
        if content_func:
            content_func(self.content)
        
        # Dragging
        titlebar.bind('<Button-1>', self.start_drag)
        titlebar.bind('<B1-Motion>', self.drag)
        
        # Position window
        x = 100 + len(Window.windows) * 30
        y = 80 + len(Window.windows) * 30
        self.win_id = desktop.canvas.create_window(x, y, window=self.frame, anchor='nw')
        
        Window.windows.append(self)
        self.frame.lift()
        
    def start_drag(self, e):
        self.drag_x = e.x
        self.drag_y = e.y
        self.frame.lift()
        
    def drag(self, e):
        if self.is_maximized:
            return
        x, y = self.desktop.canvas.coords(self.win_id)
        new_x = x + e.x - self.drag_x
        new_y = max(0, y + e.y - self.drag_y)
        self.desktop.canvas.coords(self.win_id, new_x, new_y)
        
    def close(self):
        self.desktop.canvas.delete(self.win_id)
        self.frame.destroy()
        if self in Window.windows:
            Window.windows.remove(self)
            
    def minimize(self):
        self.frame.lower()
        
    def toggle_maximize(self):
        if self.is_maximized:
            self.desktop.canvas.coords(self.win_id, *self.old_pos)
            self.content.config(width=self.old_size[0], height=self.old_size[1])
            self.is_maximized = False
        else:
            self.old_pos = self.desktop.canvas.coords(self.win_id)
            self.old_size = (self.content.winfo_width(), self.content.winfo_height())
            self.desktop.canvas.coords(self.win_id, 0, 0)
            self.content.config(width=self.desktop.screen_w, height=self.desktop.screen_h - 80)
            self.is_maximized = True


class Desktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MyOS")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000')
        
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        
        self.start_open = False
        
        # Desktop
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Wallpaper gradient
        self.draw_wallpaper()
        
        # Desktop icons
        self.create_icons()
        
        # Taskbar
        self.create_taskbar()
        
        # Start menu
        self.create_start_menu()
        
        # Bindings
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.canvas.bind('<Button-1>', lambda e: self.close_start())
        
        # Clock update
        self.update_clock()
        
    def draw_wallpaper(self):
        for i in range(self.screen_h):
            r = int(0 + (20 * i / self.screen_h))
            g = int(100 - (50 * i / self.screen_h))
            b = int(200 - (80 * i / self.screen_h))
            self.canvas.create_line(0, i, self.screen_w, i, fill=f'#{r:02x}{g:02x}{b:02x}')
            
    def create_icons(self):
        icons = [
            ('💻', 'This PC', self.open_files),
            ('📁', 'Documents', self.open_files),
            ('🌐', 'Browser', self.open_browser),
            ('📝', 'Notepad', self.open_notepad),
            ('🖥️', 'Terminal', self.open_terminal),
            ('⚙️', 'Settings', self.open_settings),
        ]
        
        y = 20
        for icon, name, cmd in icons:
            frame = tk.Frame(self.canvas, bg='')
            
            lbl_icon = tk.Label(frame, text=icon, font=('Segoe UI Emoji', 36), 
                               bg='#0064c8', fg='white')
            lbl_icon.pack()
            
            lbl_name = tk.Label(frame, text=name, font=('Segoe UI', 9),
                               bg='#0064c8', fg='white')
            lbl_name.pack()
            
            self.canvas.create_window(40, y, window=frame, anchor='nw')
            
            for w in [frame, lbl_icon, lbl_name]:
                w.bind('<Double-Button-1>', lambda e, c=cmd: c())
                w.bind('<Enter>', lambda e, f=frame: f.config(bg='#0078d4'))
                w.bind('<Leave>', lambda e, f=frame: f.config(bg='#0064c8'))
                
            y += 90
            
    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg='#1f1f1f', height=48)
        self.taskbar.pack(side='bottom', fill='x')
        self.taskbar.pack_propagate(False)
        
        # Center buttons
        center = tk.Frame(self.taskbar, bg='#1f1f1f')
        center.pack(expand=True)
        
        btn_cfg = {'bg': '#1f1f1f', 'fg': 'white', 'bd': 0, 'width': 4, 'height': 2,
                  'font': ('Segoe UI Emoji', 14), 'activebackground': '#3d3d3d', 'cursor': 'hand2'}
        
        tk.Button(center, text='⊞', command=self.toggle_start, **btn_cfg).pack(side='left', padx=2)
        tk.Button(center, text='🔍', command=self.open_search, **btn_cfg).pack(side='left', padx=2)
        tk.Button(center, text='📁', command=self.open_files, **btn_cfg).pack(side='left', padx=2)
        tk.Button(center, text='🌐', command=self.open_browser, **btn_cfg).pack(side='left', padx=2)
        tk.Button(center, text='📝', command=self.open_notepad, **btn_cfg).pack(side='left', padx=2)
        tk.Button(center, text='🖥️', command=self.open_terminal, **btn_cfg).pack(side='left', padx=2)
        
        # System tray
        tray = tk.Frame(self.taskbar, bg='#1f1f1f')
        tray.pack(side='right', padx=10)
        
        tk.Label(tray, text='🔊 📶', bg='#1f1f1f', fg='white',
                font=('Segoe UI Emoji', 11)).pack(side='left', padx=5)
        
        self.clock = tk.Label(tray, bg='#1f1f1f', fg='white', font=('Segoe UI', 10))
        self.clock.pack(side='left', padx=10)
        
    def create_start_menu(self):
        self.start_menu = tk.Frame(self.root, bg='#202020', width=500, height=450)
        
        # Search
        search = tk.Entry(self.start_menu, bg='#3d3d3d', fg='white', font=('Segoe UI', 11),
                         insertbackground='white', relief='flat', width=40)
        search.pack(padx=20, pady=15, ipady=8)
        search.insert(0, '🔍 Search...')
        
        # Pinned apps
        tk.Label(self.start_menu, text='Pinned', bg='#202020', fg='white',
                font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=20, pady=(10,5))
        
        apps_frame = tk.Frame(self.start_menu, bg='#202020')
        apps_frame.pack(fill='x', padx=20)
        
        apps = [
            ('📁', 'Files', self.open_files),
            ('🌐', 'Browser', self.open_browser),
            ('📝', 'Notepad', self.open_notepad),
            ('🖥️', 'Terminal', self.open_terminal),
            ('⚙️', 'Settings', self.open_settings),
            ('🎨', 'Paint', self.open_paint),
        ]
        
        for i, (icon, name, cmd) in enumerate(apps):
            btn = tk.Button(apps_frame, text=f'{icon}\n{name}', bg='#202020', fg='white',
                          font=('Segoe UI', 9), bd=0, width=8, height=3,
                          activebackground='#3d3d3d', cursor='hand2',
                          command=lambda c=cmd: [c(), self.close_start()])
            btn.grid(row=i//6, column=i%6, padx=4, pady=4)
            
        # Power
        power_frame = tk.Frame(self.start_menu, bg='#202020')
        power_frame.pack(side='bottom', fill='x', padx=20, pady=15)
        
        tk.Label(power_frame, text='👤 User', bg='#202020', fg='white',
                font=('Segoe UI', 10)).pack(side='left')
        
        tk.Button(power_frame, text='⏻', bg='#202020', fg='white', bd=0,
                 font=('Segoe UI', 14), activebackground='#3d3d3d',
                 command=self.shutdown, cursor='hand2').pack(side='right')
                 
    def toggle_start(self):
        if self.start_open:
            self.close_start()
        else:
            x = (self.screen_w - 500) // 2
            y = self.screen_h - 48 - 450
            self.start_menu.place(x=x, y=y)
            self.start_open = True
            
    def close_start(self, e=None):
        self.start_menu.place_forget()
        self.start_open = False
        
    def update_clock(self):
        now = datetime.now()
        self.clock.config(text=now.strftime('%H:%M\n%d.%m.%Y'))
        self.root.after(1000, self.update_clock)
        
    def shutdown(self):
        if messagebox.askyesno('Power', 'Shut down MyOS?'):
            self.root.quit()
            
    # Apps
    def open_files(self):
        def content(parent):
            tk.Label(parent, text='📁 This PC', bg='#1a1a1a', fg='white',
                    font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=10, pady=10)
            
            for item in ['💾 Local Disk (C:)', '📁 Documents', '📁 Downloads', '📁 Pictures']:
                lbl = tk.Label(parent, text=item, bg='#1a1a1a', fg='white',
                              font=('Segoe UI', 10), cursor='hand2')
                lbl.pack(anchor='w', padx=20, pady=2)
                lbl.bind('<Enter>', lambda e, l=lbl: l.config(bg='#333'))
                lbl.bind('<Leave>', lambda e, l=lbl: l.config(bg='#1a1a1a'))
                
        Window(self, '📁 File Explorer', 500, 400, content)
        
    def open_browser(self):
        def content(parent):
            # Toolbar
            toolbar = tk.Frame(parent, bg='#2d2d2d', height=40)
            toolbar.pack(fill='x')
            toolbar.pack_propagate(False)
            
            tk.Button(toolbar, text='←', bg='#2d2d2d', fg='white', bd=0).pack(side='left', padx=5)
            tk.Button(toolbar, text='→', bg='#2d2d2d', fg='white', bd=0).pack(side='left')
            tk.Button(toolbar, text='🔄', bg='#2d2d2d', fg='white', bd=0).pack(side='left', padx=5)
            
            url_var = tk.StringVar(value='https://google.com')
            url = tk.Entry(toolbar, textvariable=url_var, bg='#1a1a1a', fg='white',
                          font=('Segoe UI', 10), relief='flat', width=40)
            url.pack(side='left', padx=10, ipady=5, fill='x', expand=True)
            
            def go():
                addr = url_var.get()
                if not addr.startswith('http'):
                    addr = 'https://' + addr
                try:
                    webbrowser.open(addr)
                    status.config(text=f'Opening {addr}...')
                except:
                    status.config(text='Failed to open browser')
                    
            tk.Button(toolbar, text='Go', bg='#0078d4', fg='white', bd=0,
                     command=go, cursor='hand2').pack(side='left', padx=5)
            url.bind('<Return>', lambda e: go())
            
            # Content
            main = tk.Frame(parent, bg='#1a1a1a')
            main.pack(fill='both', expand=True)
            
            tk.Label(main, text='🌐', font=('Segoe UI Emoji', 48), 
                    bg='#1a1a1a', fg='#666').pack(pady=30)
            tk.Label(main, text='MyOS Browser', font=('Segoe UI', 16),
                    bg='#1a1a1a', fg='white').pack()
            tk.Label(main, text='Enter URL and press Go to open in system browser',
                    bg='#1a1a1a', fg='#888', font=('Segoe UI', 10)).pack(pady=5)
            
            status = tk.Label(main, text='', bg='#1a1a1a', fg='#0078d4', font=('Segoe UI', 9))
            status.pack(pady=10)
            
        Window(self, '🌐 Browser', 650, 450, content)
        
    def open_notepad(self):
        def content(parent):
            text = tk.Text(parent, bg='#1e1e1e', fg='#d4d4d4', font=('Consolas', 11),
                          insertbackground='white', relief='flat', wrap='word')
            text.pack(fill='both', expand=True, padx=2, pady=2)
            text.insert('1.0', 'Welcome to MyOS Notepad!\n\nStart typing...')
            
        Window(self, '📝 Notepad', 500, 400, content)
        
    def open_terminal(self):
        def content(parent):
            text = tk.Text(parent, bg='#0c0c0c', fg='#cccccc', font=('Consolas', 11),
                          insertbackground='white', relief='flat')
            text.pack(fill='both', expand=True)
            text.insert('1.0', '''MyOS Terminal v1.0
© 2024 MyOS

Type commands below:
$ ''')
            text.mark_set('insert', 'end')
            
            def on_enter(e):
                content = text.get('1.0', 'end')
                lines = content.strip().split('\n')
                last_line = lines[-1] if lines else ''
                cmd = last_line.replace('$ ', '').strip()
                
                result = ''
                if cmd == 'help':
                    result = 'Commands: help, ls, pwd, date, clear, whoami, uname'
                elif cmd == 'ls':
                    result = 'Desktop  Documents  Downloads  Pictures  Music'
                elif cmd == 'pwd':
                    result = '/home/user'
                elif cmd == 'date':
                    result = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                elif cmd == 'clear':
                    text.delete('1.0', 'end')
                    result = ''
                elif cmd == 'whoami':
                    result = 'user'
                elif cmd == 'uname':
                    result = 'MyOS 1.0 x86_64'
                elif cmd:
                    result = f"Command not found: {cmd}"
                    
                if result:
                    text.insert('end', f'\n{result}')
                text.insert('end', '\n$ ')
                text.see('end')
                return 'break'
                
            text.bind('<Return>', on_enter)
            
        Window(self, '🖥️ Terminal', 600, 400, content)
        
    def open_settings(self):
        def content(parent):
            tk.Label(parent, text='⚙️ Settings', bg='#1a1a1a', fg='white',
                    font=('Segoe UI', 16, 'bold')).pack(anchor='w', padx=20, pady=15)
            
            for item in ['🖥️ System', '📱 Devices', '📶 Network', '🎨 Personalization', '🔒 Privacy']:
                btn = tk.Button(parent, text=item, bg='#2d2d2d', fg='white',
                              font=('Segoe UI', 10), bd=0, anchor='w', padx=15,
                              activebackground='#3d3d3d', cursor='hand2')
                btn.pack(fill='x', padx=10, pady=2)
                
        Window(self, '⚙️ Settings', 450, 400, content)
        
    def open_paint(self):
        def content(parent):
            canvas = tk.Canvas(parent, bg='white', cursor='crosshair')
            canvas.pack(fill='both', expand=True)
            
            def paint(e):
                x, y = e.x, e.y
                canvas.create_oval(x-3, y-3, x+3, y+3, fill='black', outline='black')
                
            canvas.bind('<B1-Motion>', paint)
            
        Window(self, '🎨 Paint', 500, 400, content)
        
    def open_search(self):
        self.toggle_start()
        
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    try:
        desktop = Desktop()
        desktop.run()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
