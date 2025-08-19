# 🚀 Supabase Setup Guide for The Hero Foundry

This guide will help you set up Supabase for The Hero Foundry project.

## 📋 Prerequisites

- Python 3.11+
- Supabase project created
- Supabase service key

## 🔧 Installation

### 1. Install Dependencies

```bash
# Activate virtual environment
& "d:/The Hero Foundry/.venv/Scripts/Activate.ps1"

# Install Supabase packages
pip install supabase python-dotenv
```

### 2. Environment Configuration

Your `.env` file should contain:

```env
SUPABASE_URL=https://prwatqxfenugpxavpovs.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InByd2F0cXhmZW51Z3B4YXZwb3ZzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTU4MTg5MSwiZXhwIjoyMDcxMTU3ODkxfQ.ME9O5j8xDCwyMzTjAC5IFlmFg5ed8RlFZWZK7kZKW1U
SUPABASE_ANON_KEY=your-anon-key-here
```

## 🗄️ Database Setup

### Option 1: Manual Setup (Recommended for first time)

1. **Go to Supabase Dashboard**
   - Navigate to [https://supabase.com/dashboard](https://supabase.com/dashboard)
   - Select your project: `prwatqxfenugpxavpovs`

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query"

3. **Apply Schema**
   - Copy the contents of `database/schema.sql`
   - Paste into the SQL Editor
   - Click "Run" to execute

4. **Verify Tables**
   - Go to "Table Editor" in the left sidebar
   - You should see the following tables:
     - `users`
     - `heroes`
     - `hero_skills`
     - `hero_equipment`
     - `game_sessions`
     - `game_events`
     - `hero_progression`

### Option 2: Automated Setup

```bash
# Run the database setup script
python scripts/setup_database.py
```

## 🧪 Testing the Setup

### 1. Test Basic Connection

```bash
python supabase_config.py
```

Expected output:
```
✅ Supabase connection successful!
   URL: https://prwatqxfenugpxavpovs.supabase.co
   Service Key: eyJhbGciOiJIUzI1NiIs...
```

### 2. Test Full Client

```bash
python lib/supabase_client.py
```

Expected output:
```
✅ Database tables are ready
🎉 Supabase connection successful!
   URL: https://prwatqxfenugpxavpovs.supabase.co
   Database: connected
   Auth: available
   Storage: available
   Realtime: available
```

## 📚 Available Features

### Database Operations
- ✅ Hero CRUD operations
- ✅ User management
- ✅ Game session tracking
- ✅ Real-time subscriptions
- ✅ File storage (avatars)

### Security Features
- ✅ Row Level Security (RLS)
- ✅ User authentication
- ✅ Data isolation

## 🔐 Security Configuration

The schema includes Row Level Security (RLS) policies:

- Users can only access their own data
- Heroes are isolated by user
- Game sessions are user-specific
- All operations require authentication

## 🚨 Troubleshooting

### Common Issues

1. **"Could not find table" error**
   - Run the schema manually in Supabase SQL Editor
   - Check that all tables were created successfully

2. **Authentication errors**
   - Verify your service key is correct
   - Check that RLS policies are properly configured

3. **Connection timeouts**
   - Verify your Supabase project is active
   - Check network connectivity

### Getting Help

- Check Supabase logs in the dashboard
- Verify environment variables are loaded
- Test with the provided test scripts

## 📖 Next Steps

After successful setup:

1. **Test the API endpoints**
2. **Create your first hero**
3. **Set up real-time subscriptions**
4. **Configure storage buckets**

## 🔗 Useful Links

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)

---

**🎉 Congratulations!** Your Supabase backend is now ready for The Hero Foundry project.


