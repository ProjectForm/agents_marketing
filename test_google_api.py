#!/usr/bin/env python3
"""
Diagnóstico da integração Google AI (Imagen 2 + Veo 3).
Execute na pasta finlancer-marketing-agency/:
  python test_google_api.py
"""
import os
import sys
from pathlib import Path

# ── 0. Carrega .env ──────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 0 — Carregando .env")
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    loaded = load_dotenv(env_path)
    print(f"  .env encontrado: {env_path.exists()} | carregado: {loaded}")
except ImportError:
    print("  AVISO: python-dotenv não instalado. Usando variáveis de ambiente do sistema.")

key = os.environ.get("GOOGLE_AI_API_KEY", "")
if not key:
    print("  ERRO: GOOGLE_AI_API_KEY não encontrada no .env nem no ambiente.")
    sys.exit(1)

masked = key[:6] + "..." + key[-4:] if len(key) > 10 else "(vazia)"
print(f"  GOOGLE_AI_API_KEY detectada: {masked}")
print(f"  Comprimento da chave: {len(key)} caracteres")
print(f"  Formato esperado: começa com 'AI' (Google AI Studio) ou tem 39+ chars")

# ── 1. Importa google-genai ──────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 1 — Importando google-genai SDK")
try:
    import google.genai as genai
    print(f"  OK — google.genai importado. Versão: {genai.__version__}")
except ImportError as e:
    print(f"  ERRO: {e}")
    print("  Solução: pip install google-genai")
    sys.exit(1)
except AttributeError:
    import google.genai as genai
    print(f"  OK — google.genai importado (sem atributo __version__).")

# ── 2. Cria client ───────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2 — Criando Client com a API key")
try:
    client = genai.Client(api_key=key)
    print("  OK — Client criado com sucesso.")
except Exception as e:
    print(f"  ERRO ao criar client: {e}")
    sys.exit(1)

# ── 3. Lista modelos disponíveis ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3 — Listando modelos disponíveis na sua conta")
try:
    models = list(client.models.list())
    names = [m.name for m in models]
    print(f"  Total de modelos acessíveis: {len(names)}")

    imagen_models = [n for n in names if "imagen" in n.lower()]
    veo_models    = [n for n in names if "veo" in n.lower()]
    gemini_models = [n for n in names if "gemini" in n.lower()][:5]

    print(f"\n  Imagen (geração de imagem):")
    if imagen_models:
        for m in imagen_models:
            print(f"    ✓ {m}")
    else:
        print("    ✗ NENHUM — sua chave não tem acesso ao Imagen")

    print(f"\n  Veo (geração de vídeo):")
    if veo_models:
        for m in veo_models:
            print(f"    ✓ {m}")
    else:
        print("    ✗ NENHUM — sua chave não tem acesso ao Veo")

    print(f"\n  Gemini (LLM, para referência):")
    for m in gemini_models:
        print(f"    ✓ {m}")

except Exception as e:
    print(f"  ERRO ao listar modelos: {e}")
    print("  Isso geralmente indica chave inválida ou sem permissões.")

# ── 4. Testa Imagen 4 Fast com prompt mínimo ────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4 — Testando Imagen 4 Fast (gera 1 imagem)")
IMAGEN_MODEL = "imagen-4.0-fast-generate-001"
try:
    from google.genai import types as gtypes

    resp = client.models.generate_images(
        model=IMAGEN_MODEL,
        prompt="A simple green circle on a dark background, minimal, no text.",
        config=gtypes.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
        ),
    )
    imgs = resp.generated_images
    if imgs and imgs[0].image.image_bytes:
        size_kb = len(imgs[0].image.image_bytes) // 1024
        print(f"  OK — Imagen 4 funcionou! Imagem gerada: {size_kb} KB")
        out = Path(__file__).parent / "output" / "test-imagen4.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(imgs[0].image.image_bytes)
        print(f"  Salvo em: {out}")
    else:
        print("  AVISO: resposta vazia — nenhuma imagem retornada.")
except Exception as e:
    print(f"  ERRO no Imagen 4: {type(e).__name__}: {e}")

# ── 5. Verifica Veo 3 (não gera — só valida que o modelo existe) ─────────────
print("\n" + "=" * 60)
print("STEP 5 — Verificando acesso ao Veo 3 (sem gerar vídeo para economizar)")
VEO_MODEL = "veo-3.0-generate-001"
VEO_V2    = "veo-2.0-generate-001"
for model_id in [VEO_MODEL, VEO_V2]:
    try:
        model_info = client.models.get(model=model_id)
        print(f"  OK — {model_id} acessível: {model_info.display_name}")
    except TypeError:
        # SDK antiga — tenta sem keyword
        try:
            model_info = client.models.get(model_id)
            print(f"  OK — {model_id} acessível")
        except Exception as e2:
            print(f"  {model_id}: {e2}")
    except Exception as e:
        print(f"  {model_id}: {e}")

# ── 6. Diagnóstico final ─────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("DIAGNÓSTICO FINAL")
print("=" * 60)
print("""
Se STEP 3 mostrou modelos Imagen/Veo → sua chave está ok, mas pode haver outro erro.
Se STEP 3 não mostrou nenhum modelo Imagen/Veo → sua chave não tem acesso.

SOLUÇÕES COMUNS:
1. Chave do Google AI Studio (aistudio.google.com):
   - Acesse aistudio.google.com → Get API key → Criar chave nova
   - A chave deve começar com 'AIza...'

2. Imagen 2 requer billing ativo no projeto Google Cloud:
   - Acesse console.cloud.google.com → Faturamento → ativar

3. Veo 3 ainda é preview — acesso limitado:
   - Pode requerer aprovação manual: ai.google.dev/gemini-api/docs/video

4. Se usar Vertex AI (GCP) em vez de AI Studio:
   - A autenticação é diferente (service account JSON, não API key simples)
""")
