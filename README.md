# 🛠️ Synthetic to ViewBinding Migrator

Welcome to the **Synthetic to ViewBinding Migrator**! This tool helps you convert Kotlin Android Fragments from synthetic imports to ViewBinding. It automates the migration of old fragment code to modern, type-safe view binding in Android projects. 

[![Download Releases](https://img.shields.io/badge/Download%20Releases-Click%20Here-brightgreen)](https://github.com/gada17/synthetic-to-viewbinding-migrator/releases)

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Usage](#usage)
4. [Migration Process](#migration-process)
5. [Examples](#examples)
6. [Contributing](#contributing)
7. [License](#license)
8. [Support](#support)

## 📖 Introduction

As Android development evolves, it's essential to keep up with the latest practices. Synthetic imports were once a popular way to access views in fragments, but they have become outdated. ViewBinding offers a safer, more efficient way to handle UI components. This repository provides a straightforward solution to transition from synthetic imports to ViewBinding seamlessly.

## 🚀 Features

- **Automated Migration**: Converts synthetic imports to ViewBinding automatically.
- **Type Safety**: Ensures type-safe access to views, reducing runtime errors.
- **Easy Integration**: Works well with existing Android projects.
- **Support for Fragments**: Specifically designed for Kotlin Android Fragments.
- **Comprehensive Documentation**: Clear instructions for setup and usage.

## 🛠️ Getting Started

### Installation

To get started with the Synthetic to ViewBinding Migrator, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gada17/synthetic-to-viewbinding-migrator.git
   cd synthetic-to-viewbinding-migrator
   ```

2. **Download the Latest Release**:
   Visit the [Releases section](https://github.com/gada17/synthetic-to-viewbinding-migrator/releases) to download the latest version. Make sure to execute the file after downloading.

### Usage

After installation, you can start using the migrator. Here’s how:

1. **Open Your Project**: Navigate to your Android project directory.
2. **Run the Migrator**: Use the following command to start the migration process:
   ```bash
   ./migrator --input <path-to-your-fragment-file>
   ```

3. **Check the Output**: The migrator will generate a new file with ViewBinding code.

## 🔄 Migration Process

Migrating from synthetic imports to ViewBinding involves several steps:

1. **Identify Synthetic Imports**: The tool scans your fragment files for synthetic imports.
2. **Generate ViewBinding Code**: It generates the necessary ViewBinding code.
3. **Replace Old Code**: The tool replaces the old synthetic code with the new ViewBinding code.
4. **Output New Fragment File**: The migrator creates a new file or modifies the existing one based on your preferences.

## 🖼️ Examples

Here’s a simple example to illustrate the migration process.

### Before Migration

```kotlin
class MyFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_my, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        myTextView.text = "Hello, World!" // Synthetic import
    }
}
```

### After Migration

```kotlin
class MyFragment : Fragment() {
    private var _binding: FragmentMyBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentMyBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        binding.myTextView.text = "Hello, World!" // ViewBinding
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

## 🤝 Contributing

We welcome contributions to the Synthetic to ViewBinding Migrator! Here’s how you can help:

1. **Fork the Repository**: Create your own fork of the project.
2. **Create a Branch**: Make a new branch for your feature or fix.
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes**: Implement your changes and commit them.
4. **Push to Your Fork**: Push your changes back to your fork.
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request**: Submit a pull request to the main repository.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you have any questions or need support, please check the [Issues](https://github.com/gada17/synthetic-to-viewbinding-migrator/issues) section of the repository. You can also reach out via email or create an issue for any bugs or feature requests.

## 🔗 Additional Resources

- [Android Developer Documentation](https://developer.android.com)
- [Kotlin Documentation](https://kotlinlang.org/docs/home.html)
- [ViewBinding Guide](https://developer.android.com/topic/libraries/view-binding)

Thank you for using the **Synthetic to ViewBinding Migrator**! We hope this tool makes your transition to ViewBinding smooth and efficient. For the latest updates, visit the [Releases section](https://github.com/gada17/synthetic-to-viewbinding-migrator/releases).