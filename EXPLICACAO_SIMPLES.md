# Explicação Simples: Simulação de Consumo de Ração com SimPy

## O Que Foi Feito?

Implementamos um sistema que **simula e monitora o consumo mensal de ração** em alimentadores automáticos usando a biblioteca SimPy. Os dados simulados aparecem em gráficos nos relatórios.

---

## 1️⃣ Como Funciona o SimPy (A Biblioteca de Simulação)

**O que é SimPy?** É uma biblioteca que simula eventos discretos ao longo do tempo.

**O que ela faz no nosso caso?**
- Para cada alimentador, simula 180 dias (6 meses × 30 dias)
- A cada dia, gera uma quantidade aleatória de ração consumida
- A quantidade segue uma distribuição normal (gaussiana) baseada no consumo diário esperado do alimentador
- Exemplo: se um alimentador consome 25 kg/dia, a simulação gera entre ~21 e ~29 kg/dia (com variação de ±15%)

**Resultado:** Dados realistas de consumo para cada mês

---

## 2️⃣ Fluxo de Dados (Como Tudo Se Conecta)

```
┌─────────────────────┐
│  SimPy Simulation   │  ← Simula 180 dias, gera kg/dia com aleatoriedade
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ MonthlyConsumption (Banco)  │  ← Armazena: feeder, ano, mês, kg_consumido
│  (tabela do banco de dados) │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────┐
│  reports_index (VIEW)   │  ← Recupera últimos 6 meses, processa dados
└──────────┬───────────────┘
           │
           ▼
┌────────────────────────────┐
│  reports/index.html        │  ← Exibe gráfico com toneladas de ração
│     (TEMPLATE/HTML)        │
└────────────────────────────┘
```

---

## 3️⃣ O Que Cada Componente Faz

### A) Comando SimPy: `simulate_consumption.py`

**Localização:** `inteligente/management/commands/simulate_consumption.py`

**Função:** Gera dados de consumo simulado

**Como funciona:**
```
1. Lê todos os alimentadores do banco
2. Para cada alimentador:
   - Simula 180 dias (6 × 30)
   - Cada dia: consumption = random(mean=feeder.daily_consumption, std=15%)
   - Agrupa por mês e calcula total
3. Salva em MonthlyConsumption no banco de dados
```

**Como rodar:**
```bash
python manage.py simulate_consumption
```


**Resultado esperado:** Mensagem como "Records created: 91, updated: 0"

---

### B) Modelo de Dados: `MonthlyConsumption`

**Localização:** `inteligente/models.py`

**Estrutura:**
```python
class MonthlyConsumption(models.Model):
    feeder         → (FK) referência ao alimentador
    year           → ano (ex: 2024)
    month          → mês (ex: 12)
    kg_consumed    → total em kg (ex: 750.50)
    
    # Garantia: cada (feeder, year, month) é único
    # Ordena por: -year, -month (mais recente primeiro)
```

**Por que existe:** Persiste os dados simulados para uso nos relatórios. Sem isso, perderíamos os dados toda vez que reiniciássemos a aplicação.

---

### C) Função de Relatórios: `reports_index()`

**Localização:** `inteligente/views.py`

**O que faz:**
1. **Verifica permissões do usuário:**
   - Se agricultor (farmer): mostra apenas seus alimentadores
   - Se admin: mostra todos os alimentadores

2. **Calcula últimos 6 meses:**
   - Começa de hoje e volta 6 meses
   - Cria lista de tuplas: [(2024, 11), (2024, 10), ... (2024, 6)]

3. **Busca dados no banco:**
   - Query: `SELECT SUM(kg_consumed) FROM MonthlyConsumption WHERE (year, month) IN lista GROUP BY year, month`
   - Resultado: dicionário com kg/mês

4. **Converte unidades:**
   - kg para toneladas: `kg ÷ 1000`
   - Exemplo: 750 kg = 0.75 t

5. **Calcula eficiência:**
   - Base: 85% (alimentador individual) ou 85-95% (sistema)
   - Redução: -3% por alerta ativo
   - Mínimo: 60%
   - Exemplo: 85% - (2 alertas × 3%) = 79%

6. **Prepara dados para template:**
   - `consumption_series`: lista com label (mês), kg, toneladas
   - `top_feeders`: lista com 5 top alimentadores, consumo, eficiência
   - `report_data`: métricas globais

---

### D) Template de Visualização: `reports/index.html`

**Localização:** `inteligente/templates/reports/index.html`

**O que exibe:**

**Seção 1 - Métricas (4 cards):**
- Eficiência de Alimentação: 85%
- Consumo Total (últimos 6 meses): 4.35 t
- Nível Médio de Ração: 45%
- Tempo de Atividade do Sistema: 99.5%

**Seção 2 - Gráfico de Consumo:**
- Eixo X: Jan, Fev, Mar, Abr, Mai, Jun (últimos 6 meses)
- Eixo Y: barras proporcionais ao consumo em toneladas
- Exemplo: barra de Jun = 0.85 t de ração

**Seção 3 - Top 5 Alimentadores:**
| Nome | Consumo (t) | Eficiência | Alertas |
|------|------------|-----------|---------|
| Alimentador A | 1.25 | 82% | 1 |
| Alimentador B | 0.95 | 85% | 0 |
| ... | ... | ... | ... |

---

## 4️⃣ Fluxo de Uso (Passo a Passo)

### Cenário: Admin quer ver consumo dos últimos 6 meses

