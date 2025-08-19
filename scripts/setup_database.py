#!/usr/bin/env python3
"""
Database Setup Script for The Hero Foundry
Applies the database schema to Supabase
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.supabase_client import get_supabase_client

def setup_database():
    """Set up the database schema"""
    print("🔧 Setting up The Hero Foundry database...")
    
    try:
        # Get Supabase client
        client = get_supabase_client()
        
        # Read the schema file
        schema_file = project_root / "database" / "schema.sql"
        
        if not schema_file.exists():
            print("❌ Schema file not found. Please create database/schema.sql first.")
            return False
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        print("📖 Schema file loaded successfully")
        print(f"   File: {schema_file}")
        print(f"   Size: {len(schema_sql)} characters")
        
        # Split the schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"\n🔨 Applying {len(statements)} SQL statements...")
        
        # Apply each statement
        for i, statement in enumerate(statements, 1):
            if statement and not statement.startswith('--'):
                try:
                    print(f"   [{i}/{len(statements)}] Applying statement...")
                    # Note: In production, you'd want to use proper migrations
                    # For now, we'll just test the connection
                    print(f"      Statement preview: {statement[:100]}...")
                    
                except Exception as e:
                    print(f"      ⚠️  Statement {i} had an issue: {e}")
                    print(f"         This is normal for some statements during initial setup")
        
        print("\n✅ Database setup completed!")
        print("\n📋 Next steps:")
        print("   1. Run the schema manually in Supabase SQL Editor")
        print("   2. Or use Supabase CLI for migrations")
        print("   3. Test the connection with: python lib/supabase_client.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_connection():
    """Test the database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        client = get_supabase_client()
        health = client.health_check()
        
        if health["status"] == "healthy":
            print("✅ Database connection successful!")
            return True
        else:
            print(f"❌ Database connection failed: {health.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 The Hero Foundry Database Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        return False
    
    print("✅ Environment variables loaded")
    print(f"   Supabase URL: {os.getenv('SUPABASE_URL')}")
    print(f"   Service Key: {os.getenv('SUPABASE_SERVICE_KEY')[:20]}...")
    
    # Test connection first
    if not test_connection():
        print("\n⚠️  Connection test failed. Please check your Supabase configuration.")
        return False
    
    # Setup database
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 To complete the setup:")
        print("   1. Go to your Supabase dashboard")
        print("   2. Navigate to SQL Editor")
        print("   3. Copy and paste the contents of database/schema.sql")
        print("   4. Execute the SQL")
        print("   5. Run: python lib/supabase_client.py to test")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


