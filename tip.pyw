import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import platform


# ================================
# データ保存処理
# ================================
PC_NAME = platform.node()
DATA_DIR = Path(r"C:\Users\user\Documents\data")
DATA_FILE = DATA_DIR / f"records_{PC_NAME}.json"

def load_data():
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================================
# GUI アプリ本体
# ================================
class App(tk.Tk):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = Path(file_path)

        self.title("TipsTools")
        self.geometry("700x520")

        font_size = 14
        self.default_font = ("Meiryo", font_size)
        self.label_font = ("Meiryo", font_size)
        self.button_font = ("Meiryo", font_size - 2)

        self.labels = {}
        self.entries = {}

        fields = ["タイトル", "記録内容"]
        self.columnconfigure(1, weight=1)

        for i, field in enumerate(fields):
            self.labels[field] = tk.Label(self, text=f"{field}:", font=self.label_font)
            self.labels[field].grid(row=i, column=0, padx=10, pady=8, sticky="w")

            if field == "記録内容":
                self.entries[field] = tk.Text(self, height=5, font=self.default_font)
                self.entries[field].grid(row=i, column=1, padx=10, pady=8, sticky="nsew")
                self.rowconfigure(i, weight=1)
            else:
                self.entries[field] = tk.Entry(self, font=self.default_font)
                self.entries[field].grid(row=i, column=1, padx=10, pady=8, sticky="we")

        # 保存ボタン（row=2 に配置）
        self.save_button = tk.Button(
            self, text="保存", command=self.save_record,
            width=15, height=2, font=self.button_font
        )
        self.save_button.grid(row=3, column=1, pady=20, sticky="e")

    def save_record(self):
        title = self.entries["タイトル"].get().strip()
        text = self.entries["記録内容"].get("1.0", tk.END).strip()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        entry = {
            "title": title,
            "text": text,
            "file_path": str(self.file_path),
            "created_at": timestamp,
            "updated_at": timestamp
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        messagebox.showinfo("成功", "Tipsを保存した！")
        self.destroy()

# ================================
# 起動処理
# ================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("起動エラー", "ファイルを指定して。\nファイルを右クリックして「送る」から使用してください。")
        sys.exit(1)

    target_file_path = Path(sys.argv[1])

    if not target_file_path.exists():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("起動エラー", f"ファイルがないぞ。\nパス: {target_file_path}")
        sys.exit(1)

    app = App(file_path=target_file_path)
    app.mainloop()
