#!/usr/bin/env python3
"""
Script para criar usuários de teste com diferentes roles

Cria:
- 1 Administrador
- 1 Organizador
- 3 Jogadores
"""

from database import SessionLocal
from models import User, UserRole
import bcrypt


def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_test_users():
    db = SessionLocal()
    
    try:
        print("[INFO] Criando usuários de teste...\n")
        
        # Administrador
        admin = User(
            email="admin@pingchampions.com",
            password_hash=hash_password("admin123"),
            name="Administrador",
            role=UserRole.ADMIN,
            active=True
        )
        db.add(admin)
        db.flush()
        print(f"✅ Admin: {admin.email} (ID {admin.id})")
        
        # Organizador
        organizer = User(
            email="organizador@pingchampions.com",
            password_hash=hash_password("org123"),
            name="Organizador",
            role=UserRole.ORGANIZER,
            active=True
        )
        db.add(organizer)
        db.flush()
        print(f"✅ Organizador: {organizer.email} (ID {organizer.id})")
        
        # Jogadores
        players_data = [
            {"email": "jogador1@pingchampions.com", "password": "player1", "name": "Jogador 1"},
            {"email": "jogador2@pingchampions.com", "password": "player2", "name": "Jogador 2"},
            {"email": "jogador3@pingchampions.com", "password": "player3", "name": "Jogador 3"},
        ]
        
        for data in players_data:
            player = User(
                email=data["email"],
                password_hash=hash_password(data["password"]),
                name=data["name"],
                role=UserRole.PLAYER,
                active=True
            )
            db.add(player)
            db.flush()
            print(f"✅ Jogador: {player.email} (ID {player.id})")
        
        db.commit()
        
        print("\n" + "="*60)
        print("[SUCCESS] Usuários de teste criados com sucesso!")
        print("="*60)
        
        print("\n📋 CREDENCIAIS DE TESTE:\n")
        
        print("🔴 ADMINISTRADOR:")
        print("   Email: admin@pingchampions.com")
        print("   Senha: admin123\n")
        
        print("🟠 ORGANIZADOR:")
        print("   Email: organizador@pingchampions.com")
        print("   Senha: org123\n")
        
        print("🟢 JOGADORES:")
        for i, data in enumerate(players_data, 1):
            print(f"   {i}. Email: {data['email']}")
            print(f"      Senha: {data['password']}")
        
        print("\n" + "="*60)
        print("Como testar:")
        print("="*60)
        print("\n1️⃣  Registrar usuário (POST /users/register):")
        print("""
curl -X POST "http://127.0.0.1:8000/users/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "novo@email.com",
    "password": "senha123",
    "name": "Novo Usuário",
    "role": "player"
  }'
        """)
        
        print("\n2️⃣  Fazer login (POST /users/login):")
        print("""
curl -X POST "http://127.0.0.1:8000/users/login" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "admin@pingchampions.com",
    "password": "admin123"
  }'
        """)
        
        print("\n3️⃣  Listar usuários (GET /users):")
        print("""
curl "http://127.0.0.1:8000/users"
        """)
        
        print("\n4️⃣  Listar por role (GET /users/role/{role}):")
        print("""
curl "http://127.0.0.1:8000/users/role/admin"
curl "http://127.0.0.1:8000/users/role/organizer"
curl "http://127.0.0.1:8000/users/role/player"
        """)
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erro ao criar usuários: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()
