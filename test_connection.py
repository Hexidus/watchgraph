import os
os.environ["DATABASE_URL"] = "postgresql://postgres:Intell1Sense2024@watchgraph-db.cfsm0a8qcbn.us-east-2.rds.amazonaws.com:5432/postgres"

from database import engine, init_db

# Test connection
try:
    connection = engine.connect()
    print("✅ Successfully connected to PostgreSQL on AWS!")
    connection.close()
    
    # Initialize tables
    print("Creating database tables...")
    init_db()
    print("✅ Database tables created successfully!")
    print("\n🎉 Your AWS PostgreSQL database is ready!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check your security group allows incoming connections")
    print("2. Verify the endpoint URL is correct")
    print("3. Confirm the password is correct")