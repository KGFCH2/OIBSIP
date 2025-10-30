#!/usr/bin/env python3
"""
Random Password Generator - Command Line Version
A simple command-line tool to generate secure random passwords based on user preferences.
"""

import random
import string
import argparse
import sys

def generate_password(length=12, use_uppercase=True, use_lowercase=True,
                     use_digits=True, use_symbols=True, exclude_chars=""):
    """
    Generate a random password based on specified criteria.

    Args:
        length (int): Length of the password
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_digits (bool): Include digits
        use_symbols (bool): Include symbols
        exclude_chars (str): Characters to exclude from password

    Returns:
        str: Generated password
    """
    if length < 1:
        raise ValueError("Password length must be at least 1")

    # Build character set based on user preferences
    charset = ""
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_lowercase:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    # Remove excluded characters
    if exclude_chars:
        charset = ''.join(c for c in charset if c not in exclude_chars)

    if not charset:
        raise ValueError("No valid characters available for password generation")

    # Generate password
    password = ''.join(random.choice(charset) for _ in range(length))
    return password

def validate_password_strength(password):
    """
    Validate password against basic security rules.

    Args:
        password (str): Password to validate

    Returns:
        dict: Dictionary with validation results
    """
    result = {
        'length_ok': len(password) >= 8,
        'has_upper': any(c.isupper() for c in password),
        'has_lower': any(c.islower() for c in password),
        'has_digit': any(c.isdigit() for c in password),
        'has_symbol': any(c in string.punctuation for c in password)
    }

    result['is_strong'] = all(result.values())
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Generate a random password with customizable options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python password_generator_cli.py -l 16
  python password_generator_cli.py -l 12 --no-symbols --exclude "0O1lI"
  python password_generator_cli.py -l 20 -u -d -s --exclude " "
        """
    )

    parser.add_argument('-l', '--length', type=int, default=12,
                       help='Password length (default: 12)')
    parser.add_argument('-u', '--uppercase', action='store_true', default=True,
                       help='Include uppercase letters (default: True)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('-w', '--lowercase', action='store_true', default=True,
                       help='Include lowercase letters (default: True)')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='Exclude lowercase letters')
    parser.add_argument('-d', '--digits', action='store_true', default=True,
                       help='Include digits (default: True)')
    parser.add_argument('--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('-s', '--symbols', action='store_true', default=True,
                       help='Include symbols (default: True)')
    parser.add_argument('--no-symbols', action='store_true',
                       help='Exclude symbols')
    parser.add_argument('-e', '--exclude', type=str, default="",
                       help='Characters to exclude from password')
    parser.add_argument('-c', '--count', type=int, default=1,
                       help='Number of passwords to generate (default: 1)')
    parser.add_argument('-v', '--validate', action='store_true',
                       help='Validate password strength')

    args = parser.parse_args()

    # Handle mutually exclusive options
    if args.no_uppercase:
        args.uppercase = False
    if args.no_lowercase:
        args.lowercase = False
    if args.no_digits:
        args.digits = False
    if args.no_symbols:
        args.symbols = False

    try:
        for i in range(args.count):
            password = generate_password(
                length=args.length,
                use_uppercase=args.uppercase,
                use_lowercase=args.lowercase,
                use_digits=args.digits,
                use_symbols=args.symbols,
                exclude_chars=args.exclude
            )

            print(f"Generated Password {i+1}: {password}")

            if args.validate:
                strength = validate_password_strength(password)
                print(f"Password Strength: {'Strong' if strength['is_strong'] else 'Weak'}")
                if not strength['is_strong']:
                    issues = []
                    if not strength['length_ok']:
                        issues.append("too short (< 8 characters)")
                    if not strength['has_upper']:
                        issues.append("missing uppercase letters")
                    if not strength['has_lower']:
                        issues.append("missing lowercase letters")
                    if not strength['has_digit']:
                        issues.append("missing digits")
                    if not strength['has_symbol']:
                        issues.append("missing symbols")
                    print(f"Issues: {', '.join(issues)}")
                print()

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()