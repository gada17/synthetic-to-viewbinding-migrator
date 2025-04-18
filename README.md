# **Synthetic to ViewBinding Migrator**

Convert Kotlin Android Fragments and Adapters from synthetic imports to ViewBinding. Automate the migration of old fragment code to modern, type-safe view binding in Android projects.

---

## **Overview**

This is a Python script designed to **automatically convert Android Kotlin code** from **synthetic imports to ViewBinding** for older projects. The script uses **OpenAI's GPT-4 Turbo model** to assist with the conversion process, ensuring minimal changes to the existing code apart from the ViewBinding updates.

---

## **Features**

- Converts fragments using **synthetic imports** to use **ViewBinding** instead.
- Uses **GPT-4 Turbo** model with a **temperature of 0.3** to ensure **minimal changes** to the original code, apart from those required for ViewBinding.
- The script processes both **Kotlin files** and associated **layout XML files**, ensuring proper integration of ViewBinding.
- Works in an automated manner with **minimal configuration** required.

---

## **How to Use**

### 1. **Get Your OpenAI API Key**

To use this script, you need an **OpenAI API key**. You can get it from [here](https://platform.openai.com/account/api-keys).

### 2. **Install Dependencies**

Install the required Python packages by running:

```bash```
pip install openai

Technical Details:
Model Used: GPT-4 Turbo

Temperature: 0.3 (This ensures minimal creative modification and more accurate results)

### 3. **Run the Script**

- Open the script and follow the instructions in the console to input your **OpenAI API key** when prompted.
- The script will automatically **scan your project directory** for **Kotlin files** and **layout XML files**.
- It will generate **converted Kotlin files** with **ViewBinding integrated** and save them in the appropriate directories.

### 4. **Limitations & Notes**

- **Code Changes:** The script makes **minimal changes** to the existing code, focusing solely on converting **synthetic imports to ViewBinding**. It does **not alter** other parts of the code unless absolutely necessary.
  
- **Partial Conversion:** The script may **not fully convert all aspects** of the code, particularly if there are deeper issues with the synthetic imports. After running the script, **manual inspection** and **adjustments** might be required to ensure complete migration.

### **Contribute**
If you would like to contribute to this project, feel free to fork the repository and make improvements. Whether it's fixing bugs, adding new features, or refining the code, your contributions are welcome!

To contribute:

1. Fork the repository.

2. Make your changes.

3. Submit a pull request with a description of your changes.

### **License**
This project is open-source, licensed under the MIT License. Feel free to modify and distribute it according to the terms of the license.



