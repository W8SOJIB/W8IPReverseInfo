# 🔥 W8IP PRO MAX SCANNER

Advanced IP Intelligence & Deep Port Scanner Tool
Coded by **W8Team / MD SOJIB**

---

## 🚀 Features

* 🌐 Domain → IP + Full Info
* 📡 Reverse IP Scan (CIDR /24 /16 /8)
* 🧠 Hostname Detection
* 🖥 Server Detection (nginx / apache / etc)
* 📄 Website Title Grabber
* ⚡ Deep Scan (ALL PORTS 1–65535)
* 🔥 Real-Time Port Detection
* 🛑 CTRL + C Stop Support
* 📁 Auto Save Results (deep_scan.txt)
* 🎨 Clean & Colorful Output
* 📱 Termux Supported

---

## ⚙️ Installation (PC / Linux / Windows)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/w8ip-scanner.git
cd w8ip-scanner
```

### 2️⃣ Install Requirements

```bash
pip install requests colorama
```

### 3️⃣ Run Tool

```bash
python main.py
```

---

## 📱 Termux Installation (Android)

### Step 1: Update Packages

```bash
pkg update && pkg upgrade
```

### Step 2: Install Python & Git

```bash
pkg install python git
```

### Step 3: Clone Tool

```bash
git clone https://github.com/yourusername/w8ip-scanner.git
cd w8ip-scanner
```

### Step 4: Install Requirements

```bash
pip install requests colorama
```

### Step 5: Run

```bash
python main.py
```

---

## 🎯 Usage

After running the tool:

```
[1] Domain → IP + Info
[2] IP Range Scan (/24 + Server + Title)
[3] Deep Scan (ALL PORTS ⚡ + Server + Title + Save)
[4] Exit
```

### Example:

```
Enter CIDR ➤ 103.165.48.0/24
```

---

## 📁 Output File

Deep scan results are saved in:

```
deep_scan.txt
```

Example:

```
103.165.48.10 Hostname: example.com
103.165.48.10 Server: nginx
103.165.48.10 Title: welcome page
103.165.48.10:22
103.165.48.10:80
```

---

## ⚡ Performance Tips

| Device    | Recommended MAX_CONCURRENT |
| --------- | -------------------------- |
| Termux 📱 | 300–700                    |
| PC 💻     | 800–2000                   |
| VPS 🔥    | 3000+                      |

Edit in code:

```python
MAX_CONCURRENT = 800
```

---

## ⚠️ Disclaimer

This tool is for **educational & security testing purposes only**.
Do not use this tool on systems without proper authorization.

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to:

* Use
* Modify
* Distribute

But must include original credit:

**W8Team / MD SOJIB**

---

## 💻 Author

* 👑 MD SOJIB
* ⚡ W8Team

---

## ⭐ Support

If you like this tool, give it a ⭐ on GitHub!

---
