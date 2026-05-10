# Finlancer Marketing Agency

Este repositório contém o pipeline de produção de conteúdo para a Finlancer Marketing Agency, utilizando agentes de IA para gerar copy, roteiros, briefings visuais e imagens, com upload automático para o Google Drive.

## Setup

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ProjectForm/agents_marketing.git
    cd agents_marketing
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração das Credenciais Google

Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`, e preencha as seguintes variáveis:

-   `GEMINI_API_KEY`: Sua chave de API para o Google Gemini. Obtenha em [Google AI Studio](https://aistudio.google.com/app/apikey).
-   `GOOGLE_SERVICE_ACCOUNT_JSON`: O caminho para o arquivo JSON da sua chave de conta de serviço do Google Cloud, ou o conteúdo JSON diretamente. Esta chave é usada para autenticação com a Google Drive API. Certifique-se de que a conta de serviço tenha permissões de acesso ao Google Drive.
-   `GOOGLE_DRIVE_ROOT_FOLDER_ID`: O ID da pasta raiz no Google Drive onde os outputs serão salvos (ex: a pasta "Finlancer Marketing").

Exemplo de `.env`:

```
GEMINI_API_KEY=SUA_CHAVE_GEMINI
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/your/service_account.json
GOOGLE_DRIVE_ROOT_FOLDER_ID=SEU_ID_DA_PASTA_RAIZ_NO_DRIVE
```

## Uso

Execute o `main.py` com os seguintes argumentos:

-   **Produção normal (tema automático por data):**
    ```bash
    python main.py
    ```

-   **Tema específico:**
    ```bash
    python main.py --custom "separação PF e PJ para MEI iniciante"
    ```

-   **Data específica:**
    ```bash
    python main.py --date 2026-05-20
    ```

-   **Só texto, sem gerar imagens (modo rápido):**
    ```bash
    python main.py --no-images
    ```

-   **Só texto, sem upload para Drive:**
    ```bash
    python main.py --no-drive
    ```

-   **Pular fases de revisão (3 e 4):**
    ```bash
    python main.py --no-review
    ```

## Estrutura do Repositório

```
agents_marketing/
├── agents/                     # Definições dos agentes de IA
│   ├── base_agent.py
│   ├── brand_director.py
│   ├── content_strategist.py
│   ├── social_copy_specialist.py
│   ├── visual_content_creator.py
│   ├── video_script_specialist.py
│   └── image_generator.py      # NOVO: Agente para geração de imagens com Gemini Imagen
├── utils/                      # Utilitários e módulos auxiliares
│   ├── output_manager.py
│   └── drive_manager.py        # NOVO: Gerenciador de upload para Google Drive
├── config/                     # Configurações dos agentes e prompts
├── knowledge/                  # Base de conhecimento para os agentes
├── workflows/                  # Definições de workflows
├── output/                     # Pasta local temporária para outputs gerados
├── main.py                     # Orquestrador principal do pipeline
├── requirements.txt            # Dependências do projeto
├── .env.example                # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```
