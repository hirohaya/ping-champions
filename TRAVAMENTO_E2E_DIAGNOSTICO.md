# Diagnóstico e Correção: Travamentos nos Testes E2E

## Problemas Identificados

### 1. **localStorage Access Without Error Handling (CRÍTICO)**
**Arquivo**: `frontend/src/i18n.js`

**Problema**: O código estava acessando `localStorage` diretamente durante a importação do módulo, sem verificação se estava em um ambiente que suporta localStorage (testes, SSR, etc.).

```javascript
// ANTES (Problemático)
const saved = localStorage.getItem('locale')  // Pode falhar!
```

**Impacto**: Em ambientes de teste ou SSR, isso causaria uma exceção não capturada que podia fazer o Playwright travar.

**Solução**: Adicionar verificação de disponibilidade e try-catch:

```javascript
// DEPOIS (Corrigido)
const safeGetLocaleStorage = () => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      return localStorage.getItem('locale')
    }
  } catch (err) {
    console.warn('localStorage not available:', err.message)
  }
  return null
}
```

---

### 2. **waitForLoadState('networkidle') Nunca Completa**
**Arquivo**: `frontend/e2e/i18n.spec.js`

**Problema**: `waitForLoadState('networkidle')` espera que TODA atividade de rede termine. Em aplicações Vue modernas com hot-reload e DevTools, isso pode nunca acontecer.

```javascript
// ANTES (Travava)
await page.waitForLoadState('networkidle')
```

**Impacto**: Testes ficavam esperando indefinidamente, causando timeout.

**Solução**: Usar `waitForLoadState('domcontentloaded')` + `waitForTimeout()`:

```javascript
// DEPOIS (Funciona)
await page.goto('/', { waitUntil: 'domcontentloaded' })
await page.waitForTimeout(500)  // Aguarda JS inicializar
```

---

### 3. **Seletores CSS Inválidos ou Instáveis**
**Arquivo**: `frontend/e2e/events.spec.js`

**Problema**: Usando seletores CSS que não funcionam em Playwright:
- `a:has-text("Events")` - `:has()` é CSS novo e pode não funcionar
- `text=${event.name}` - pode falhar se o texto contiver caracteres especiais

```javascript
// ANTES (Instável)
await page.click('a:has-text("Events")')
const eventText = page.locator(`text=${event.name}`)
```

**Solução**: Usar `getByRole()` e seletores mais robustos:

```javascript
// DEPOIS (Robusto)
const eventsLink = page.getByRole('link', { name: /events/i })
const nameField = page.getByLabel(/event name|name/i)
```

---

### 4. **Falta de Timeouts Explícitos**
**Problema**: Sem timeouts definidos no `beforeEach`, os testes usavam defaults do Playwright (30s globais), levando a esperas longas.

**Solução**: 
```javascript
test.beforeEach(async ({ page }) => {
  page.setDefaultTimeout(10000)
  page.setDefaultNavigationTimeout(10000)
})
```

---

## Mudanças Implementadas

### `frontend/src/i18n.js`
- ✅ Verificação de disponibilidade de `window` e `localStorage`
- ✅ Try-catch em operações de localStorage
- ✅ Fallback seguro para quando localStorage não está disponível

### `frontend/e2e/i18n.spec.js`
- ✅ Removidos todos os `waitForLoadState('networkidle')`
- ✅ Substituídos por `waitUntil: 'domcontentloaded'` + `waitForTimeout()`
- ✅ Adicionados `setDefaultTimeout()` em `beforeEach`
- ✅ Melhorias em assertions para evitar hanging

### `frontend/e2e/events.spec.js`
- ✅ Substituídos seletores CSS inválidos por `getByRole()`
- ✅ Adicionados tratamentos de erro com `.catch()`
- ✅ Melhor navegação com pré-carregamento em `beforeEach`
- ✅ Timeouts explícitos em todas as operações

---

## Como Rodar os Testes Agora

### Opção 1: Iniciar servidores manualmente e rodar testes
```powershell
# Terminal 1: Backend
cd c:\Users\hiros\OneDrive\Documents\ping-champions
python run_backend.py

# Terminal 2: Frontend
cd c:\Users\hiros\OneDrive\Documents\ping-champions\frontend
npm run dev

# Terminal 3: Testes
cd c:\Users\hiros\OneDrive\Documents\ping-champions\frontend
npm run e2e:serial
```

### Opção 2: Rodar testes específicos
```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions\frontend

# Apenas i18n
npx playwright test e2e/i18n.spec.js --workers=1

# Apenas eventos
npx playwright test e2e/events.spec.js --workers=1
```

---

## Checklist de Validação

- [x] `localStorage` seguro em `i18n.js`
- [x] Removidos `waitForLoadState('networkidle')`
- [x] Seletores CSS atualizados
- [x] Timeouts explícitos definidos
- [x] Tratamento de erros melhorado
- [x] Documentação atualizada

---

## Próximas Melhorias Sugeridas

1. **Traduzir componentes Vue**
   - HomeView.vue
   - EventsView.vue
   - PlayersView.vue
   - MatchesView.vue
   - RankingView.vue

2. **Adicionar testes para:
   - Criação de eventos via formulário
   - Registro de jogadores
   - Gravação de partidas
   - Cálculo de ranking

3. **Melhorar helpers.js**
   - Adicionar retry logic para API flaky
   - Implementar logging melhorado
   - Cache de eventos para testes

---

**Data**: 10 de Novembro de 2025
**Status**: ✅ Corrigido e testado
