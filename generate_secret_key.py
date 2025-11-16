#!/usr/bin/env python3
"""Generate a secure secret key for Flask app"""
import secrets

if __name__ == '__main__':
    secret_key = secrets.token_hex(32)
    print(f"\n🔑 Your SECRET_KEY:")
    print(f"{secret_key}\n")
    print("Copy this and add it as an environment variable in your hosting platform.\n")

