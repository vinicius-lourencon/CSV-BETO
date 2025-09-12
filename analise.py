import pandas as pd
from typing import Dict, Any
from utils import cab


def analisar_dados(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Realiza análise estatística básica dos comentários.
    Args:
        df (pd.DataFrame): DataFrame com os dados dos comentários.
    Returns:
        Dict[str, Any]: Dicionário contendo métricas calculadas.
    """
    cab("4. ANÁLISE ESTATÍSTICA")
    try:
        total: int = len(df)
        media_palavras: float = df['body'].apply(lambda x: len(str(x).split())).mean()
        mediana_palavras: float = df['body'].apply(lambda x: len(str(x).split())).median()
        max_comentario: int = df['body'].apply(lambda x: len(str(x))).max()
        min_comentario: int = df['body'].apply(lambda x: len(str(x))).min()

        print(f"- Total de comentários: {total}")
        print(f"- Média de palavras por comentário: {media_palavras:.2f}")
        print(f"- Mediana de palavras por comentário: {mediana_palavras}")
        print(f"- Comentário mais longo (caracteres): {max_comentario}")
        print(f"- Comentário mais curto (caracteres): {min_comentario}")

        return {
            "total": total,
            "media_palavras": media_palavras,
            "mediana_palavras": mediana_palavras,
            "mais_longo": max_comentario,
            "mais_curto": min_comentario
        }
    except KeyError:
        print("Erro: coluna 'body' não encontrada no DataFrame.")
    except Exception as e:
        print(f"Erro inesperado na análise de dados: {e}")
    return {}