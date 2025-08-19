#!/usr/bin/env python3
"""
Archon Database Setup Script
This script will initialize the complete Archon database schema in Supabase
"""

import os
import sys
from pathlib import Path

def main():
    print("🔧 Archon Database Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please ensure your .env file contains SUPABASE_URL and SUPABASE_SERVICE_KEY")
        return False
    
    # Read the SQL setup file
    sql_file = Path("archon-source/migration/complete_setup.sql")
    if not sql_file.exists():
        print("❌ SQL setup file not found!")
        print("Please ensure you have cloned the archon-source repository")
        return False
    
    print("✅ Found setup files")
    print(f"📁 SQL file: {sql_file}")
    
    # Read the SQL content
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        print(f"📊 SQL file loaded: {len(sql_content)} characters")
    except Exception as e:
        print(f"❌ Error reading SQL file: {e}")
        return False
    
    print("\n📋 Next Steps:")
    print("1. Go to your Supabase Dashboard:")
    print("   https://supabase.com/dashboard/project/prwatqxfenugpxavpovs")
    print("2. Click on 'SQL Editor' in the left sidebar")
    print("3. Copy and paste the SQL content below:")
    print("4. Click 'Run' to execute the setup script")
    
    print("\n" + "=" * 50)
    print("📝 SQL Setup Script Content:")
    print("=" * 50)
    print(sql_content)
    print("=" * 50)
    
    print("\n🎯 After running this script, you should have:")
    print("✅ Tasks functionality in the knowledge base")
    print("✅ Projects management")
    print("✅ Document processing")
    print("✅ Code examples storage")
    print("✅ Settings configuration")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Setup instructions provided successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
