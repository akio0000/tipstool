import json
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ================================
# 設定類の読み込み
# ================================


#フォント設定
font_settings = ( "Meiryo", 14 )

#検索対象のフォルダを読み出し、中のjsonファイルをすべて検索対象に
import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

DATA_DIR = Path(r"C:\Users\user\Documents\data")
HTML_DIR = Path(r"C:\Users\user\Documents\data_html")
HTML_DIR.mkdir(exist_ok=True)


def load_all_data():
    """全PCの JSON を読み込む"""
    if not DATA_DIR.exists():
        return []

    all_data = []
    for file_path in DATA_DIR.glob("*.json"):
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    entry["source_file"] = file_path.name
                all_data.extend(data)
        except Exception as e:
            print(f"{file_path.name} の読み込みエラー: {e}")

    return all_data


def save_results_as_html(results, filename="search_results.html"):
    """検索結果を HTML に保存して開く"""
    output_path = HTML_DIR / filename

    html_lines = [
        "<!DOCTYPE html>",
        "<html lang='ja'>",
        "<head>",
        "    <meta charset='UTF-8'>",
        "    <title>検索結果</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; padding: 20px; }",
        "        h2 { color: #2c3e50; }",
        "        .entry { border-bottom: 1px solid #ccc; margin-bottom: 20px; padding-bottom: 10px; }",
        "    </style>",
        "</head>",
        "<body>",
        "    <h1>検索結果</h1>"
    ]

    for entry in results:
        file_path = entry.get("file_path", "")
        file_name = os.path.basename(file_path)

        if file_path.startswith("http://") or file_path.startswith("https://"):
            file_link = f"<a href='{file_path}' target='_blank'>{file_path}</a>"
        else:
            file_link = f"<a href='file:///{file_path}'>{file_name}</a>"

        text = entry.get("text", "").replace("\n", "<br>")

        html_lines.append("<div class='entry'>")
        html_lines.append(f"<h2>{entry.get('title', '（タイトルなし）')}</h2>")
        html_lines.append(f"<p><strong>内容:</strong><br>{text}</p>")
        html_lines.append(f"<p><strong>ファイル:</strong> {file_link}</p>")
        html_lines.append(f"<p><strong>作成日:</strong> {entry.get('created_at', '')}</p>")
        html_lines.append(f"<p><strong>更新日:</strong> {entry.get('updated_at', '')}</p>")
        html_lines.append(f"<p><strong>元ファイル:</strong> {entry.get('source_file', '')}</p>")
        html_lines.append("</div>")

    html_lines.append("</body></html>")

    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    os.startfile(output_path)


def search_entries(keyword_list, mode="or"):
    """AND / OR 検索（タイトル＋内容）"""
    data = load_all_data()
    results = []

    for entry in data:
        title = entry.get("title", "").lower()
        text = entry.get("text", "").lower()

        matches = []
        for kw in keyword_list:
            kw = kw.lower()
            matches.append(kw in title or kw in text)

        if mode == "and" and all(matches):
            results.append(entry)
        elif mode == "or" and any(matches):
            results.append(entry)

    return results


def run_search():
    raw = keyword_entry.get().strip()
    if not raw:
        messagebox.showinfo("エラー", "検索ワードを入力してください。")
        return

    keywords = raw.split()  # スペース区切りで複数ワード
    mode = mode_var.get()

    results = search_entries(keywords, mode)

    result_box.delete(0, tk.END)
    if results:
        result_box.insert(tk.END, f"{len(results)} 件ヒットしました。ブラウザで開きます。")
        save_results_as_html(results)
    else:
        messagebox.showinfo("検索結果", "該当なし")


root = tk.Tk()
root.title("Tips検索ツール")
root.geometry("400x350")

font = ("Meiryo", 14)

tk.Label(root, text="検索ワード（スペース区切り）", font=font).pack(pady=10)
keyword_entry = tk.Entry(root, font=font)
keyword_entry.pack(pady=5)

mode_var = tk.StringVar(value="or")
tk.Radiobutton(root, text="OR検索", font=font, variable=mode_var, value="or").pack()
tk.Radiobutton(root, text="AND検索", font=font, variable=mode_var, value="and").pack()

tk.Button(root, text="検索", font=font, command=run_search).pack(pady=10)

result_box = tk.Listbox(root, width=50)
result_box.pack(pady=10)

root.mainloop()
