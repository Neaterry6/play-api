#!/bin/bash

echo "🚀 Starting StreamMe setup..."

# Activate virtual environment (if using one)
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing required libraries..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo "🔑 Setting up environment variables..."
cat <<EOF > .env
SESSION_SECRET="hiItkwH1TAEtUpT2/DVHAExrZGQqj0cuRItb6AqAhFEIGOaBIwzb7wXvxi/Ms9VKLZIsOFoNxz7/F69k9PZz0g=="
DATABASE_URL="postgresql://neondb_owner:npg_gX98vslEYZNe@ep-tiny-rain-a50izhgg.us-east-2.aws.neon.tech/neondb?sslmode=require"
PGDATABASE="neondb"
PGHOST="ep-tiny-rain-a50izhgg.us-east-2.aws.neon.tech"
PGPORT="5432"
PGUSER="neondb_owner"
PGPASSWORD="npg_gX98vslEYZNe"
COOKIES_PATH="cookies.txt"
EOF

echo "✅ Environment variables set!"

# Run Flask application
echo "✅ Running Flask server..."
python app.p
