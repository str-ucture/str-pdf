# 🗂️ str-pdf

**str-pdf** is a simple tool that allows users to convert most PDFs to **PDF/A** — a standardized, archivable format designed for long-term preservation of electronic documents.

This app uses [Ghostscript](https://www.ghostscript.com/) under the **GNU AGPLv3 license** and is distributed in compliance with that license.

---

## 🔧 Features

- Convert PDF files to **PDF/A** format
- Works with most standard PDFs
- Designed with long-term document preservation

---

## 🛠️ How to Use the App

- Download `str-pdf.exe` and the `utils` folder
- Your local folder structure should look like this:

  ```
  <app-directory>/
  ├── str-pdf.exe
  ├── utils/
      ├── auth.bin
      ├── gsdll64.dll
      └── str.ico
  ```

---

## 🔑 Authentication Key Requirement

To use the app, you must have a valid authentication key that is stored locally.

### Step-by-step instructions:

1. Navigate to the `utils` folder in the project.
2. Check for a file named `auth.bin`:

   - **If it does not exist**, create a new file named `auth.bin` inside the `utils` folder.
   - **Paste the authentication key** found at this URL into the file:
     ```
     https://github.com/str-ucture/str-key/blob/main/key_25.txt
     ```
   - **Save** the file.

3. If `auth.bin` already exists, the app will automatically check whether the stored key matches from the **URL** above.

---

## ⚠️ Important Note on Key Availability

If the key at `https://github.com/str-ucture/str-key/blob/main/key_25.txt` becomes temporarily unavailable (e.g., due to removal, access issues, or downtime), the app may not function.

This is **intentional** and indicates that:

- An **update or change or maintenance** is in progress
- The admin has disabled the access temporarily

Please wait and try again later once the update is complete.

---

## 🛠️ About the Remote Check (Kill Switch)

The app includes a **remote authentication check** mechanism. This allows the app owner to disable functionality if the app is being misused or needs to be updated urgently.

This mechanism is:

- Fully visible and editable in the source code (`str-pdf.py` file)
- Compliant with open-source licensing (AGPLv3)
- Designed to protect users and maintain control over distribution integrity

Users who build the app from source may remove or modify this behavior as permitted by the AGPL license.

---

## 🖥️ Ghostscript Modifications and Binary Requirements

To ensure proper functionality of the app, there are two important modifications and requirements related to Ghostscript:

1. **Modified Python Library**  
   The Python library of Ghostscript has been slightly modified in the file `_gsprint.py` and is made available inside `utils/_gsprint.py`. Please replace the default file in your virtual environment:

   ```
   your_virtual_environment\Lib\site-packages\ghostscript\_gsprint.py
   ```

   with the file `utils/_gsprint.py` from this repository for the app to work properly.

2. **Ghostscript Binary (gsdll64.dll)**  
   The binary file required for Ghostscript to run properly is provided in the `utils/gsdll64.dll` file. It is important to note that this file was accessed from a ghostscript portable available at *https://portableapps.com/apps/utilities/ghostscript_portable* and it has **not** been modified but is necessary for the **str-pdf** app to work properly.

If this file is missing from your `utils` folder, please download it from this repository and place it in the `utils` folder.

### Ghostscript Already Installed?

- If Ghostscript (https://ghostscript.com/releases/gsdnld.html) is already installed on your system, the `_gsprint.py` file does **not** need to be replaced, and the `gsdll64.dll` file is **not** required inside the `utils` folder.
- However, replacing the `_gsprint.py` file and having the `gsdll64.dll` file inside the `utils` folder will **not affect the functionality** of the app and is safe to do.

---

## 📄 License

This project includes components licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. You are free to use, modify, and distribute it under the same license terms.

For more information, see the [LICENSE](./LICENSE) file.
