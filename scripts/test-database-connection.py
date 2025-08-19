#!/usr/bin/env python3
"""
Database Connection Test Script for The Hero Foundry

This script tests the database connection and verifies that all required
tables and data are accessible. Run this after starting the database
containers to ensure everything is working correctly.
"""

import os
import sys
import asyncio
import asyncpg
import redis
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

async def test_postgres_connection():
    """Test PostgreSQL database connection and basic operations."""
    print("🔍 Testing PostgreSQL connection...")
    
    try:
        # Get database URL from environment
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
        
        # Test connection
        conn = await asyncpg.connect(database_url)
        print("✅ PostgreSQL connection successful")
        
        # Test basic query
        version = await conn.fetchval('SELECT version()')
        print(f"📊 PostgreSQL version: {version.split()[1]}")
        
        # Test if our tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        
        expected_tables = {'rulesets', 'characters', 'character_snapshots', 'homebrew_content', 'ai_chat_sessions'}
        found_tables = {row['table_name'] for row in tables}
        
        print(f"📋 Found tables: {', '.join(sorted(found_tables))}")
        
        if expected_tables.issubset(found_tables):
            print("✅ All expected tables found")
        else:
            missing = expected_tables - found_tables
            print(f"⚠️  Missing tables: {', '.join(missing)}")
        
        # Test data access
        ruleset_count = await conn.fetchval('SELECT COUNT(*) FROM rulesets')
        character_count = await conn.fetchval('SELECT COUNT(*) FROM characters')
        homebrew_count = await conn.fetchval('SELECT COUNT(*) FROM homebrew_content')
        
        print(f"📊 Rulesets: {ruleset_count}, Characters: {character_count}, Homebrew: {homebrew_count}")
        
        # Test specific data
        dnd5e_ruleset = await conn.fetchrow('SELECT * FROM rulesets WHERE id = $1', 'dnd5e')
        if dnd5e_ruleset:
            print(f"✅ D&D 5e ruleset found: {dnd5e_ruleset['name']} v{dnd5e_ruleset['version']}")
        else:
            print("⚠️  D&D 5e ruleset not found")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_redis_connection():
    """Test Redis connection and basic operations."""
    print("\n🔍 Testing Redis connection...")
    
    try:
        # Get Redis URL from environment
        redis_url = os.getenv('REDIS_URL')
        if not redis_url:
            print("❌ REDIS_URL not found in environment variables")
            return False
        
        # Parse Redis URL
        if redis_url.startswith('redis://'):
            redis_url = redis_url[8:]
        
        host, port_db = redis_url.split(':')
        if '/' in port_db:
            port, db = port_db.split('/')
        else:
            port, db = port_db, '0'
        
        # Test connection
        r = redis.Redis(host=host, port=int(port), db=int(db), decode_responses=True)
        
        # Test ping
        response = r.ping()
        if response:
            print("✅ Redis connection successful")
        else:
            print("❌ Redis ping failed")
            return False
        
        # Test basic operations
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        if value == 'test_value':
            print("✅ Redis read/write operations successful")
        else:
            print("❌ Redis read/write operations failed")
            return False
        
        # Clean up test data
        r.delete('test_key')
        
        # Get Redis info
        info = r.info()
        print(f"📊 Redis version: {info.get('redis_version', 'unknown')}")
        print(f"📊 Connected clients: {info.get('connected_clients', 'unknown')}")
        print(f"📊 Used memory: {info.get('used_memory_human', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False

def test_environment_variables():
    """Test that all required environment variables are set."""
    print("\n🔍 Testing environment variables...")
    
    required_vars = [
        'DATABASE_URL',
        'REDIS_URL',
        'ENVIRONMENT',
        'LOG_LEVEL'
    ]
    
    optional_vars = [
        'AI_PROVIDER_API_KEY',
        'JWT_SECRET_KEY',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        return False
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print(f"⚠️  Missing optional environment variables: {', '.join(missing_optional)}")
        print("   These are not required for basic functionality but may limit features")
    
    return True

def test_file_structure():
    """Test that required directories and files exist."""
    print("\n🔍 Testing file structure...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        'database',
        'scripts',
        'docs',
        'logs'
    ]
    
    required_files = [
        'requirements.txt',
        'docker-compose.dev.yml',
        'database/init/01-init-database.sql',
        'database/redis.conf'
    ]
    
    missing_dirs = []
    missing_files = []
    
    for dir_path in required_dirs:
        if not (project_root / dir_path).exists():
            missing_dirs.append(dir_path)
    
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_files.append(file_path)
    
    if missing_dirs:
        print(f"❌ Missing required directories: {', '.join(missing_dirs)}")
        return False
    else:
        print("✅ All required directories exist")
    
    if missing_files:
        print(f"⚠️  Missing required files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
    
    return True

async def main():
    """Run all tests and provide a summary."""
    print("🚀 The Hero Foundry - Development Environment Test")
    print("=" * 60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("File Structure", test_file_structure),
        ("PostgreSQL Connection", test_postgres_connection),
        ("Redis Connection", test_redis_connection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your development environment is ready.")
        print("\n🚀 Next steps:")
        print("   1. Start your development servers: npm run dev")
        print("   2. Open http://localhost:8000/docs for API documentation")
        print("   3. Open http://localhost:3000 for the frontend")
        print("   4. Open http://localhost:5050 for pgAdmin (admin@herofoundry.local / admin)")
        print("   5. Open http://localhost:8081 for Redis Commander (admin / admin)")
    else:
        print("⚠️  Some tests failed. Please check the errors above and fix them.")
        print("\n🔧 Common solutions:")
        print("   1. Ensure Docker containers are running: docker-compose -f docker-compose.dev.yml up -d")
        print("   2. Check your .env file configuration")
        print("   3. Verify database initialization script ran successfully")
        print("   4. Check container logs: docker-compose -f docker-compose.dev.yml logs")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)
