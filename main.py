from utils import fetch_api_data, salvar_json, converter_para_csv
from analise import analisar_dados
from graficos import plotar_graficos


def main() -> None:
    """
    Executa o fluxo principal do projeto:
    1) Busca dados da API
    2) Salva em JSON
    3) Converte para CSV
    4) Analisa estatísticas
    5) Gera gráficos com seaborn
    """
    url: str = "https://jsonplaceholder.typicode.com/comments"

    #Buscar dados
    dados = fetch_api_data(url)
    if not dados:
        print("Execução encerrada: não foi possível obter dados da API.")
        return

    #Salva em JSON
    salvar_json(dados, "comentarios.json")

    #Converte para CSV
    df = converter_para_csv(dados, "comentarios.csv")
    if df is None:
        print("Execução encerrada: não foi possível criar o CSV.")
        return

    # Analisa estatísticas
    estatisticas = analisar_dados(df)

    # Gera gráficos
    plotar_graficos(df)

    print("\nExecução finalizada com sucesso.")
    print("Estatísticas principais calculadas:")
    for chave, valor in estatisticas.items():
        print(f"  {chave}: {valor}")


if __name__ == "__main__":
    main()