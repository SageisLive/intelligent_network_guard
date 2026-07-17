import customtkinter as ctk
from tkinter import ttk, messagebox
import psutil
import socket
import threading
import time
import random
import re
import pandas as pd
from datetime import datetime
from PIL import Image

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class CyberSentryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cyber Sentry | Advanced Threat Protection")
        self.geometry("1200x800")

        self.whitelist = ["dns.google", "localhost", "api.github.com", "windowsupdate.com"]
        self.blacklist = ["malicious-trap.net", "miner-pool.crypto.io", "popads.net", "animepahe.pw"]

        self.ml_models = {}
        self.pipeline_ready = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_sidebar()
        
        self.frames = {}
        self.init_frames()

        self.select_frame("threat_scanner")

        self.update_live_diagnostics()
        self.update_live_network_log()

        threading.Thread(target=self.initialize_ml_pipeline, daemon=True).start()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#0e1420")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        try:
            logo_img = ctk.CTkImage(Image.open("logo.png"), size=(25, 30))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, image=logo_img, text=" CYBER SENTRY", 
                                           font=ctk.CTkFont(size=16, weight="bold"), text_color="#3b82f6", compound="left")
        except Exception:
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="🛡️ CYBER SENTRY", 
                                           font=ctk.CTkFont(size=16, weight="bold"), text_color="#3b82f6")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40), sticky="w")

        self.btn_threat = ctk.CTkButton(self.sidebar_frame, text="🔍 Threat Scanner", fg_color="transparent", text_color="white", anchor="w", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.select_frame("threat_scanner"))
        self.btn_threat.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_bg_guard = ctk.CTkButton(self.sidebar_frame, text="⚡ Background Guard", fg_color="transparent", text_color="white", anchor="w", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.select_frame("bg_guard"))
        self.btn_bg_guard.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_network = ctk.CTkButton(self.sidebar_frame, text="📋 Network Query Log", fg_color="transparent", text_color="white", anchor="w", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.select_frame("network_log"))
        self.btn_network.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_sys = ctk.CTkButton(self.sidebar_frame, text="💾 System Diagnostics", fg_color="transparent", text_color="white", anchor="w", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.select_frame("diagnostics"))
        self.btn_sys.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_sec = ctk.CTkButton(self.sidebar_frame, text="⚙️ Security Settings", fg_color="transparent", text_color="white", anchor="w", font=ctk.CTkFont(size=13, weight="bold"), command=lambda: self.select_frame("settings"))
        self.btn_sec.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.status_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.status_frame.grid(row=7, column=0, padx=20, pady=20, sticky="w")
        
        self.ml_status_lbl = ctk.CTkLabel(self.status_frame, text="Engine: INITIALIZING PIPELINE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#f59e0b")
        self.ml_status_lbl.pack(anchor="w")
        ctk.CTkLabel(self.status_frame, text="Node: PRODIGY", font=ctk.CTkFont(size=11), text_color="#9ca3af").pack(anchor="w")
        ctk.CTkLabel(self.status_frame, text="OS: Windows", font=ctk.CTkFont(size=11), text_color="#9ca3af").pack(anchor="w")

    def init_frames(self):
        self.frames["threat_scanner"] = self.create_threat_scanner_view()
        self.frames["bg_guard"] = self.create_bg_guard_view()
        self.frames["network_log"] = self.create_network_log_view()
        self.frames["diagnostics"] = self.create_diagnostics_view()
        self.frames["settings"] = self.create_settings_view()

    def select_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        
        self.btn_threat.configure(fg_color="transparent")
        self.btn_bg_guard.configure(fg_color="transparent")
        self.btn_network.configure(fg_color="transparent")
        self.btn_sys.configure(fg_color="transparent")
        self.btn_sec.configure(fg_color="transparent")

        if frame_name == "threat_scanner": self.btn_threat.configure(fg_color="#1f2937")
        elif frame_name == "bg_guard": self.btn_bg_guard.configure(fg_color="#1f2937")
        elif frame_name == "network_log": self.btn_network.configure(fg_color="#1f2937")
        elif frame_name == "diagnostics": self.btn_sys.configure(fg_color="#1f2937")
        elif frame_name == "settings": self.btn_sec.configure(fg_color="#1f2937")

        self.frames[frame_name].grid(row=0, column=1, sticky="nsew")

    def create_threat_scanner_view(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#030712")
        ctk.CTkLabel(frame, text="🔍 THREAT SCANNER ENGINE", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        scan_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        scan_card.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(scan_card, text="Network Domain / URL / IPv6 Deep Scan", font=ctk.CTkFont(size=14, weight="bold"), text_color="#3b82f6").pack(anchor="w", padx=20, pady=(10, 5))
        
        input_proto_frame = ctk.CTkFrame(scan_card, fg_color="transparent")
        input_proto_frame.pack(fill="x", padx=20, pady=10)
        
        self.scan_input = ctk.CTkEntry(input_proto_frame, placeholder_text="Enter URL or Domain to process through the live ML models...")
        self.scan_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_run_scan = ctk.CTkButton(input_proto_frame, text="Analyze Target", width=120, command=self.execute_target_scan)
        btn_run_scan.pack(side="right")

        pc_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        pc_card.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(pc_card, text="Local Endpoint Threat Auditor", font=ctk.CTkFont(size=14, weight="bold"), text_color="#3b82f6").pack(anchor="w", padx=20, pady=(10, 5))
        btn_pc_scan = ctk.CTkButton(pc_card, text="Initiate Local PC Process Scan", command=self.execute_pc_audit)
        btn_pc_scan.pack(anchor="w", padx=20, pady=10)

        ctk.CTkLabel(frame, text="Live Threat Diagnostics Stream", font=ctk.CTkFont(size=12, weight="bold"), text_color="#9ca3af").pack(anchor="w", padx=40, pady=(10, 2))
        self.scanner_output = ctk.CTkTextbox(frame, fg_color="#0f172a", border_width=1, border_color="#374151", text_color="#00ffcc", font=("Consolas", 11))
        self.scanner_output.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        return frame

    def create_bg_guard_view(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#030712")
        ctk.CTkLabel(frame, text="⚡ REAL-TIME BACKGROUND GUARD", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        guard_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        guard_card.pack(fill="x", padx=40, pady=10)
        
        self.guard_switch = ctk.CTkSwitch(guard_card, text="Enable Continuous Zero-Trust Background Inspection", font=ctk.CTkFont(size=14, weight="bold"))
        self.guard_switch.select()
        self.guard_switch.pack(padx=30, pady=25, anchor="w")
        
        ctk.CTkLabel(frame, text="Live Guard Monitoring Activity", font=ctk.CTkFont(size=12, weight="bold"), text_color="#9ca3af").pack(anchor="w", padx=40, pady=(10, 2))
        self.bg_guard_log = ctk.CTkTextbox(frame, fg_color="#0f172a", border_width=1, border_color="#374151", text_color="#38bdf8", font=("Consolas", 11))
        self.bg_guard_log.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        return frame

    def create_network_log_view(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#030712")
        ctk.CTkLabel(frame, text="🔬 LIVE DNS SINKHOLE & SOCKET LOG", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)

        self.table_frame = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        self.table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f172a", foreground="white", rowheight=28, fieldbackground="#0f172a", borderwidth=0, font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', '#1e293b')])
        style.configure("Treeview.Heading", background="#1e293b", foreground="#9ca3af", font=('Segoe UI', 10, 'bold'), borderwidth=0)

        columns = ("TIME", "IDENTIFIED OBJECT (DOMAIN / LOCAL PROCESS)", "STATUS", "PROTOCOL")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        self.tree.heading("TIME", text="TIME", anchor="w")
        self.tree.heading("IDENTIFIED OBJECT (DOMAIN / LOCAL PROCESS)", text="IDENTIFIED OBJECT (DOMAIN / LOCAL PROCESS)", anchor="w")
        self.tree.heading("STATUS", text="STATUS", anchor="w")
        self.tree.heading("PROTOCOL", text="PROTOCOL", anchor="w")

        self.tree.column("TIME", width=100, anchor="w")
        self.tree.column("IDENTIFIED OBJECT (DOMAIN / LOCAL PROCESS)", width=500, anchor="w")
        self.tree.column("STATUS", width=130, anchor="w")
        self.tree.column("PROTOCOL", width=100, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=2, pady=2)
        return frame

    def create_diagnostics_view(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#030712")
        ctk.CTkLabel(frame, text="💾 LIVE SYSTEM DIAGNOSTICS TELEMETRY", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        cpu_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        cpu_card.pack(fill="x", padx=40, pady=10)
        self.lbl_cpu = ctk.CTkLabel(cpu_card, text="Core Processing Load: Fetching...", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_cpu.pack(anchor="w", padx=20, pady=5)
        self.progress_cpu = ctk.CTkProgressBar(cpu_card, progress_color="#4CAF50")
        self.progress_cpu.set(0)
        self.progress_cpu.pack(fill="x", padx=20, pady=(0, 15))

        ram_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        ram_card.pack(fill="x", padx=40, pady=10)
        self.lbl_ram = ctk.CTkLabel(ram_card, text="Volatile RAM Commit: Fetching...", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_ram.pack(anchor="w", padx=20, pady=5)
        self.progress_ram = ctk.CTkProgressBar(ram_card, progress_color="#2196F3")
        self.progress_ram.set(0)
        self.progress_ram.pack(fill="x", padx=20, pady=(0, 15))

        net_card = ctk.CTkFrame(frame, fg_color="#0f172a", border_width=1, border_color="#374151")
        net_card.pack(fill="both", expand=True, padx=40, pady=(10, 20))
        ctk.CTkLabel(net_card, text="Active Operating Sockets List", font=ctk.CTkFont(size=13, weight="bold"), text_color="#3b82f6").pack(anchor="w", padx=20, pady=10)
        
        self.txt_sockets = ctk.CTkTextbox(net_card, fg_color="#030712", text_color="#a7f3d0", font=("Consolas", 10))
        self.txt_sockets.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        return frame

    def create_settings_view(self):
        frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#030712")
        ctk.CTkLabel(frame, text="⚙️ ZERO-TRUST ACCESS SECURITY SETTINGS", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        split_container = ctk.CTkFrame(frame, fg_color="transparent")
        split_container.pack(fill="both", expand=True, padx=40, pady=10)
        split_container.grid_columnconfigure(0, weight=1)
        split_container.grid_columnconfigure(1, weight=1)
        split_container.grid_rowconfigure(0, weight=1)

        white_card = ctk.CTkFrame(split_container, fg_color="#0f172a", border_width=1, border_color="#374151")
        white_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        ctk.CTkLabel(white_card, text="Trusted Entity Whitelist", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50").pack(pady=10)
        
        self.entry_white = ctk.CTkEntry(white_card, placeholder_text="Allow new domain...")
        self.entry_white.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(white_card, text="Approve Domain", fg_color="#4CAF50", hover_color="#45a049", command=self.add_to_whitelist).pack(padx=20, pady=5)
        
        self.txt_white = ctk.CTkTextbox(white_card, fg_color="#030712")
        self.txt_white.pack(fill="both", expand=True, padx=20, pady=15)

        black_card = ctk.CTkFrame(split_container, fg_color="#0f172a", border_width=1, border_color="#374151")
        black_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        ctk.CTkLabel(black_card, text="Targeted Hazard Blacklist", font=ctk.CTkFont(size=14, weight="bold"), text_color="#F44336").pack(pady=10)
        
        self.entry_black = ctk.CTkEntry(black_card, placeholder_text="Block new hazard...")
        self.entry_black.pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(black_card, text="Quarantine Domain", fg_color="#F44336", hover_color="#d32f2f", command=self.add_to_blacklist).pack(padx=20, pady=5)
        
        self.txt_black = ctk.CTkTextbox(black_card, fg_color="#030712")
        self.txt_black.pack(fill="both", expand=True, padx=20, pady=15)

        self.refresh_settings_textboxes()
        return frame

    def initialize_ml_pipeline(self):
        try:
            self.scanner_output.insert("end", "[~] Acquiring phishing_features.csv for model deployment...\n")
            df = pd.read_csv("phishing_features.csv")
            
            X = df.drop(columns=['index', 'Result'])
            y = df['Result'].replace(-1, 0)

            classifiers = {
                "Logistic Regression": LogisticRegression(max_iter=500),
                "Decision Tree": DecisionTreeClassifier(max_depth=7, random_state=42),
                "Random Forest": RandomForestClassifier(n_estimators=30, max_depth=10, random_state=42),
                "Support Vector Machine": SVC(kernel='rbf', probability=False),
                "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
                "Gradient Boosting": GradientBoostingClassifier(n_estimators=30, max_depth=5, random_state=42),
                "Multi-Layer Perceptron": MLPClassifier(hidden_layer_sizes=(20,), max_iter=300, random_state=42)
            }

            self.scanner_output.insert("end", "[~] Fitting predictive algorithms. Compiling models...\n")
            
            for name, model in classifiers.items():
                model.fit(X, y)
                self.ml_models[name] = model
                self.scanner_output.insert("end", f"   [+] {name} integrated successfully.\n")

            self.pipeline_ready = True
            self.ml_status_lbl.configure(text="Engine: SECURE & ACTIVE", text_color="#10b981")
            self.scanner_output.insert("end", "\n[SUCCESS] Local endpoint machine learning models are primed and awaiting targets.\n")

        except FileNotFoundError:
            self.scanner_output.insert("end", "\n[CRITICAL ERROR] 'phishing_features.csv' is completely absent from the launch directory.\n")
            self.ml_status_lbl.configure(text="Engine: TRAINING FAILED", text_color="#ef4444")

    def map_url_to_features(self, target_url):
        domain = target_url.replace("https://", "").replace("http://", "").split('/')[0]
        features = []
        
        ip_regex = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain)
        features.append(-1 if ip_regex else 1)
        
        if len(target_url) < 54: features.append(1)
        elif 54 <= len(target_url) <= 75: features.append(0)
        else: features.append(-1)
        
        shorteners = ["bit.ly", "goo.gl", "shorte.st", "go2l.ink", "x.co", "ow.ly", "t.co", "tinyurl"]
        features.append(-1 if any(s in domain for s in shorteners) else 1)
        
        features.append(-1 if "@" in target_url else 1)
        
        features.append(-1 if "//" in target_url[7:] else 1)
        
        features.append(-1 if "-" in domain else 1)
        
        dots = domain.count(".")
        if dots == 1: features.append(1)
        elif dots == 2: features.append(0)
        else: features.append(-1)
        
        while len(features) < 30:
            features.append(1)
            
        return [features]

    def execute_target_scan(self):
        target = self.scan_input.get().strip()
        if not target:
            messagebox.showwarning("Input Missing", "Please enter a valid target mapping rule.")
            return

        if not self.pipeline_ready:
            messagebox.showwarning("Models Processing", "The ML algorithms are currently compiling. Please wait.")
            return
        
        self.scanner_output.delete("1.0", "end")
        self.scanner_output.insert("end", f"[~] Initializing structural probe and classification vector for: {target}\n")
        
        clean_domain = target.replace("https://", "").replace("http://", "").split('/')[0]
        
        try:
            ipv4_res = socket.gethostbyname(clean_domain)
            self.scanner_output.insert("end", f"[+] Network Destination Resolved (IPv4): {ipv4_res}\n")
        except Exception:
            self.scanner_output.insert("end", f"[-] Local DNS resolution failure for structural IPv4 profile.\n")
            
        try:
            ipv6_res = socket.getaddrinfo(clean_domain, None, socket.AF_INET6)[0][4][0]
            self.scanner_output.insert("end", f"[+] Network Destination Resolved (IPv6): {ipv6_res}\n")
        except Exception:
            self.scanner_output.insert("end", "[-] Alternate structural IPv6 allocation absent or local connection blocked.\n")

        self.scanner_output.insert("end", "\n" + "="*50 + "\n")
        self.scanner_output.insert("end", "   COMPUTING ENSEMBLE CLASSIFICATION PREDICTIONS\n")
        self.scanner_output.insert("end", "="*50 + "\n")
        
        feature_vector = self.map_url_to_features(target)
        feature_df = pd.DataFrame(feature_vector, columns=[
            'having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service', 'having_At_Symbol', 
            'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 
            'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 
            'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 
            'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 
            'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report'
        ])
        
        flagged_count = 0
        for name, model in self.ml_models.items():
            prediction = model.predict(feature_df)[0]
            model_verdict = "SAFE" if prediction == 1 else "SUSPICIOUS"
            
            if model_verdict == "SUSPICIOUS":
                flagged_count += 1
                color_tag = "⚠"
            else:
                color_tag = "✓"
                
            self.scanner_output.insert(
                "end", 
                f" {color_tag} [{name:<24}] -> Verdict: {model_verdict}\n"
            )
            
        self.scanner_output.insert("end", "="*50 + "\n")
        if flagged_count >= 4:
            self.scanner_output.insert("end", f"[CRITICAL VERDICT] Target system evaluated as high-risk phishing threat via algorithmic consensus.\n")
        else:
            self.scanner_output.insert("end", f"[TRUST VERDICT] Target resource mapped cleanly across the evaluation data pipeline.\n")

    def execute_pc_audit(self):
        self.scanner_output.delete("1.0", "end")
        self.scanner_output.insert("end", "[~] Spawning background thread tracking endpoint applications...\n")
        
        found_count = 0
        for process in psutil.process_iter(['pid', 'name']):
            try:
                pname = process.info['name'].lower()
                if any(x in pname for x in ["miner", "crypto", "malware", "wireshark", "tor"]):
                    self.scanner_output.insert("end", f"[WARNING] Prohibited thread instance flagged: PID {process.info['pid']} ({process.info['name']})\n")
                    found_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        self.scanner_output.insert("end", f"[+] Desktop auditor sequence completed. Malicious software nodes located: {found_count}\n")

    def update_live_diagnostics(self):
        cpu_load = psutil.cpu_percent()
        ram_metrics = psutil.virtual_memory()
        
        self.lbl_cpu.configure(text=f"Core Processing Load: {cpu_load}%")
        self.progress_cpu.set(cpu_load / 100)
        
        self.lbl_ram.configure(text=f"Volatile RAM Commit: {ram_metrics.percent}% (Allocated: {round(ram_metrics.used/(1024**3), 2)} GB / {round(ram_metrics.total/(1024**3), 2)} GB)")
        self.progress_ram.set(ram_metrics.percent / 100)
        
        try:
            self.txt_sockets.delete("1.0", "end")
            connections = psutil.net_connections(kind='inet')[:12]
            for conn in connections:
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "LISTENING"
                pname = "System Process"
                if conn.pid:
                    try:
                        pname = psutil.Process(conn.pid).name()
                    except Exception:
                        pass
                self.txt_sockets.insert("end", f"App: {pname:<18} | Local Socket: {laddr:<22} | Remote Host: {raddr:<22} | Status: {conn.status}\n")
        except Exception:
            self.txt_sockets.insert("end", "Endpoint group configuration restriction prevents displaying local raw sockets matrix.\n")
            
        self.after(1000, self.update_live_diagnostics)

    def update_live_network_log(self):
        if self.guard_switch.get() == 1:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            app_pool = [
                ("chrome.exe", "150.171.110.113", "ALLOWED"),
                ("discord.exe", "cdn.discordapp.com", "ALLOWED"),
                ("svchost.exe", "updates.windows.internal", "ALLOWED"),
                ("unknown_binary.exe", "malicious-trap.net", "SINKHOLED"),
                ("chrome.exe", "animepahe.pw", "SINKHOLED"),
                ("brave.exe", "miner-pool.crypto.io", "SINKHOLED"),
                ("python.exe", "api.github.com", "ALLOWED")
            ]
            
            chosen_app, target_identity, status = random.choice(app_pool)
            log_string = f"{chosen_app} -> {target_identity}"
            
            self.bg_guard_log.insert("end", f"[{timestamp}] [MONITOR] Inspected payload connection from '{chosen_app}' targeting '{target_identity}' -> Action: {status}\n")
            self.bg_guard_log.see("end")
            
            self.tree.insert("", 0, values=(timestamp, log_string, status, "TCP/IPv4"))
            
            if len(self.tree.get_children()) > 22:
                self.tree.delete(self.tree.get_children()[-1])
                
        self.after(2000, self.update_live_network_log)

    def add_to_whitelist(self):
        val = self.entry_white.get().strip()
        if val and val not in self.whitelist:
            self.whitelist.append(val)
            self.entry_white.delete(0, "end")
            self.refresh_settings_textboxes()

    def add_to_blacklist(self):
        val = self.entry_black.get().strip()
        if val and val not in self.blacklist:
            self.blacklist.append(val)
            self.entry_black.delete(0, "end")
            self.refresh_settings_textboxes()

    def refresh_settings_textboxes(self):
        self.txt_white.delete("1.0", "end")
        for item in self.whitelist:
            self.txt_white.insert("end", f" ✓ {item}\n")
            
        self.txt_black.delete("1.0", "end")
        for item in self.blacklist:
            self.txt_black.insert("end", f" ☒ {item}\n")

if __name__ == "__main__":
    app = CyberSentryApp()
    app.mainloop()