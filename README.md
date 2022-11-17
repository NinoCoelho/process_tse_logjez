# Processador de Logs do TSE

Para processar os arquivos, primeiro baixe-os do [site do TSE](https://dadosabertos.tse.jus.br/dataset/resultados-2022-arquivos-transmitidos-para-totalizacao)

Há 2 scripts em python principais. Um processa todos os arquivos gerando 2 arquivos por estado, um com os dados por urna, incluindo o modelo da urna, e o outro com os votos para cada candidato, brancos e nulos; o outro serve somente para fazer a busca por texto dentro dos logs.

Há também um Jupyter Notebook pronto para gerar as análises e gráficos básicos.

Para sua conveniência, incluí os arquivos que eu gerei previamente na pasta **[csv_gerados](csv_gerados)**, assim você poderá executar o notebook de análise dos dados tão logo você baixe esse repositório.

Jupyter Notebook é uma das mais utilizadas ferramentas em Data Science (ciencia de dados) e permite processar e visualizar grande quantidade de informação com rapidez e precisão. 

[Clique aqui para visualizar um exemplo das informações extraídas com esse estudo](https://htmlpreview.github.io/?https://raw.githubusercontent.com/NinoCoelho/process_tse_logjez/master/auditoriaEleicoes.html)

Usando esse projeto você pode, não só repetir esse estudo, mas realizar outros estudos, já que há muito mais informação disponível, que não foram consideradas nesse estudo preliminar

## Instalação


Baixe esse repositório e instale também o Jupyter Notebook.

Eu utilizei o [Microsoft Visual Studio Code](https://code.visualstudio.com/) com o Jupyter Notebook

## Usage

Para processar os arquivos da pasta **logjez** e gerar os respectivos na pasta **csv_gerados**, primeiramente crie estas duas pastas na pasta onde baixou o projeto, e depois execute o comando:

```shell
python logjez_process.py
```
Esse script vai ler todos os arquivos de log em formato **zip** da pasta **logjez** e gerar os respectivos arquivos de voto e urnas na pasta **csv_gerados**

Se voce deseja somente buscar algum texto dentro dos arquivos de log, use o exemplo abaixo

```shell
logjez_grep.py "Modelo de Urna"
```

Esse comando gera uma lista das linhas contendo essa sequencia, exemplo:

```
27/09/2022 09:03:07	INFO	67305985	SCUE	Identificação do Modelo de Urna: UE2009	8801289B29EECD19
27/09/2022 09:11:26	INFO	67305985	SCUE	Identificação do Modelo de Urna: UE2009	7819A03E9B0AAAD2
28/09/2022 18:38:25	INFO	67305985	SCUE	Identificação do Modelo de Urna: UE2010	E8413B4968B45D74
27/09/2022 09:03:07	INFO	67305985	SCUE	Identificação do Modelo de Urna: UE2009	8801289B29EECD19
21/09/2022 10:26:00	INFO	2211301	SCUE	Identificação do Modelo de Urna: UE2020	32D1DDC5144FE449
21/09/2022 10:32:14	INFO	2074364	SCUE	Identificação do Modelo de Urna: UE2020	33578CB4B9CC1FF8
```

O arquivo [modeloDeUrna.zip](modeloDeUrna.zip) contem a extração acima para todas as urnas do Brasil, e mostra que, enquanto as urnas UE2020 contém as identificações de urna corretas, todos os modelos anteriores tem o código de urna cravado como 67305985, o que prova que 1) o software instalado nas urnas UE2020 difere das anteriores e 2) há uma falha nessas urnas antigas que pode ter sido causada pelo software malicioso que fraudou os votos. Possivelmente, no fechamento das urnas, o log era adulterado  para esconder evidências das fraudes, porém o desenvolvedor não conseguiu capturar o código da urna, ou errou na hora de formatar o log fraudado.

## Jupyter Notebook

Jupyter Notebook é uma ferramenta para análise de dados muito utilizada por cientistas de dados. O arquivo **auditoriaEleicoes.ipynb** pode ser aberto nesse âmbiente para gerar gráficos e relatórios a fim de analisar os dados das urnas



## Contributing

Fique a vontade pra contribuir ou clonar esse repositorio e realizar suas proprias pesquisas

Nao esqueca de publicar suas conclusoes em suas redes sociais

Eu utilizei o [Microsoft Visual Studio Code](https://code.visualstudio.com/) com o Jupyter Notebook para realizar a análise e o desenvolvimento destes programas

Se você precisar de algum suporte, conte comigo. Basta criar um issue descrevendo sua dúvida que farei o máximo para te ajudar

Repetir essas análises e validar ou contradizer as acusações do PL, assim como os pontos apontados pelo relatório das FFAA ou indícios apontados pelo PSDB em 2014, são um bom caminho para você, profissional de TI, servir de forma patriótica seu paiz.

## License

[MIT](https://choosealicense.com/licenses/mit/)