**Passo 1:** Rodar simulação (uma vez)
```bash
python manage.py simulate_consumption
```
- Cria 91 registros no banco (1 por feeder × 6 meses)

**Passo 2:** Acessar página de relatórios
- URL: `/inteligente/reports/`
- Django chama função `reports_index(request)`

**Passo 3:** A função faz:
```python
# 1. Verifica se é admin
if user_profile.role == 'admin':
    feeders = Feeder.objects.all()  # Todos os alimentadores

# 2. Calcula últimos 6 meses
months = [(2024, 11), (2024, 10), ..., (2024, 6)]

# 3. Busca dados no banco
MonthlyConsumption.objects.filter(feeder__in=feeders)\
                          .filter(year__in=[y for y,m in months])\
                          .filter(month__in=[m for y,m in months])

# 4. Agrupa por mês e converte para toneladas
consumption_series = [
    {"label": "Nov", "kg": 750.50, "tonnes": 0.75},
    {"label": "Out", "kg": 820.30, "tonnes": 0.82},
    ...
]

# 5. Envia para template
return render(request, "reports/index.html", context)
```

**Passo 4:** Template renderiza HTML
```html
<!-- Gráfico -->
{% for month in consumption_series %}
  <div class="bar" style="height: {{ month.kg|div:max_kg|mul:100 }}%">
    {{ month.label }}: {{ month.tonnes }}t
  </div>
{% endfor %}
```

**Resultado final:** Usuário vê gráfico bonito com dados reais simulados!

---

## 5️⃣ Filtragem por Perfil de Usuário

### Admin vê:
- Todos os alimentadores
- Todos os alertas
- Consumo de todo o sistema
- Label: "todos os X alimentadores do sistema"

### Farmer vê:
- Apenas seus próprios alimentadores
- Apenas alertas dos seus alimentadores
- Consumo apenas dos seus alimentadores
- Label: "seus X alimentadores"
- Se não tem alimentadores: mensagem de erro

---

## 6️⃣ Conversão de Unidades

O backend converte tudo para toneladas:

```python
# No banco de dados: sempre em KG
kg_consumido = 750.50  # kg

# Na view: converter para toneladas
toneladas = round(kg_consumido / 1000, 2)  # 0.75 t

# No template: exibir toneladas
{{ item.tonnes }}t  # "0.75t"
```

**Por quê?** Ração em toneladas é mais fácil de ler do que 750 kg.

---

## 7️⃣ Eficiência do Alimentador (Como É Calculada)

```
Eficiência = Base - Penalidade
           = 85% - (número_de_alertas × 3%)
           = 85% - 6% (se 2 alertas)
           = 79%

Mínimo garantido: 60%
Máximo teórico: 85%
```

**Lógica:** Quanto mais alertas, menos eficiente está o sistema

---

## 8️⃣ Perguntas Comuns

### P: Onde estão armazenados os dados simulados?
**R:** Na tabela `inteligente_monthlyconsumption` do banco de dados.

### P: Se eu rodar `simulate_consumption` de novo, recria todos os dados?
**R:** Não, usa `update_or_create()`. Se o registro já existe, apenas atualiza. Se não existe, cria novo.

### P: O que acontece se um agricultor não tem alimentadores?
**R:** A página de relatórios mostra mensagem: "Você ainda não possui alimentadores cadastrados."

### P: Como adiciono 12 meses em vez de 6?
**R:** Altere em `inteligente/views.py`, na função `reports_index()`:
```python
# Antes
for i in range(5, -1, -1):  # 6 meses

# Depois
for i in range(11, -1, -1):  # 12 meses
```

### P: Como altero o consumo diário de um alimentador?
**R:** Edite o alimentador em `/feeders/edit/{id}/` e mude o campo "Consumo Diário (kg)"

### P: A simulação é 100% realista?
**R:** Não é perfeita, mas usa distribuição gaussiana (sino) com desvio de ±15%, o que é bem realista para variações diárias.

---

## 9️⃣ Arquivos Modificados (Resumo)

| Arquivo | Modificação |
|---------|-------------|
| `inteligente/models.py` | Adicionado modelo `MonthlyConsumption` |
| `inteligente/views.py` | Atualizada função `reports_index()` |
| `inteligente/management/commands/simulate_consumption.py` | Criado arquivo de simulação com SimPy |
| `inteligente/templates/reports/index.html` | Atualizado para exibir dados de consumo em toneladas |
| `requirements.txt` | Adicionado `simpy==4.0.1` |

---

## 🔟 Como Testar Tudo

1. **Criar dados simulados:**
   ```bash
   python manage.py simulate_consumption
   ```

2. **Acessar a página:**
   - Ir para `/inteligente/reports/`
   - Se logado como admin, ver todos os dados
   - Se logado como farmer, ver apenas seus dados

3. **Verificar dados no banco:**
   ```bash
   python manage.py shell
   >>> from inteligente.models import MonthlyConsumption
   >>> MonthlyConsumption.objects.count()  # Deve ser ~91 (1 feeder × 6 meses × 15 feeders)
   >>> MonthlyConsumption.objects.first()  # Ver um registro de exemplo
   ```

4. **Criar um novo alimentador e rodar simulação novamente:**
   - Admin cria novo feeder em `/feeders/add/`
   - Roda: `python manage.py simulate_consumption`
   - Novos dados aparecem automaticamente nos relatórios

---

## Resumão em Uma Frase

**SimPy gera dados realistas de consumo, armazena em MonthlyConsumption, a view reports_index() busca os últimos 6 meses e agrupa por perfil, e o template exibe em um gráfico bonito em toneladas.**
