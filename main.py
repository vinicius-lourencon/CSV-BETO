# ================================================================
# Projeto: Análise de Comentários da API JSONPlaceholder
# Disciplina: Ferramentas de Linguagem de Programação (3º semestre)
# Estilo: funções simples + cabeçalhos no console (padrão da aula)
# ================================================================

import requests      # Requisições HTTP (buscar dados da API)
import json          # Salvar/ler JSON
import time          # Medir tempo de execução
from typing import Optional, List, Dict

def cab(titulo: str) -> None:
    print("=" * 60)
    print(titulo)
    print("=" * 60)

def fetch_api_data(url: str) -> Optional[List[Dict]]:
    """
    1) Busca dados da API e retorna como lista de dicionários.
    - timeout evita travar
    - raise_for_status() levanta erro p/ códigos 4xx/5xx
    - tratamento de erros específico
    """
    cab("1. BUSCA DE DADOS NA API")
    try:
        inicio = time.time()
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        dados = resp.json()  # pode levantar json.JSONDecodeError
        fim = time.time()

        # Validações básicas
        if not isinstance(dados, list) or len(dados) == 0:
            print(" A API respondeu, mas não retornou uma lista com registros.")
            return None

        print(f" {len(dados)} registros obtidos em {fim - inicio:.2f} segundos")
        return dados

    except requests.exceptions.Timeout:
        print(" Erro: a requisição excedeu o tempo limite (timeout).")
    except requests.exceptions.ConnectionError:
        print(" Erro: falha de conexão (verifique internet/URL).")
    except requests.exceptions.HTTPError as e:
        print(f" Erro HTTP: {e}")
    except json.JSONDecodeError:
        print(" Erro: a resposta não estava em JSON válido.")
    except Exception as e:
        print(f" Erro inesperado: {e}")

    return None

def salvar_json(dados: List[Dict], nome_arquivo: str) -> None:
    """
    2) Salva os dados brutos em JSON com indentação e UTF-8.
    - mede tempo de escrita
    - trata permissões e caminho inválido
    """
    cab("2. SALVAR DADOS BRUTOS EM JSON")
    try:
        inicio = time.time()
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        fim = time.time()
        print(f" Arquivo JSON salvo: {nome_arquivo} (em {fim - inicio:.2f}s)")
    except PermissionError:
        print(" Permissão negada para salvar o arquivo nesse local.")
    except FileNotFoundError:
        print(" Caminho inválido para salvar o arquivo.")
    except OSError as e:
        print(f" Erro de sistema ao salvar o arquivo: {e}")
    except Exception as e:
        print(f" Erro inesperado ao salvar JSON: {e}")

def main() -> None:
    url = "https://jsonplaceholder.typicode.com/comments"

    dados = fetch_api_data(url)
    if dados is None:
        print(" Não foi possível continuar sem os dados da API.")
        return

    salvar_json(dados, "comentarios.json")
    print("\n Etapas 1 e 2 concluídas. Próximo passo: converter para CSV com pandas.")

if __name__ == "__main__":
    main()