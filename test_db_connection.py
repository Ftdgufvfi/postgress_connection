import asyncio
import asyncpg
from src.config import Config

async def test_connection():
    """Test the database connection"""
    try:
        # Extract connection details from DATABASE_URL
        url = Config.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        
        print("Attempting to connect to the database...")
        print(f"Connection URL: {url.replace('npg_FG8IDQhPSxd4', '*****')}")  # Hide password
        
        # Connect to the database
        conn = await asyncpg.connect(url)
        
        # Test query
        result = await conn.fetchval("SELECT version();")
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {result}")
        
        # Test basic queries
        result = await conn.fetchval("SELECT current_database();")
        print(f"Current database: {result}")
        
        result = await conn.fetchval("SELECT current_user;")
        print(f"Current user: {result}")
        
        # List tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print(f"Tables in database:")
        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  No tables found in the public schema")
        
        await conn.close()
        print("✅ Connection closed successfully!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())