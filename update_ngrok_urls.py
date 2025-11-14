#!/usr/bin/env python3
"""
Script para atualizar as URLs do ngrok dinamicamente
quando a URL muda (ngrok reinicia)
"""

import requests
import re
import sys

def get_ngrok_url():
    """Obter URL pública do ngrok via API local"""
    try:
        response = requests.get('http://127.0.0.1:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
        
        print("❌ Nenhum tunnel HTTPS encontrado no ngrok")
        return None
    except Exception as e:
        print(f"❌ Erro ao conectar ao ngrok: {e}")
        print("   Verifique se ngrok está rodando: ngrok http 8000")
        return None

def update_env_file(url):
    """Atualizar .env.local com nova URL"""
    env_file = './frontend/.env.local'
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Atualizar ou adicionar VITE_API_BASE_URL
        if 'VITE_API_BASE_URL=' in content:
            content = re.sub(
                r'VITE_API_BASE_URL=.*',
                f'VITE_API_BASE_URL={url}',
                content
            )
        else:
            content += f'\nVITE_API_BASE_URL={url}\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Atualizado {env_file}")
        print(f"   VITE_API_BASE_URL={url}")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar {env_file}: {e}")
        return False

def update_main_py(url):
    """Atualizar main.py com nova URL do ngrok"""
    main_file = './backend/main.py'
    
    try:
        with open(main_file, 'r') as f:
            content = f.read()
        
        # Encontrar a URL do ngrok actual
        old_pattern = r'"https://[a-zA-Z0-9\-]*\.ngrok[a-zA-Z0-9\-]*\.dev"'
        
        # Se houver uma URL velha, substituir. Senão, adicionar
        if re.search(old_pattern, content):
            content = re.sub(
                old_pattern,
                f'"{url}"',
                content
            )
        else:
            # Adicionar após "http://localhost:5174"
            content = re.sub(
                r'("http://localhost:5174",)',
                f'\\1\n        "{url}",',
                content
            )
        
        with open(main_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Atualizado {main_file}")
        print(f"   allow_origins: {url}")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar {main_file}: {e}")
        return False

def main():
    print("🔄 Verificando URL do ngrok...")
    
    ngrok_url = get_ngrok_url()
    if not ngrok_url:
        sys.exit(1)
    
    print(f"\n✅ URL encontrada: {ngrok_url}")
    
    print("\n📝 Atualizando configurações...")
    
    success = True
    success &= update_env_file(ngrok_url)
    success &= update_main_py(ngrok_url)
    
    if success:
        print("\n✅ Configurações atualizadas com sucesso!")
        print("\n📋 Próximos passos:")
        print("   1. Reiniciar o backend: python run_backend.py")
        print("   2. Reiniciar o frontend: cd frontend; npm run dev")
        print(f"   3. Acessar via: {ngrok_url}:5173")
    else:
        print("\n❌ Houve erros ao atualizar as configurações")
        sys.exit(1)

if __name__ == '__main__':
    main()
