<template>
  <div class="user-menu">
    <template v-if="isLoggedIn">
      <div class="user-info">
        <div class="user-avatar">
          {{ userInitial }}
        </div>
        <div class="user-details">
          <div class="user-name">{{ userInfo.name }}</div>
          <div class="user-role">{{ getRoleLabel(userInfo.role) }}</div>
        </div>
        <button @click="toggleDropdown" class="dropdown-toggle">
          ▼
        </button>
      </div>

      <div v-if="showDropdown" class="dropdown-menu">
        <router-link to="/profile" class="menu-item" @click="showDropdown = false">
          👤 Meu Perfil
        </router-link>
        <router-link
          v-if="isAdmin"
          to="/admin"
          class="menu-item"
          @click="showDropdown = false"
        >
          🔧 Painel Admin
        </router-link>
        <router-link
          v-if="isOrganizer"
          to="/organizer"
          class="menu-item"
          @click="showDropdown = false"
        >
          📋 Painel Organizador
        </router-link>
        <button @click="handleLogout" class="menu-item logout">
          🚪 Sair
        </button>
      </div>
    </template>

    <template v-else>
      <router-link to="/login" class="btn-auth btn-login">
        Entrar
      </router-link>
      <router-link to="/register" class="btn-auth btn-register">
        Registrar
      </router-link>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as authService from '@/services/auth'

const router = useRouter()
const showDropdown = ref(false)

// Força reatividade ao localStorage
const authToken = ref(authService.getAuthToken())
const userInfo = ref(authService.getUserInfo())

const isLoggedIn = computed(() => authToken.value !== null)
const currentUser = computed(() => userInfo.value)
const isAdmin = computed(() => userInfo.value?.role === 'admin')
const isOrganizer = computed(() => userInfo.value?.role === 'organizer')

const userInitial = computed(() => {
  if (!userInfo.value) return '?'
  return userInfo.value.name.charAt(0).toUpperCase()
})

function getRoleLabel(role) {
  const labels = {
    admin: '🔐 Administrador',
    organizer: '📋 Organizador',
    player: '🏓 Jogador'
  }
  return labels[role] || role
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

function handleLogout() {
  authService.logout()
  showDropdown.value = false
  // Redirecionar para login
  router.push('/login')
}

// Fechar dropdown ao clicar fora
function handleClickOutside(event) {
  const menu = document.querySelector('.user-menu')
  if (menu && !menu.contains(event.target)) {
    showDropdown.value = false
  }
}

let unsubscribe = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Sincronizar com localStorage na montagem
  authToken.value = authService.getAuthToken()
  userInfo.value = authService.getUserInfo()
  
  // Inscrever-se em mudanças de autenticação
  unsubscribe = authService.onAuthChange(() => {
    authToken.value = authService.getAuthToken()
    userInfo.value = authService.getUserInfo()
  })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // Desinscrever do serviço de autenticação
  if (unsubscribe) {
    unsubscribe()
  }
})
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
  position: relative;
}

/* Usuário autenticado */
.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  background: #f5f5f5;
  cursor: pointer;
  transition: background-color 0.2s;
}

.user-info:hover {
  background: #e8e8e8;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 16px;
}

.user-details {
  display: flex;
  flex-direction: column;
  min-width: 120px;
}

.user-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: #666;
}

.dropdown-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 12px;
  padding: 0;
  transition: color 0.2s;
}

.dropdown-toggle:hover {
  color: #333;
}

/* Menu dropdown */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  margin-top: 8px;
  z-index: 1000;
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item {
  display: block;
  width: 100%;
  padding: 12px 16px;
  text-align: left;
  color: #333;
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
  transition: background-color 0.2s;
  font-family: inherit;
  font-size: 14px;
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item.logout {
  color: #c33;
  border-top: 1px solid #e0e0e0;
  margin-top: 4px;
  padding-top: 8px;
}

.menu-item.logout:hover {
  background-color: #fef;
}

/* Botões de autenticação */
.btn-auth {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  font-family: inherit;
}

.btn-login {
  color: #667eea;
  background: transparent;
  border: 2px solid #667eea;
}

.btn-login:hover {
  background: #667eea;
  color: white;
}

.btn-register {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-register:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

@media (max-width: 600px) {
  .user-details {
    display: none;
  }

  .user-info {
    padding: 4px 8px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .dropdown-toggle {
    display: none;
  }

  .dropdown-menu {
    position: fixed;
    top: auto;
    bottom: 20px;
    left: 20px;
    right: 20px;
    min-width: unset;
  }
}
</style>
