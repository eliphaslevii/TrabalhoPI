# Sistema de Gerenciamento de Entregas

Este é um sistema de gerenciamento de entregas desenvolvido em Python utilizando PyQt5 para a interface gráfica e Google Maps API para funcionalidades de geolocalização e rotas.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta no Google Cloud Platform
- Chave de API do Google Maps

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📦 Dependências Principais

- PyQt5
- PyQtWebEngine
- googlemaps
- polyline
- folium
- requests
- mysql-connector-python
- PyMySQL
- branca

## 🔑 Configuração da API do Google Maps

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Habilite as seguintes APIs:
   - Directions API
   - Places API
   - Geocoding API
4. Crie uma chave de API
5. Substitua a chave de API no arquivo `windows/map_gui.py`:
```python
GOOGLE_API_KEY = 'SUA_CHAVE_API_AQUI'
```

## 🏃‍♂️ Como Executar

1. Certifique-se de que todas as dependências estão instaladas
2. Execute o arquivo principal:
```bash
python main.py
```

## ⚠️ Solução de Problemas

### Erro ao carregar o mapa
- Verifique se sua chave de API do Google Maps está correta
- Confirme se todas as APIs necessárias estão habilitadas no Google Cloud Console
- Verifique sua conexão com a internet

### Erro ao instalar dependências
Se encontrar problemas ao instalar as dependências, tente:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro com PyQt5
Se encontrar problemas com o PyQt5, tente:
```bash
pip uninstall PyQt5 PyQt5-Qt5 PyQt5-sip
pip install PyQt5
```

### Erro com PyQtWebEngine
Se o PyQtWebEngine não instalar corretamente, tente:
```bash
pip install PyQtWebEngine
```

### Erro com MySQL
Se encontrar problemas com o MySQL, verifique:
- Se o servidor MySQL está rodando
- Se as credenciais no arquivo de configuração estão corretas
- Se o banco de dados foi criado corretamente

## 📁 Estrutura do Projeto

```
.
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências do projeto
├── windows/               # Diretório com as janelas da aplicação
│   ├── map_gui.py         # Interface do mapa
│   ├── new_delivery_form.py # Formulário de nova entrega
│   └── ...
└── database.py            # Configurações do banco de dados
```

## 🔧 Configuração do Banco de Dados

O sistema utiliza MySQL como banco de dados. Certifique-se de:
1. Ter o MySQL Server instalado e rodando
2. Criar um banco de dados para o projeto
3. Configurar as credenciais no arquivo de configuração

## 📝 Notas Importantes

- Mantenha sua chave de API do Google Maps segura e não a compartilhe
- A API do Google Maps tem limites de uso gratuitos. Consulte a documentação para mais detalhes
- Certifique-se de ter uma conexão estável com a internet para usar as funcionalidades de mapa
- Mantenha suas credenciais do banco de dados seguras

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📧 Suporte

Se você encontrar algum problema ou tiver alguma dúvida, por favor abra uma issue no repositório. 