<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Ping Champions</h1>
      <h2>Criar Conta</h2>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Email -->
        <div class="form-group">
          <label for="email">Email:</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="seu@email.com"
            required
          />
        </div>

        <!-- Nome -->
        <div class="form-group">
          <label for="name">Nome Completo:</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            placeholder="Seu nome"
            required
          />
        </div>

        <!-- Senha -->
        <div class="form-group">
          <label for="password">Senha:</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Mínimo 6 caracteres"
            required
            minlength="6"
          />
        </div>

        <!-- Confirmação de Senha -->
        <div class="form-group">
          <label for="passwordConfirm">Confirmar Senha:</label>
          <input
            id="passwordConfirm"
            v-model="form.passwordConfirm"
            type="password"
            placeholder="Confirme a senha"
            required
            minlength="6"
          />
        </div>

        <!-- Tipo de Usuário -->
        <div class="form-group">
          <label for="role">Tipo de Usuário:</label>
          <select id="role" v-model="form.role" required>
            <option value="">Selecione...</option>
            <option value="player">Jogador</option>
            <option value="organizer">Organizador</option>
          </select>
        </div>

        <!-- Mensagem de erro -->
        <div v-if="error" class="error-message">
          ⚠️ {{ error }}
        </div>

        <!-- Mensagem de sucesso -->
        <div v-if="success" class="success-message">
          ✅ Conta criada com sucesso! Redirecionando...
        </div>

        <!-- Botão de envio -->
        <button type="submit" :disabled="loading" class="btn-register">
          {{ loading ? 'Criando conta...' : 'Registrar' }}
        </button>
      </form>

      <!-- Link para login -->
      <p class="login-link">
        Já tem uma conta?
        <router-link to="/login">Faça login aqui</router-link>
      </p>
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
  name: '',
  password: '',
  passwordConfirm: '',
  role: ''
})

const error = ref('')
const success = ref(false)
const loading = ref(false)

async function handleRegister() {
  // Validações
  if (!form.value.email || !form.value.name || !form.value.password || !form.value.role) {
    error.value = 'Todos os campos são obrigatórios'
    return
  }

  if (form.value.password.length < 6) {
    error.value = 'A senha deve ter no mínimo 6 caracteres'
    return
  }

  if (form.value.password !== form.value.passwordConfirm) {
    error.value = 'As senhas não conferem'
    return
  }

  loading.value = true
  error.value = ''
  success.value = false

  const result = await authService.register(
    form.value.email,
    form.value.password,
    form.value.name,
    form.value.role
  )

  if (result.success) {
    success.value = true
    // Aguardar 2 segundos e redirecionar para home
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } else {
    error.value = result.error
  }

  loading.value = false
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}

.register-container {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 450px;
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

.register-form {
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

.form-group input,
.form-group select {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
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

.success-message {
  padding: 12px;
  background-color: #efe;
  border: 1px solid #cfc;
  border-radius: 4px;
  color: #3c3;
  font-size: 14px;
  text-align: center;
}

.btn-register {
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

.btn-register:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn-register:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 20px;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.login-link a:hover {
  color: #764ba2;
}
</style>
