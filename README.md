# Sistema de Gerenciamento de Logística

Um sistema completo de gerenciamento de rotas de entrega com otimização automática, gestão de frota e controle de entregadores.

## 🚀 Funcionalidades Principais

### **Gestão de Frota e Entregadores**
- **Cadastro de Entregadores**: Criação de contas individuais para motoristas
- **Gestão de Veículos**: Cadastro completo de veículos com informações detalhadas
- **Vinculação Veículo-Entregador**: Associação de veículos a motoristas específicos
- **Interface de Gerenciamento**: Painel administrativo para gestão completa da frota

### **Planejamento de Rotas Inteligente**
- **Seleção de Veículos**: Escolha exata de quais veículos participarão de cada rota
- **Otimização Automática**: Algoritmo K-Means para distribuição geográfica eficiente
- **Múltiplos Veículos**: Suporte a rotas com vários veículos simultaneamente
- **Visualização Avançada**: Mapa interativo com cores diferenciadas por veículo

### **Sistema de Permissões**
- **Administrador**: Acesso completo a todas as funcionalidades
- **Entregadores**: Visualização apenas das rotas onde são motoristas
- **Controle Granular**: Permissões baseadas na associação veículo-entregador

### **Interface Profissional**
- **Design Moderno**: Interface polida com estilos QSS profissionais
- **Drag & Drop**: Reordenação manual de entregas para rotas únicas
- **Exportação Google Maps**: Links diretos para navegação no celular
- **Histórico Completo**: Rastreamento de rotas concluídas

## 🗄️ Nova Estrutura de Banco de Dados

### **Tabelas Principais**

#### **rotas**
```sql
CREATE TABLE rotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pendente', 'em_andamento', 'concluida') DEFAULT 'pendente'
);
```

#### **rota_veiculos** (Nova Tabela de Ligação)
```sql
CREATE TABLE rota_veiculos (
    rota_id INT,
    veiculo_id INT,
    PRIMARY KEY (rota_id, veiculo_id),
    FOREIGN KEY (rota_id) REFERENCES rotas(id) ON DELETE CASCADE,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
);
```

#### **veiculos**
```sql
CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50),
    ano INT,
    capacidade_kg FLOAT,
    entregador_id INT,
    FOREIGN KEY (entregador_id) REFERENCES users(id) ON DELETE SET NULL
);
```

#### **entregas**
```sql
CREATE TABLE entregas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rota_id INT NOT NULL,
    endereco_id INT NOT NULL,
    ordem INT NOT NULL,
    status ENUM('pendente', 'em_andamento', 'entregue', 'cancelada') DEFAULT 'pendente',
    data_entrega DATETIME,
    observacoes TEXT,
    veiculo_id INT DEFAULT NULL,
    FOREIGN KEY (rota_id) REFERENCES rotas(id),
    FOREIGN KEY (endereco_id) REFERENCES enderecos(id),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE SET NULL
);
```

## 🔄 Migração de Dados

Para usuários com instalações existentes, execute o script de migração:

```bash
python migrate_database.py
```

Este script irá:
1. Verificar e remover colunas antigas (`entregador_id`, `numero_veiculos`)
2. Criar a nova tabela `rota_veiculos`
3. Migrar dados existentes quando possível
4. Adicionar a coluna `veiculo_id` na tabela `entregas`

## 🎯 Fluxo de Trabalho Atualizado

### **1. Gestão da Frota**
1. Acesse "Gerenciamento" (apenas admin)
2. Cadastre entregadores na aba "Entregadores"
3. Cadastre veículos na aba "Veículos"
4. Vincule veículos a entregadores

### **2. Criação de Rotas**
1. Clique em "Nova Rota"
2. Digite o nome da rota
3. **Selecione os veículos específicos** que participarão
4. Clique em "Criar Rota"

### **3. Adição de Entregas**
1. Clique em "Nova Entrega"
2. Selecione a rota (agora mostra os veículos associados)
3. Digite o endereço com autocompletar
4. Salve a entrega

### **4. Otimização e Visualização**
1. Clique em "Visualizar" na rota
2. O sistema automaticamente:
   - Agrupa endereços por veículo usando K-Means
   - Otimiza a rota de cada veículo
   - Salva as atribuições no banco de dados
   - Exibe no mapa com cores diferenciadas

## 🔧 Instalação

1. **Dependências**:
```bash
pip install PyQt5 PyQtWebEngine googlemaps folium scikit-learn numpy polyline requests
```

2. **Banco de Dados**:
   - Configure MySQL/MariaDB
   - Atualize as credenciais em `database.py`
   - Execute `python main.py` para criar as tabelas

3. **API Google Maps**:
   - Obtenha uma chave da Google Maps Directions API
   - Atualize `GOOGLE_API_KEY` em `windows/map_gui.py`

## 🎨 Melhorias Visuais

- **Paleta de Cores Profissional**: Azuis, verdes e tons neutros
- **Botões Modernos**: Estilo flat com hover effects
- **Tabelas Organizadas**: Headers fixos e alinhamento perfeito
- **Formulários Intuitivos**: Layout responsivo e validação visual

## 🚀 Próximas Funcionalidades

- [ ] Relatórios de performance por veículo
- [ ] Integração com GPS em tempo real
- [ ] Notificações push para entregadores
- [ ] Dashboard com métricas de entrega
- [ ] API REST para integração externa

---

**Desenvolvido com ❤️ para otimizar a logística de entregas** 