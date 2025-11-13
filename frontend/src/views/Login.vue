<template>
  <div class="login-page">
    <div class="login-container">
      <h1>Ping Champions</h1>
      <h2>Entrar</h2>

      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Email -->
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="seu@email.com"
            required
            @keyup.enter="handleLogin"
          />
        </div>

        <!-- Senha -->
        <div class="form-group">
          <label for="password">Senha:</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Sua senha"
            required
            @keyup.enter="handleLogin"
          />
        </div>

        <!-- Mensagem de erro -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <!-- Botão de envio -->
        <button type="submit" :disabled="loading" class="btn-login">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <!-- Link para registrar -->
      <p class="register-link">
        Não tem uma conta?
        <router-link to="/register">Registre-se aqui</router-link>
      </p>

      <!-- Usuários de teste -->
      <div class="test-users">
        <p><strong>Usuários de Teste:</strong></p>
        <ul>
          <li>
            <strong>Admin:</strong>
            admin@pingchampions.com / admin123
          </li>
          <li>
            <strong>Organizador:</strong>
            organizador@pingchampions.com / org123
          </li>
          <li>
            <strong>Jogador:</strong>
            jogador1@pingchampions.com / player1
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import * as authService from '@/services/auth'

const router = useRouter()

const form = ref({
  email: '',
  password: ''
})

const error = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!form.value.email || !form.value.password) {
    error.value = 'Email e senha são obrigatórios'
    return
  }

  loading.value = true
  error.value = ''

  const result = await authService.login(form.value.email, form.value.password)

  if (result.success) {
    // Redirecionar para home/dashboard
    router.push('/')
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 10px;
  font-size: 32px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.form-group input {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
  font-family: inherit;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input::placeholder {
  color: #999;
}

.error-message {
  padding: 12px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 4px;
  color: #c33;
  font-size: 14px;
  text-align: center;
}

.btn-login {
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 20px;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.register-link a:hover {
  color: #764ba2;
}

.test-users {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  font-size: 13px;
  color: #666;
  background: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
}

.test-users p {
  margin: 0 0 10px 0;
  font-weight: 600;
}

.test-users ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.test-users li {
  margin: 8px 0;
  padding-left: 20px;
  position: relative;
}

.test-users li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #667eea;
}

.test-users strong {
  color: #333;
}
</style>
