import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from utils import cab


def plotar_graficos(df: pd.DataFrame) -> None:
    """
    Cria e salva gráficos a partir do DataFrame usando apenas seaborn.
    Inclui medição de tempo de execução.
    """
    cab("5. CRIAÇÃO DE GRÁFICOS (SEABORN)")

    inicio_total: float = time.time()

    try:
        sns.set_theme(style="whitegrid")

        # Gráfico 1: número de comentários por postId
        inicio = time.time()
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
        fim = time.time()
        print(f"Gráfico 'comentarios_por_post.png' criado em {fim - inicio:.2f}s")

        # Gráfico 2: distribuição do tamanho dos comentários
        inicio = time.time()
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
        fim = time.time()
        print(f"Gráfico 'tamanho_comentarios.png' criado em {fim - inicio:.2f}s")

        # Gráfico 3: distribuição do número de palavras
        inicio = time.time()
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
        fim = time.time()
        print(f"Gráfico 'palavras_por_comentario.png' criado em {fim - inicio:.2f}s")

        # Gráfico 4: volume semanal de comentários x média de palavras
        inicio = time.time()
        df["semana"] = (df.index // 50) + 1
        weekly_data = df.groupby("semana").agg(
            comentarios_semana=("body", "count"),
            media_palavras=("num_palavras", "mean")
        ).reset_index()

        plt.figure(figsize=(12, 6))
        ax4 = sns.barplot(x="semana", y="comentarios_semana", data=weekly_data, color="skyblue")
        ax4.set_title("Volume semanal de comentários x Média de palavras")
        ax4.set_xlabel("Semana")
        ax4.set_ylabel("Número de comentários", color="blue")

        ax5 = ax4.twinx()
        sns.lineplot(x="semana", y="media_palavras", data=weekly_data, color="red", marker="o", ax=ax5)
        ax5.set_ylabel("Média de palavras", color="red")

        plt.tight_layout()
        plt.savefig("comentarios_semana_vs_palavras.png")
        plt.close()
        fim = time.time()
        print(f"Gráfico 'comentarios_semana_vs_palavras.png' criado em {fim - inicio:.2f}s")

    except KeyError as e:
        print(f"Erro: coluna não encontrada no DataFrame ({e}).")
    except Exception as e:
        print(f"Erro inesperado na criação dos gráficos: {e}")

    fim_total: float = time.time()
    print(f"Tempo total para gerar todos os gráficos: {fim_total - inicio_total:.2f}s")