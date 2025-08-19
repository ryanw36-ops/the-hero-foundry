#!/usr/bin/env python3
"""
Supabase Configuration for The Hero Foundry
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class SupabaseConfig:
    """Supabase configuration and client management"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.url or not self.service_key:
            raise ValueError("Missing required Supabase environment variables")
        
        # Create Supabase client
        self.client: Client = create_client(self.url, self.service_key)
    
    def test_connection(self):
        """Test the Supabase connection"""
        try:
            # Test basic connection by getting user info
            response = self.client.auth.get_user()
            print("✅ Supabase connection successful!")
            print(f"   URL: {self.url}")
            print(f"   Service Key: {self.service_key[:20]}...")
            return True
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
            return False
    
    def get_client(self) -> Client:
        """Get the Supabase client instance"""
        return self.client

def main():
    """Test Supabase configuration"""
    print("🔧 Testing Supabase Configuration...")
    
    try:
        config = SupabaseConfig()
        success = config.test_connection()
        
        if success:
            print("\n🎉 Supabase is properly configured!")
            print("\n📋 Available methods:")
            print("   - config.get_client() - Get Supabase client")
            print("   - config.test_connection() - Test connection")
        else:
            print("\n⚠️  Supabase configuration needs attention")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\n📋 Please check your .env file contains:")
        print("   SUPABASE_URL=https://prwatqxfenugpxavpovs.supabase.co")
        print("   SUPABASE_SERVICE_KEY=your-service-key-here")

if __name__ == "__main__":
    main()


