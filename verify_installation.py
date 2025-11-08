#!/usr/bin/env python3
"""
Installation Verification Script for Black Sultan OS
Run this script to verify that your installation is correct.
"""

import sys
import importlib.util


def check_module(module_name, package=None):
    """Check if a module can be imported."""
    try:
        if package:
            spec = importlib.util.find_spec(f"{package}.{module_name}")
        else:
            spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False


def verify_dependencies():
    """Verify that all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'flask_socketio',
        'flask_sqlalchemy',
        'requests',
        'numpy',
        'pandas'
    ]
    
    all_good = True
    for package in required_packages:
        if check_module(package):
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ {package} - NOT FOUND")
            all_good = False
    
    return all_good


def verify_structure():
    """Verify that the project structure is correct."""
    import os
    
    print("\n📁 Checking project structure...")
    
    required_dirs = [
        'src/config',
        'src/models',
        'src/routes',
        'src/services',
        'src/utils',
        'src/database',
        'src/static'
    ]
    
    all_good = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ - NOT FOUND")
            all_good = False
    
    return all_good


def verify_imports():
    """Verify that local modules can be imported."""
    print("\n🔧 Checking local modules...")
    
    sys.path.insert(0, 'src')
    
    modules = [
        ('config', 'Config'),
        ('services', 'GameState'),
        ('services', 'TradingBot'),
        ('services', 'PayPalIntegration'),
        ('services', 'GamificationEngine'),
        ('utils', 'get_market_data'),
        ('models', 'User'),
        ('models', 'db')
    ]
    
    all_good = True
    for module, item in modules:
        try:
            mod = __import__(module, fromlist=[item])
            if hasattr(mod, item):
                print(f"  ✅ {module}.{item}")
            else:
                print(f"  ❌ {module}.{item} - ATTRIBUTE NOT FOUND")
                all_good = False
        except ImportError as e:
            print(f"  ❌ {module}.{item} - IMPORT ERROR: {e}")
            all_good = False
    
    return all_good


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Black Sultan OS - Installation Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", verify_dependencies),
        ("Project Structure", verify_structure),
        ("Local Modules", verify_imports)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All checks passed! Installation is correct.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
