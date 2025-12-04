# 🔐 LockForge - Advanced Random Password Generator

A comprehensive Python-based password generator with both command-line and graphical user interfaces. Generate secure, customizable passwords with advanced security features and clipboard integration.

## 🚀 Features

### Command-Line Version (`password_generator_cli.py`)
- ✅ Custom password length (4-128 characters)
- ✅ Selective character types (uppercase, lowercase, digits, symbols)
- ✅ Character exclusion (remove specific characters)
- ✅ Password strength validation
- ✅ Batch password generation
- ✅ Cross-platform compatibility

### GUI Version (`password_generator_gui.py`)
- 🎨 Modern Tkinter-based interface
- 🔒 Advanced security rules enforcement
- 📋 One-click clipboard integration
- 📊 Real-time password strength indicator
- 📝 Password history tracking
- 🎛️ Intuitive controls for all options
- ⚡ Instant password generation

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Setup
1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd "Simple Password Generator/LockForge"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Command-Line Version

#### Basic Usage
```bash
python password_generator_cli.py
```
Generates a 12-character password with all character types.

#### Advanced Options
```bash
# Generate a 16-character password
python password_generator_cli.py -l 16

# Generate password without symbols, exclude confusing characters
python password_generator_cli.py -l 12 --no-symbols --exclude "0O1lI"

# Generate multiple passwords with validation
python password_generator_cli.py -c 5 -v

# Custom character set (only uppercase and digits)
python password_generator_cli.py -l 10 -u -d --no-lowercase --no-symbols
```

#### Command-Line Arguments
- `-l, --length`: Password length (default: 12)
- `-u, --uppercase`: Include uppercase letters (default: True)
- `--no-uppercase`: Exclude uppercase letters
- `-w, --lowercase`: Include lowercase letters (default: True)
- `--no-lowercase`: Exclude lowercase letters
- `-d, --digits`: Include digits (default: True)
- `--no-digits`: Exclude digits
- `-s, --symbols`: Include symbols (default: True)
- `--no-symbols`: Exclude symbols
- `-e, --exclude`: Characters to exclude (e.g., "0O1lI")
- `-c, --count`: Number of passwords to generate (default: 1)
- `-v, --validate`: Show password strength validation

### GUI Version

#### Launch
```bash
python password_generator_gui.py
```

#### Interface Guide
1. **Password Length**: Set desired length (4-128 characters)
2. **Character Types**: Select which character types to include
3. **Exclude Characters**: Enter characters to remove from generation
4. **Security Rules**: Enable strong password enforcement
5. **Generate**: Click to create password
6. **Copy**: Copy password to clipboard
7. **History**: View previously generated passwords

## 🔐 Security Features

### Strong Password Rules
When "Enforce Strong Password Rules" is enabled:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one symbol
- No repeated characters
- No sequential characters (e.g., "abc", "123")

### Password Strength Validation
- 🟢 **Strong**: Meets all security criteria
- 🟡 **Medium**: Good but could be improved
- 🔴 **Weak**: Needs more character types or length

## 🎯 Key Concepts Demonstrated

### Randomization
- Uses `random.choice()` for cryptographically secure random selection
- Ensures uniform distribution across character sets

### User Input Validation
- Validates password length constraints
- Ensures at least one character type is selected
- Handles invalid character exclusions

### Character Set Management
- Modular character set construction
- Dynamic exclusion of specified characters
- Support for custom character combinations

### GUI Design (Advanced)
- Clean, intuitive Tkinter interface
- Responsive layout with proper spacing
- Real-time feedback and validation

### Security Rules (Advanced)
- Enforced strong password criteria
- Strength scoring algorithm
- Sequential and repeated character detection

### Clipboard Integration (Advanced)
- One-click copying using `pyperclip`
- Cross-platform clipboard support
- Error handling for clipboard operations

### Customization (Advanced)
- Flexible character type selection
- Character exclusion system
- Batch generation capabilities

## 📁 Project Structure

```
LockForge/
├── password_generator_cli.py    # Command-line version
├── password_generator_gui.py    # GUI version
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
└── password_vault.db           # Password storage (future feature)
```

## 🧪 Testing

### CLI Testing
```bash
# Test basic functionality
python password_generator_cli.py -l 8 -v

# Test character exclusion
python password_generator_cli.py -l 10 --exclude "aA1!" -v

# Test batch generation
python password_generator_cli.py -c 3 -l 16
```

### GUI Testing
1. Launch the GUI application
2. Test different length settings
3. Toggle character type checkboxes
4. Test character exclusion
5. Enable/disable security rules
6. Verify clipboard functionality
7. Check password history

## 🔧 Dependencies

- **Python 3.6+**: Core language
- **pyperclip**: Clipboard operations (GUI version)
- **tkinter**: GUI framework (included with Python)

## 🚀 Future Enhancements

- Password vault functionality
- Export password history
- Password policy templates
- Advanced strength analysis
- Multi-language support
- Dark mode theme

## 📝 License

This project is part of the Oasis Infobyte Python Programming Internship.

## 👨‍💻 Author

**Babin Bid**
- GitHub: [KGFCH2](https://github.com/KGFCH2)
- LinkedIn: [Babin Bid](https://www.linkedin.com/in/babin-bid-853728293)
- Email: babinbid05@gmail.com

## 🙏 Acknowledgments

- Oasis Infobyte for the internship opportunity
- Python community for excellent libraries
- Security researchers for password best practices

---

**"Security through strong passwords, simplicity through great design"**