#!/bin/bash

echo "🔧 Configuration PostgreSQL..."

DB_NAME="sante"
DB_USER="admin"
DB_PASS="1234"

# Accès postgres
sudo -u postgres psql <<EOF

-- Supprimer si existe
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;

-- Créer utilisateur
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';

-- Créer base
CREATE DATABASE $DB_NAME OWNER $DB_USER;

-- Donner droits
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

EOF

echo "✅ Base et utilisateur créés"

# Modifier auth
echo "🔐 Configuration authentification..."

sudo sed -i "s/peer/md5/g" /etc/postgresql/*/main/pg_hba.conf

# Redémarrer
sudo service postgresql restart

echo "🚀 PostgreSQL prêt !"
echo "User: $DB_USER"
echo "Password: $DB_PASS"
echo "Database: $DB_NAME"
chmod: cannot access 'setup_postgres.sh': No such file or directory
bash: line 1: ./setup_postgres.sh: No such file or directory
