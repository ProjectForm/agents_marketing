# Finlancer Marketing Agency

Este repositório contém o pipeline de produção de conteúdo para a Finlancer Marketing Agency, utilizando agentes de IA para gerar copy, roteiros, briefings visuais, imagens e vídeos, com upload automático para o Google Drive.

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

Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`, e preencha a seguinte variável:

-   `GEMINI_API_KEY`: Sua chave de API para o Google Gemini. Obtenha em [Google AI Studio](https://aistudio.google.com/app/apikey).

**Nota sobre o Google Drive:** O sistema utiliza o `gws` CLI e `rclone` pré-configurados no ambiente Manus para interagir com o Google Drive. Não é necessário configurar `GOOGLE_SERVICE_ACCOUNT_JSON` ou `GOOGLE_DRIVE_ROOT_FOLDER_ID` diretamente no `.env` para esta integração.

Exemplo de `.env`:

```
GEMINI_API_KEY=SUA_CHAVE_GEMINI
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

-   **Pular geração de vídeo UGC:**
    ```bash
    python main.py --no-video
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
│   ├── image_generator.py      # Agente para geração de imagens com Imagen 4
│   └── video_generator.py      # NOVO: Agente para geração de vídeos UGC com Veo 3
├── utils/                      # Utilitários e módulos auxiliares
│   ├── output_manager.py
│   ├── drive_manager.py        # Gerenciador de upload para Google Drive (usando gws CLI)
│   └── output_parser.py        # NOVO: Parser para extrair dados dos outputs dos agentes
├── config/                     # Configurações dos agentes e prompts
├── knowledge/                  # Base de conhecimento para os agentes
├── workflows/                  # Definições de workflows
├── output/                     # Pasta local temporária para outputs gerados
├── main.py                     # Orquestrador principal do pipeline
├── requirements.txt            # Dependências do projeto
├── .env.example                # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```
```
