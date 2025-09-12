import pandas as pd
from typing import Dict, Any
from utils import cab


def analisar_dados(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Realiza análise estatística dos comentários e cria colunas extras
    para facilitar a visualização nos gráficos.
    
    Args:
        df (pd.DataFrame): DataFrame com os comentários.
    
    Returns:
        Dict[str, Any]: Dicionário com métricas estatísticas principais.
    """
    cab("4. ANÁLISE ESTATÍSTICA")

    try:
        # Criar colunas auxiliares
        df["tamanho"] = df["body"].apply(lambda x: len(str(x)))           # caracteres
        df["num_palavras"] = df["body"].apply(lambda x: len(str(x).split()))  # palavras

        # Estatísticas gerais
        total: int = len(df)

        media_caracteres: float = df["tamanho"].mean()
        mediana_caracteres: float = df["tamanho"].median()
        desvio_caracteres: float = df["tamanho"].std()
        max_caracteres: int = df["tamanho"].max()
        min_caracteres: int = df["tamanho"].min()

        media_palavras: float = df["num_palavras"].mean()
        mediana_palavras: float = df["num_palavras"].median()
        desvio_palavras: float = df["num_palavras"].std()
        max_palavras: int = df["num_palavras"].max()
        min_palavras: int = df["num_palavras"].min()

        # Exibir resultados no console
        print(f"- Total de comentários: {total}")
        print(f"- Média de caracteres por comentário: {media_caracteres:.2f}")
        print(f"- Mediana de caracteres por comentário: {mediana_caracteres}")
        print(f"- Desvio padrão (caracteres): {desvio_caracteres:.2f}")
        print(f"- Comentário mais longo (caracteres): {max_caracteres}")
        print(f"- Comentário mais curto (caracteres): {min_caracteres}")
        print("---")
        print(f"- Média de palavras por comentário: {media_palavras:.2f}")
        print(f"- Mediana de palavras por comentário: {mediana_palavras}")
        print(f"- Desvio padrão (palavras): {desvio_palavras:.2f}")
        print(f"- Comentário com mais palavras: {max_palavras}")
        print(f"- Comentário com menos palavras: {min_palavras}")

        return {
            "total": total,
            "media_caracteres": media_caracteres,
            "mediana_caracteres": mediana_caracteres,
            "desvio_caracteres": desvio_caracteres,
            "max_caracteres": max_caracteres,
            "min_caracteres": min_caracteres,
            "media_palavras": media_palavras,
            "mediana_palavras": mediana_palavras,
            "desvio_palavras": desvio_palavras,
            "max_palavras": max_palavras,
            "min_palavras": min_palavras,
        }

    except KeyError:
        print("Erro: coluna 'body' não encontrada no DataFrame.")
    except Exception as e:
        print(f"Erro inesperado na análise de dados: {e}")

    return {}