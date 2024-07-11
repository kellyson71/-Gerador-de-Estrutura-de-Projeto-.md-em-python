import os

def imprimir_estrutura_diretorio(diretorio_base, nivel=0):
    for item in os.listdir(diretorio_base):
        if item == '.git':
            continue
        caminho_item = os.path.join(diretorio_base, item)
        if os.path.isdir(caminho_item):
            print('    ' * nivel + f"> {item}/")
            imprimir_estrutura_diretorio(caminho_item, nivel + 1)
        else:
            print('    ' * nivel + f"> {item}")

def ler_arquivos(diretorio_base):
    conteudo_arquivos = {}
    for raiz, dirs, arquivos in os.walk(diretorio_base):
        # Pular diretório .git
        dirs[:] = [d for d in dirs if d != '.git']
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(raiz, arquivo)
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    conteudo_arquivos[caminho_arquivo] = f.read()
            except UnicodeDecodeError:
                print(f"Pular arquivo não textual: {caminho_arquivo}")
    return conteudo_arquivos

def gerar_md(diretorio_base, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# Estrutura e Arquivos do Projeto\n\n")

        # Escrever estrutura do diretório
        md_file.write(f"## Estrutura do Diretório\n\n")
        for raiz, dirs, arquivos in os.walk(diretorio_base):
            # nesse caso eu coloquei para pular a pasta .git, mas você pode adicionar mais pastas que deseja pular ou ate mesmo remover 
            dirs[:] = [d for d in dirs if d != '.git']
            nivel = raiz.replace(diretorio_base, '').count(os.sep)
            indentacao = '    ' * nivel
            md_file.write(f"{indentacao}> {os.path.basename(raiz)}/\n")
            sub_indentacao = '    ' * (nivel + 1)
            for arquivo in arquivos:
                md_file.write(f"{sub_indentacao}> {arquivo}\n")
        
        # Escrever conteúdo dos arquivos
        md_file.write(f"\n## Conteúdo dos Arquivos\n\n")
        conteudo_arquivos = ler_arquivos(diretorio_base)
        for caminho_arquivo, conteudo in conteudo_arquivos.items():
            caminho_relativo = os.path.relpath(caminho_arquivo, diretorio_base)
            md_file.write(f"### {caminho_relativo}\n\n")
            md_file.write(f"```\n{conteudo}\n```\n\n")

def main():
    diretorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))  # Definir diretório base
    arquivo_saida = "estrutura_projeto.md"  # Nome do arquivo de saída

    print("\nEstrutura do diretório:\n")
    imprimir_estrutura_diretorio(diretorio_base)
    
    gerar_md(diretorio_base, arquivo_saida)
    print(f"\nArquivo '{arquivo_saida}' foi gerado.")

if __name__ == "__main__":
    main()
