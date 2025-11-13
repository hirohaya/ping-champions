# i18n English Translation Toggle Guide

## Overview

A feature flag foi implementada para desativar facilmente a tradução para inglês e forçar o aplicativo a usar apenas **Português Brasileiro (pt-BR)**.

## Como Usar

### Desativar Inglês (Padrão Atual)

O toggle está **DESATIVADO** por padrão:

```javascript
// frontend/src/i18n.js (linha 8)
const I18N_ENABLE_ENGLISH = false
```

**Comportamento quando `false`**:
- ✅ Aplicativo força português (pt-BR)
- ✅ Seletor de idioma fica escondido (não aparece no header)
- ✅ Nenhum armazenamento em localStorage de preferência de idioma
- ✅ Sem problemas de SecurityError com localStorage

### Ativar Inglês (Se Necessário)

Para reativar a tradução em inglês no futuro:

```javascript
// frontend/src/i18n.js (linha 8)
const I18N_ENABLE_ENGLISH = true
```

**Comportamento quando `true`**:
- ✅ Seletor de idioma aparece no header
- ✅ Detecta idioma do navegador automaticamente
- ✅ Persiste preferência em localStorage
- ⚠️ Pode ter problemas com localStorage em alguns ambientes

## Arquivos Modificados

### 1. `frontend/src/i18n.js`
- Adicionou feature flag `I18N_ENABLE_ENGLISH`
- `getLocale()` retorna `pt-BR` se flag é `false`
- `getAvailableLocales()` inclui en-US apenas se flag é `true`

### 2. `frontend/src/components/LanguageSwitcher.vue`
- Seletor de idioma fica hidden se apenas 1 idioma disponível
- Condição: `v-if="availableLocales.length > 1"`

## Benefícios

✅ **Sem problemas de localStorage**: Elimina SecurityError em navegadores restritos
✅ **Interface simplificada**: Sem confusão de múltiplos idiomas
✅ **Fácil reativar**: Basta mudar `false` para `true` em 1 linha
✅ **Zero impacto de performance**: Sem overhead de seletor desnecessário

## Próximos Passos

Se quiser reativar inglês no futuro:
1. Abra `frontend/src/i18n.js`
2. Mude linha 8 para: `const I18N_ENABLE_ENGLISH = true`
3. Frontend vai automaticamente mostrar seletor de idioma

## Status Atual

- **Estado**: ✅ Inglês DESATIVADO
- **Idioma Forçado**: Português (pt-BR)
- **Seletor de Idioma**: Escondido
- **localStorage**: Sem problemas
