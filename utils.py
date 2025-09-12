import requests
import json
import pandas as pd
import time
from typing import Optional, List, Dict, Any


def cab(titulo: str) -> None:
    """
    Exibe um cabeçalho formatado no console.
    Args:
        titulo (str): Texto do título a ser exibido.
    Returns:
        None
    """
    print("=" * 60)
    print(titulo)
    print("=" * 60)


def fetch_api_data(url: str) -> Optional[List[Dict[str, Any]]]:
    """
    Busca dados de uma API em formato JSON.
    Args:
        url (str): Endereço da API.
    Returns:
        Optional[List[Dict[str, Any]]]: Lista de registros em formato dicionário,
        ou None em caso de falha.
    """
    cab("1. BUSCA DE DADOS NA API")
    try:
        inicio: float = time.time()
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        dados: Any = resp.json()
        fim: float = time.time()

        if not isinstance(dados, list) or len(dados) == 0:
            print("Aviso: a API respondeu, mas não retornou uma lista válida.")
            return None

        print(f"{len(dados)} registros obtidos em {fim - inicio:.2f} segundos")
        return dados

    except requests.exceptions.Timeout:
        print("Erro: tempo limite excedido na requisição.")
    except requests.exceptions.ConnectionError:
        print("Erro: falha de conexão com a API.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP: {e}")
    except json.JSONDecodeError:
        print("Erro: resposta não é JSON válido.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    return None


def salvar_json(dados: List[Dict[str, Any]], nome_arquivo: str) -> None:
    """
    Salva dados em formato JSON.
    Args:
        dados (List[Dict[str, Any]]): Dados a serem salvos.
        nome_arquivo (str): Caminho/nome do arquivo de saída.
    Returns:
        None
    """
    cab("2. SALVAR DADOS BRUTOS EM JSON")
    try:
        inicio: float = time.time()
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        fim: float = time.time()
        print(f"Arquivo JSON salvo: {nome_arquivo} (em {fim - inicio:.2f}s)")
    except PermissionError:
        print("Erro: permissão negada para salvar o arquivo.")
    except OSError as e:
        print(f"Erro de sistema ao salvar o arquivo: {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar JSON: {e}")


def converter_para_csv(dados: List[Dict[str, Any]], nome_arquivo: str) -> Optional[pd.DataFrame]:
    """
    Converte lista de dicionários em CSV usando pandas.
    Args:
        dados (List[Dict[str, Any]]): Dados carregados da API.
        nome_arquivo (str): Nome do arquivo CSV de saída.
    Returns:
        Optional[pd.DataFrame]: DataFrame criado a partir dos dados,
        ou None em caso de falha.
    """
    cab("3. CONVERTER DADOS PARA CSV")
    try:
        inicio: float = time.time()
        df: pd.DataFrame = pd.DataFrame(dados)
        df.to_csv(nome_arquivo, index=False, encoding="utf-8")
        fim: float = time.time()
        print(f"Arquivo CSV salvo: {nome_arquivo} (em {fim - inicio:.2f}s)")
        return df
    except (ValueError, OSError) as e:
        print(f"Erro ao converter para CSV: {e}")
    except Exception as e:
        print(f"Erro inesperado ao salvar CSV: {e}")
    return None