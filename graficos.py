import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import cab


def plotar_graficos(df: pd.DataFrame) -> None:
    """
    Cria e salva gráficos a partir do DataFrame usando apenas seaborn.
    Os gráficos incluem linhas verticais representando a média.
    
    Args:
        df (pd.DataFrame): DataFrame contendo os comentários (já com colunas 'tamanho' e 'num_palavras').
    
    Returns:
        None
    """
    cab("5. CRIAÇÃO DE GRÁFICOS (SEABORN)")

    try:
        sns.set_theme(style="whitegrid")

        # Gráfico 1: número de comentários por postId
        plt.figure(figsize=(12, 6))
        ax1 = sns.countplot(
            x="postId",
            data=df,
            color="skyblue",
            order=df["postId"].value_counts().index.sort_values()
        )
        ax1.set_title("Número de comentários por Post")
        ax1.set_xlabel("postId")
        ax1.set_ylabel("Quantidade de comentários")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("comentarios_por_post.png")
        plt.close()
        print("Gráfico 'comentarios_por_post.png' criado.")

        # Gráfico 2: distribuição do tamanho dos comentários (em caracteres)
        plt.figure(figsize=(10, 5))
        ax2 = sns.histplot(df["tamanho"], bins=30, kde=True, color="lightgreen")
        media_caracteres = df["tamanho"].mean()
        ax2.axvline(media_caracteres, color="red", linestyle="--", label=f"Média: {media_caracteres:.1f}")
        ax2.set_title("Distribuição do tamanho dos comentários (caracteres)")
        ax2.set_xlabel("Número de caracteres")
        ax2.set_ylabel("Frequência")
        ax2.legend()
        plt.tight_layout()
        plt.savefig("tamanho_comentarios.png")
        plt.close()
        print("Gráfico 'tamanho_comentarios.png' criado.")

        # Gráfico 3: distribuição do número de palavras por comentário
        plt.figure(figsize=(10, 5))
        ax3 = sns.histplot(df["num_palavras"], bins=20, kde=True, color="orange")
        media_palavras = df["num_palavras"].mean()
        ax3.axvline(media_palavras, color="red", linestyle="--", label=f"Média: {media_palavras:.1f}")
        ax3.set_title("Distribuição de palavras por comentário")
        ax3.set_xlabel("Número de palavras")
        ax3.set_ylabel("Frequência")
        ax3.legend()
        plt.tight_layout()
        plt.savefig("palavras_por_comentario.png")
        plt.close()
        print("Gráfico 'palavras_por_comentario.png' criado.")

    except KeyError as e:
        print(f"Erro: coluna não encontrada no DataFrame ({e}).")
    except Exception as e:
        print(f"Erro inesperado na criação dos gráficos: {e}")