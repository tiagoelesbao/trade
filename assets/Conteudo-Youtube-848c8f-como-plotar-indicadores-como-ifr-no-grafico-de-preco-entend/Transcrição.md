# Transcrição — Índice Força Relativa (IFR) no Gráfico - Indicador Programação Profitchart

Então, eu queria mostrar um indicador aqui e FR no gráfico, porque, primeiro, porque
eu noto muitas pessoas perguntando sobre, ah, eu quero plotar o meu maquidino gráfico,
eu quero plotar tal indicador, enfim, no gráfico, só que a gente tem que entender que a
gente tem que sempre trabalhar na mesma escala, comparar, eu sempre brinco, você vai comparar
banana com banana e massa com maçã, não dá para comparar banana com maçã, não é uma
comparação justa, então, matemáticamente falando isso, você tem que seguir também, então,
por exemplo, vamos pegar o FR e o FR é um bom exemplo, porque, vamos adicionar ele aqui no gráfico,
o FR nativo, o índice de força relativo, porque o FR é um acilador, e o que é um acilador?
O acilador é uma categoria, vamos dizer assim, de indicadores, onde os valores vão variar entre
uma determinada limitação, no caso do FR entre 0 e 100, então, é isso que um acilador faz, ele
é um acilo entre uma limitação, no caso do FR, 0 e 100, você tem diversos tipos de
aciladores, com diversos tipos de variações, menos 100, 100, 1, 0, menos 1, 1, enfim,
depende de como é o cálculo ele executado, mas o ponto importante a ser observado é que são
as diferentes, então, eu só vou alterando enquanto a gente vai conversando aqui para ficar mais visual,
mas o ponto é, essas escalas diferentes, você não pode esperar que você conseguirá comparar
matemáticamente com o preço, como a gente está observando aqui, pega um exemplo aqui do índice de
força relativa, esses valores que ele está plotando aqui, como é que você quer plotar sobre
posto no gráfico, enquanto a gente está lidando de um número 0 a 100, enquanto o nosso preço está na
região lá do 5600, por exemplo, claro que essa informação não bate, agora, existem formas de você
correlacionar essa informação, para que o o acilador, no caso desse exemplo FR tivete passando,
uma forma de você correlacionar com o gráfico de preço, então, esse é um código exemplo bem
simples, esses códigos que eu apresento, veja bem, eu não estou reenvidicando a autoria deles,
eu não criei, inventei nada aqui, a grande verdade é que todos esses estudos, tá bom, não vou dizer todos,
para não ser injusto, mas 99,9% dos estudos e indicadores que existem aí, que a gente conhece,
a grande verdade é que eles precedem até o mercado brasileiro, o financeiro brasileiro, em termos
de ações, B3, BNF, Bolvés, antes de ter nascido, tá, isso que é a grande verdade, porque vem de
mercado americano, vem de estudos de mercado americano que provavelmente precedem até esse estudo mais
moderno, mas moderno gráfico, enfim, então, tudo que a gente apresenta aqui, no fim dão das contas,
as adaptações do que já existe, leituras do que já existe, tá, então, o que a gente está fazendo basicamente
aqui, a gente tem duas condições, duas condições principais aqui, aqui são pequenas correções de
plotagem que a gente vai falar, mas são basicamente duas condições em que, naturalmente ou puramente,
a forma em que o FR lido, observando essas regiões 70 e 30, que são padrão, mas obviamente existe, você
pode ir argumentar 80, 20, 90, 10, depende da leituras, uma leitura encaixa melhor com um ativo específico,
com uma periodicidade específico, enfim, mas, por via de regra, vamos usar o 7030, que é o mais conhecido,
onde, acima de 30, a gente ler isso, como uma região sobrecomprada, e o inverso na região 30, a gente
leia isso como uma região sobrevendida, então, a gente pega aqui, quando, e o que a gente faz, como a gente
não pode fazer essa correlação ou essa alinhamento puro do número, do número 30 com a nossa
escala, o que a gente faz, quando ocorre essa circunstância aqui, por exemplo, se a gente está usando,
vamos até usar a mesma cor para fazer sentido, quando a gente está lendo aqui a região abaixo
de 30, quando a gente está lendo essa região abaixo de 30, o que a gente faz, a gente armazena numa variável
o preço de fechamento anterior, e a gente pede para plotar, preso B aqui, o nosso preço de fechamento,
e o que isso significa, então, se a gente pegar esse momento aqui em que essa ocorrência, vamos dizer assim,
note que o que ele faz é demarcar no nosso gráfico aquele ponto, que correlaciona o momento em que o
indicador chegou naquela região de preço, perdão, chegou naquela região de valor, de o
silador de sobrevendido, e a gente corre relaciona isso com o valor da nossa escala de preço, do nosso
gráfico, usando o preço de fechamento aqui da barra anterior, quando isso não ocorre, a gente simplesmente
repete o valor anterior, para dar justamente esse efeito de linha vertical, porque ele fica
replotando, ele encontra o primeiro valor aqui, e depois ele fica só repetindo, repete, repete, repete, repete, repete,
repete, repete, até o que? Até que uma nova condição seja satisfeita, ele atualiza, repete aí uma nova
condição satisfeita, atualiza, note que todas elas estão recorrelacionados com o que? Com momentos em que o
indicador aqui, o nosso indicador o silador e FR passa lá para baixo, o mesmo na ponta contrária,
então se você observar a ponta contrária, que seria a região sobrecomprada, vamos fazer a mesma coisa
acima de 70, o que ele faz, ele é armazeno o preço, numa variável diferente, agora pressuar, caso
não haja este acondição, o que ele faz, ele simplesmente repete o preço anterior, e aí o efeito disso,
como a gente viu aqui no região sobrevendida, vai ser aqui no sobrecomprado, como não aconteceu mais,
você nota que ele veio repetindo aqui, você nota que este valor ele vem ao lado passado, só que como
aqui aconteceu um novo fenômeno, ele parou de plotar aqui e encontramos um novo valor
ser plotado, e aí ele vem plotando até que, em algum momento aqui, no futuro, em relação a esse gráfico,
isso aqui ocorra de novo, esse valor vem cruzar novamente aqui, a região do 70, e aí ele vai traçar uma
nova linha onde quer, que seja, no preço de fechamento, para corre relacionar essa informação, então
basicamente é isso que a gente está fazendo, então note que agora assim faz sentido, a gente corre
relacionar um ossilador que tem uma escala completamente diferente, com a nossa escala de preço, então eu
falei que eu mencionei aqui a única observação que eu faço, porque aqui você, como você viu, a gente plot
esses valores, a única coisa que eu faço aqui é que quando ele encontra essa mudança de condição,
ou seja, houve uma alteração nesse valor, se a gente pensar na linha vermelha, o valor
deste em relação a este, o novo valor aconteceu, ele usa a função não no plot, que cancela
a plotagem anterior, para quebrar essa linha, porque do contrário o que aconteceria é, ele plotaria
a linha de agonais conectando essas plotagens, e aí tudo bem, você pode argumentar que dependendo
o que você quer, é melhor ter isso, fica gosto aí, que você pode observar, se a gente fizer o que,
se a gente vou comentar isso aqui, só para você ver o que aconteceria, note que ele começa a fazer
essas plotagens de contínuas, o que você pode argumentar que pode te ajudar, dependendo da
configuração que você fizer a observar regiões, enfim, é que estão meio de gosto, também,
eu estou aqui para editar isso, mas eu só queria mostrar isso, então basicamente, hoje
eu queria mostrar uma periodicidade diferente, que ele vai abrir um frente, justamente para mostrar
que corre relacionando essas informações, mesmo que agora em escalas diferentes, se a gente
tem uma forma válida, vamos dizer assim, de relacionar essas duas escalas diferentes, a gente consegue
se extrair a informação útil, então fica aí um indicador, fica aí essa dica, obviamente você
pode ter percebido o serve para qualquer outro indicador, e posso até apresentar outros aí conhecidos
famosos que usam esse tipo de interpretação, para fazer algo parecido.
