# Instituto Mises Brasil - Uma análise editorial usando Natural Language Processing

Sabe quando algo muda na redação de algum jornal, revista ou algum meio de 
comunicação, mas você não sabe o que é? Pois bem, eu fiquei com a mesma dúvida e
resolvi usar algumas ferramentas para validar se houve uma mudança ou não. 

## Background

Tem algum tempo que eu venho acompanhando a política brasileira da perspectiva de 
ensaístas de vertentes ligadas ao libertarianismo, anarcocapitalismo, secessão, 
autopropriedade e assuntos correlatos; e um fato que me chamou bastante a 
atenção foi a mudança editorial que está acontecendo de forma lenta em um dos 
principais Think Tanks liberais do Brasil que é o Instituto Mises Brasil (IMB).

Para quem não sabe, em meados de 2015 houve uma ruptura no núcleo do IMB em que 
de um lado ficou o Presidente do IMB (Hélio Beltrão) e do outro ficaram o 
Chiocca Brothers (Fernando, Cristiano, Roberto) que na sequência criaram o 
Instituto Rothbard. O motivo dessa ruptura foi devido a divergências relativas 
a artigos ligados a secessão.

E devido a esse processo de ruptura que eu penso que houve essa transição do 
IMB para uma linha editorial mais _leve_ no que diz respeito a assuntos ligados 
à liberdade o que contrário as ideias do próprio Ludwig von Mises.

## Qual o motivo desse repositório?

O principal motivo é fazer uma análise de dados simples usando Natural 
Processing Language (NLP) em todos textos do Mises Brasil para validar uma 
hipótese que é:

* __Hipótese [0]__: Houve uma mudança editorial no Instituto Mises Brasil em que 
assuntos ligados ao austrolibertarianismo, liberdade, ética, e secessão e 
outras questões relacionadas deram espaço para temas efêmeros como financismo, 
burocracia e principalmente política.

Caso a resposta da H0 seja positiva, eu vou tentar chegar nas repostas das 
seguintes perguntas que são:  

* __Pergunta [1]__: Caso H0 for verdadeira, assuntos ligados ao austrolibertarianismo 
como praxeologia, fim do estatismo, ética argumentativa, e secessão estão sendo 
deixados de lado em termos editoriais?

* __Pergunta [2]__: O Instituto Mises Brasil está se tornando em termos editoriais 
mais liberal-mainstream do que libertário?

* __Pergunta [3]__: Houve uma mudança em relação ao grupo de assuntos que são tratados 
ao longo do tempo como também a mudança do espectro de assuntos dos 
articulistas presentes?



## Preparação
Tudo isso foi gerado em um MacMini com Python 3.6, mas também pode ser executado
em computadores com Linux com a pré-instalação das seguintes bibliotecas:

```bash
$ pip install numpy==1.17.2
$ pip install pandas==0.25.1
$ pip install requests==2.22.0
$ pip install spacy==2.2.1
$ pip install beautifulsoup4==4.8.1
$ pip install bs4==0.0.1
$ python -m spacy download pt_core_news_sm
```
Sinceramente: Usem o R para geração dos seus próprios gráficos. Eu adoro o 
Seaborn e o Matplotlib para geração de gráficos, mas nesse sentido o R é muito 
mais flexível e precisa de bem menos “hacking” para fazer as coisas ficarem 
legais. 

## Extração de dados
A base que está no repositório foi gerada em 16.10.2019 para fins de congelar a 
análise e deixar a mesma com um grau maior de replicabilidade. 

A extração busca todos os textos, independente de ser artigo do blog ou post 
da página principal. Isso ocorre devido ao fato de que não há uma divisão das 
URLs que faça essa distinção e algumas vezes temos artigos do blog que viram 
posts na página principal.

Outro ponto é que deve ser mencionado é que o Leandro Roque é o principal 
tradutor/ ensaísta do site e alguns posts de tradução são assinados por ele 
(o que é correto). Isso leva a dois efeitos que são 1) ele e muito profícuo 
com o fluxo de artigos no site e definitivamente isso distorce as estatísticas 
individuais dele como ensaísta e 2) por causa das traduções ele tem um espectro 
de assuntos bem mais diversos do que os outros autores, e isso tem que ser 
considerado quando analisarmos os assuntos os quais ele mais escreve. 
Pessoalmente eu desconsideraria ele de todas as análises dado esses dois 
pontos colocados. Mas aí vai de cada um. 

Para quem quiser gerar uma base de dados nova com os dados até a presente data 
basta executar o comando abaixo no terminal:

```bash
$ python3 data-extraction.py
```

Ao final da execução vão aparecer as seguintes informações:
```
Fetching Time: 00:16:52
Articles fetched: 2855
```


## Avisos gerais
Essa análise é apenas para fins educacionais. É obvio que uma análise editorial 
que envolva questões linguísticas/semânticas é algo muito complexo até mesmo 
para nós seres humanos, e colocar que uma máquina consiga fazer isso é algo que
 não tem muito sentido dado a natureza da complexidade da linguagem e as suas 
 nuances.

Esse repositório como também a análise não tem a menor pretensão de ser algo 
"cientifico". Isso significa que não haverá elementos de linguística cognitiva, 
linguística computacional, análise do discurso ou ciências similares. Esse 
repositório traz muitas visões pessoais e observações que porventura usa alguns 
dados e alguns scripts.


## Distribuição e usos
 Todos os dados, scripts, gráficos podem ser usados livremente sem nenhum tipo 
 de restrição. Quem puder ajudar faz um hyperlink para o meu site/blog ou pode 
 citar academicamente que vai ajudar bastante.
 
 Eu não sou dono dos direitos dos textos do Instituto Mises Brasil e aqui tem 
 apenas uma compilação dos dados extraídos do site, dados estes públicos e que 
 podem ser extraídos por qualquer pessoa.


## Garantias, erros e afins
  Não existe garantia nestas análises, gráficos, dados e scripts e o uso 
  está por conta de quem usar. Vão ter muitos erros (principalmente gramaticais, 
  sintáticos e semânticos) e na medida que forem acontecendo podem abrir um 
  Pull Request ou me mandar um e-mail que eu vou ajustando. Porém, como eu vou 
  escrevendo na velocidade dos meus pensamentos nem sempre o sistema 
  responsável pela correção sintática vai funcionar bem.
