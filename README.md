# Spelling Correction System for Psychology

A specialized spell checking system designed for psychology-related text, featuring a graphical user interface and advanced error detection algorithms.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This spell checking system is specifically designed for psychology-related text, incorporating specialized dictionaries and advanced natural language processing techniques. The system provides both a command-line interface and a user-friendly GUI for spell checking and correction.

**Author:** CHEAH WENG HOE  
**TP Number:** TP055533  
**Date Created:** 24/12/2024  
**Date Modified:** 30/12/2024

## ✨ Features

### Core Functionality
- **Psychology-Specific Dictionary**: Specialized vocabulary for psychology terminology
- **Advanced Error Detection**: Uses N-gram models and context analysis
- **Multiple Correction Algorithms**: 
  - Damerau-Levenshtein distance
  - Double Metaphone phonetic matching
  - Context-based scoring
- **Real-time Spell Checking**: Instant feedback on misspelled words
- **Interactive GUI**: User-friendly interface with right-click suggestions

### GUI Features
- **Text Input Area**: Large text area for input
- **Dictionary Search**: Search through psychology dictionary
- **Correction Suggestions**: Right-click on words for suggestions
- **Add to Dictionary**: Add new words to the system
- **Clear/Revert Functions**: Easy text management

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "05. Spell Check System"
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv spell_check_env

# Activate virtual environment
# On Windows (PowerShell):
.\spell_check_env\Scripts\Activate.ps1
# On Windows (Command Prompt):
.\spell_check_env\Scripts\activate.bat
# On macOS/Linux:
source spell_check_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data (First Run)
```bash
python -c "import nltk; nltk.download('words'); nltk.download('wordnet')"
```

## �� Usage

### Running the Application

1. **Start the GUI Application**:
   ```bash
   python main.py
   ```

2. **Using the Interface**:
   - Enter text in the input area
   - Right-click on misspelled words for suggestions
   - Use the dictionary search to look up psychology terms
   - Add new words to the dictionary as needed

### Command Line Usage
```bash
# Run the main application
python main.py

# Run with specific configuration
python main.py --config config.json
```

## 📁 Project Structure
