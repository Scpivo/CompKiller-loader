import sys
import os
import time
import threading
import ctypes
from tkinter import *
from tkinter import ttk, messagebox
import pymem
from pymem.process import inject_dll_from_path

class CompKillerLoader:
    def __init__(self):
        self.root = Tk()
        self.root.title("CompKiller Loader")
        self.root.geometry("550x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#0c0c0c')
        
        # GameSense стиль
        self.bg_color = '#0c0c0c'
        self.fg_color = '#ffffff'
        self.accent_color = '#00ff00'
        self.secondary_color = '#1a1a1a'
        self.error_color = '#ff3333'
        
        # Центрируем окно
        self.center_window()
        
        # Переменные
        self.dll_name = "autizm.dll"
        self.dll_path = None
        self.injecting = False
        self.process_found = False
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Проверяем DLL сразу при запуске
        self.check_dll()
        
        # Проверяем права админа
        if not self.is_admin():
            self.show_error("Run as Administrator!")
            self.root.after(100, self.root.destroy)
            return
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def center_window(self):
        """Центрируем окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создаем интерфейс в стиле GameSense"""
        
        # Main frame
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = Frame(main_frame, bg=self.bg_color)
        header_frame.pack(fill=X, pady=(0, 20))
        
        # Title with GameSense style
        title_label = Label(header_frame, text="CompKiller", 
                          font=("Segoe UI", 24, "bold"), 
                          fg=self.accent_color, bg=self.bg_color)
        title_label.pack(side=LEFT)
        
        version_label = Label(header_frame, text="Loader v1.0", 
                            font=("Segoe UI", 10), 
                            fg='#666666', bg=self.bg_color)
        version_label.pack(side=LEFT, padx=(10, 0), pady=(10, 0))
        
        # Separator
        separator = Frame(main_frame, height=2, bg='#1a1a1a')
        separator.pack(fill=X, pady=(0, 20))
        
        # Status frames
        status_frame = Frame(main_frame, bg=self.bg_color)
        status_frame.pack(fill=X, pady=(0, 20))
        
        # DLL Status
        dll_frame = Frame(status_frame, bg=self.secondary_color, relief=FLAT, bd=1)
        dll_frame.pack(fill=X, pady=(0, 10))
        
        Label(dll_frame, text="DLL STATUS:", 
              font=("Segoe UI", 9, "bold"), 
              fg='#888888', bg=self.secondary_color).pack(anchor=W, padx=10, pady=(10, 0))
        
        self.dll_status = Label(dll_frame, text="Checking...", 
                              font=("Segoe UI", 11, "bold"), 
                              fg=self.fg_color, bg=self.secondary_color)
        self.dll_status.pack(anchor=W, padx=10, pady=(0, 10))
        
        # CS2 Status
        cs2_frame = Frame(status_frame, bg=self.secondary_color, relief=FLAT, bd=1)
        cs2_frame.pack(fill=X)
        
        Label(cs2_frame, text="CS2 STATUS:", 
              font=("Segoe UI", 9, "bold"), 
              fg='#888888', bg=self.secondary_color).pack(anchor=W, padx=10, pady=(10, 0))
        
        self.cs2_status = Label(cs2_frame, text="Not running", 
                              font=("Segoe UI", 11, "bold"), 
                              fg=self.error_color, bg=self.secondary_color)
        self.cs2_status.pack(anchor=W, padx=10, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=460, mode='determinate',
                                       style="GameSense.Horizontal.TProgressbar")
        self.progress.pack(pady=(20, 10))
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("GameSense.Horizontal.TProgressbar",
                       background=self.accent_color,
                       troughcolor=self.secondary_color,
                       bordercolor=self.secondary_color,
                       lightcolor=self.accent_color,
                       darkcolor=self.accent_color)
        
        # Inject button
        self.inject_btn = Button(main_frame, text="START INJECTION", 
                               font=("Segoe UI", 12, "bold"),
                               bg=self.secondary_color, fg=self.fg_color,
                               width=30, height=2,
                               command=self.start_injection,
                               cursor="hand2",
                               state=DISABLED,
                               relief=FLAT,
                               activebackground='#2a2a2a',
                               activeforeground=self.fg_color)
        self.inject_btn.pack(pady=(10, 20))
        
        # Log area
        log_frame = Frame(main_frame, bg=self.secondary_color, relief=FLAT, bd=1)
        log_frame.pack(fill=BOTH, expand=True)
        
        Label(log_frame, text="INJECTION LOG:", 
              font=("Segoe UI", 9, "bold"), 
              fg='#888888', bg=self.secondary_color).pack(anchor=W, padx=10, pady=(10, 5))
        
        # Log text with scrollbar
        log_container = Frame(log_frame, bg=self.secondary_color)
        log_container.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = Scrollbar(log_container)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.log_text = Text(log_container, height=8, 
                            bg='#111111', fg=self.accent_color,
                            font=("Consolas", 9), 
                            relief=FLAT,
                            insertbackground=self.accent_color,
                            selectbackground='#2a2a2a',
                            yscrollcommand=scrollbar.set)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        self.log_text.insert(END, "> CompKiller Loader initialized\n")
        self.log_text.config(state=DISABLED)
        
        # Footer
        footer_frame = Frame(main_frame, bg=self.bg_color)
        footer_frame.pack(fill=X, pady=(20, 0))
        
        Label(footer_frame, text="⚠️ Remove -insecure from CS2 launch options", 
              font=("Segoe UI", 8), 
              fg='#888888', bg=self.bg_color).pack()
        
        # Обновляем статус CS2 каждые 2 секунды
        self.update_cs2_status()
    
    def log(self, message):
        """Добавляем сообщение в лог"""
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, f"> {message}\n")
        self.log_text.see(END)
        self.log_text.config(state=DISABLED)
        self.root.update()
    
    def is_admin(self):
        """Проверка прав администратора"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def get_exe_dir(self):
        """Получаем папку где находится exe файл"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))
    
    def check_dll(self):
        """Проверяем наличие DLL в папке с exe"""
        exe_dir = self.get_exe_dir()
        self.dll_path = os.path.join(exe_dir, self.dll_name)
        
        if os.path.exists(self.dll_path):
            self.dll_status.config(text=f"✓ {self.dll_name} FOUND", fg=self.accent_color)
            self.log(f"DLL found: {os.path.basename(self.dll_path)}")
            self.inject_btn.config(state=NORMAL, bg=self.accent_color, fg='#000000')
            return True
        else:
            self.dll_status.config(text=f"✗ {self.dll_name} NOT FOUND", fg=self.error_color)
            self.log(f"ERROR: {self.dll_name} not found in directory!")
            self.log(f"Place file in: {exe_dir}")
            self.inject_btn.config(state=DISABLED, bg=self.secondary_color, fg=self.fg_color)
            return False
    
    def update_cs2_status(self):
        """Обновляем статус CS2"""
        try:
            pm = pymem.Pymem('cs2.exe')
            self.cs2_status.config(text="✓ CS2 RUNNING", fg=self.accent_color)
            self.process_found = True
        except:
            self.cs2_status.config(text="✗ CS2 NOT RUNNING", fg=self.error_color)
            self.process_found = False
        
        # Повторяем каждые 2 секунды
        self.root.after(2000, self.update_cs2_status)
    
    def find_cs2_process(self):
        """Ищем процесс CS2"""
        try:
            process_names = ['cs2.exe', 'cs2_x64.exe', 'Counter-Strike 2.exe']
            
            for name in process_names:
                try:
                    pm = pymem.Pymem(name)
                    self.log(f"Found process: {name} (PID: {pm.process_id})")
                    return pm
                except:
                    continue
            
            return None
        except Exception as e:
            self.log(f"Process search error: {e}")
            return None
    
    def start_injection(self):
        """Начинаем инжект"""
        if self.injecting:
            return
        
        if not self.check_dll():
            messagebox.showerror("Error", 
                f"File {self.dll_name} not found!\n\n"
                f"Place it in folder:\n{self.get_exe_dir()}")
            return
        
        # Запускаем в отдельном потоке
        self.injecting = True
        self.inject_btn.config(state=DISABLED, text="INJECTING...", 
                              bg=self.secondary_color, fg=self.fg_color)
        self.log_text.config(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.config(state=DISABLED)
        
        thread = threading.Thread(target=self.injection_thread, daemon=True)
        thread.start()
    
    def injection_thread(self):
        """Поток инжекта"""
        try:
            self.log("=" * 50)
            self.log("STARTING INJECTION PROCESS")
            self.log("=" * 50)
            
            # 1. Проверяем процесс CS2
            self.progress['value'] = 10
            self.log("\n[1] Searching for CS2...")
            
            cs2 = self.find_cs2_process()
            
            if not cs2:
                self.log("CS2 not running. Launching...")
                
                # Запускаем Steam если не запущен
                try:
                    pymem.Pymem('steam.exe')
                    self.log("Steam already running")
                except:
                    self.log("Launching Steam...")
                    os.startfile('steam://open/main')
                    time.sleep(8)
                
                # Запускаем CS2
                self.log("Launching CS2...")
                os.startfile('steam://run/730')
                
                # Ждем запуска
                self.log("Waiting for CS2 to start...")
                for i in range(30):
                    self.progress['value'] = 10 + (i * 2)
                    self.root.update()
                    
                    cs2 = self.find_cs2_process()
                    if cs2:
                        break
                    time.sleep(1)
                
                if not cs2:
                    raise Exception("CS2 failed to launch within 30 seconds")
            
            self.log(f"CS2 found! PID: {cs2.process_id}")
            self.progress['value'] = 40
            
            # 2. Ждем загрузки игры
            self.log("\n[2] Waiting for game to load...")
            for i in range(5):
                self.log(f"Loading... {i+1}/5 seconds")
                self.progress['value'] = 40 + (i * 5)
                time.sleep(1)
                self.root.update()
            
            self.progress['value'] = 70
            
            # 3. ВЫПОЛНЯЕМ ИНЖЕКТ
            self.log("\n[3] PERFORMING INJECTION...")
            self.log(f"Injecting: {self.dll_name}")
            
            # ИНЖЕКТ ЧЕРЕЗ PYMEM
            inject_dll_from_path(cs2.process_handle, self.dll_path)
            
            self.progress['value'] = 100
            
            # УСПЕХ
            self.log("\n" + "=" * 50)
            self.log("✓ INJECTION SUCCESSFUL!")
            self.log("=" * 50)
            self.log("\nCheat activated. Ready to play!")
            
            # Меняем цвет кнопки на успех
            self.inject_btn.config(text="✓ INJECTION COMPLETE", 
                                  bg=self.accent_color, fg='#000000')
            
            # Автозакрытие через 5 секунд
            self.root.after(5000, self.root.destroy)
            
        except Exception as e:
            self.log(f"\n✗ INJECTION ERROR: {str(e)}")
            self.progress['value'] = 0
            
            # Показываем окно ошибки
            self.root.after(100, lambda: messagebox.showerror(
                "Injection Error",
                f"Injection failed:\n\n{str(e)}\n\n"
                "Check:\n"
                "1. Run as Administrator\n"
                "2. Disable antivirus\n"
                "3. Remove -insecure from launch options\n"
                "4. Verify DLL version"
            ))
            
            # Возвращаем кнопку в исходное состояние
            self.inject_btn.config(text="START INJECTION", 
                                  bg=self.accent_color, fg='#000000')
        
        finally:
            self.injecting = False
    
    def show_error(self, message):
        """Показываем ошибку"""
        messagebox.showerror("Error", message)
    
    def on_closing(self):
        """При закрытии окна"""
        self.root.destroy()

# Точка входа
if __name__ == "__main__":
    # Проверяем наличие pymem
    try:
        import pymem
        from pymem.process import inject_dll_from_path
    except ImportError:
        print("Install pymem: pip install pymem")
        messagebox.showerror("Error", 
            "Pymem library not installed!\n\n"
            "Install via command prompt:\n"
            "pip install pymem")
        sys.exit(1)
    
    # Запускаем приложение
    app = CompKillerLoader()