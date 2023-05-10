# RayTracing
Projeto para a disciplina de Processamento Gráfico

# Alunos 
## * João Pedro Ribeiro da Silva Dias - jprsd
## * Rodrigo Santos Batista - rsb6 

# Como Usar o Projeto
## O projeto é divido em classes então para os nossos objetos:
1 - Esfera, Essa como o próprio nome indica é responsável pela a criação dos objetos esfera em nossas cenas.
2 - Cena Objeto, Que se trata de nossa classe principal para redenrizar objetos na cena.
3 - Ray hit, Também é um nome sugestivo e indica a classe responsavel por gerênciar quando ah ou não um intersecção(hit) entre raios e os objetos da cena.
4 - Piso, Que é responsavel por criar a malha quadriculada abaixo das esferas.

## Alem das classes também existem funções auxiliares 
1 - color_fuctions, responsavel por fazer a soma, multiplicação por escalares e converter do padrão de 0 ate 1.0, para o padrão 0 a 255.
2 - reflexão e refração, responsavel por calcular as reflexões dos objetos e a refração do objeto.
3 - normalização, responsavel por criar a normal quando necessário.

## Pasta Entradas
Dentro dessa pasta existem vários arquivos de input com variações de nossas cenas, nos inputs de 1 a 3, apenas variamos a sombra das esferas e suas interções
Nos inputs de 4 a 6 variamos a posição das esferas.

## Explicando como funciona o aquivo de entrada
primeira linha: contem a dimensão da imagem a maioria dos arquivos é 480 X 640, lembrando que a primeira é y e a segunda x.
segunda linha: Define o tamanho do pixel e a distância focal da câmera.
terceira linha: Define a posição da câmera no espaço tridimensional (x, y, z).
quarta linha: Define a direção para a qual a câmera está apontando (vetor de olhar).
quinta linha: Define a orientação "para cima" da câmera.
sexta linha: Define a distância da câmera ao plano de imagem.
setima linha: Define o número de luzes na cena.
oitava linha: Define o número de objetos na cena.
nona linha: Define a primeira esfera na cena. Os valores são: posição x, posição y, posição z, coeficiente de reflexão ambiente (ka), coeficiente de reflexão difusa (kd), coeficiente de reflexão especular (ks), expoente especular (phongN), coeficiente de reflexão especular transparente (kr), coeficiente de transmissão transparente (kt), índice de refração (refN), operador de transformação (rot/scale/translate), valor 1, valor 2, valor 3.
decima linha: Define a segunda esfera na cena. A sintaxe é a mesma que na linha anterior.
decima primeira linha: Define um objeto retangular na cena. Os valores são: cor vermelha, verde e azul (RGB), coeficiente de reflexão ambiente (ka), coeficiente de reflexão difusa (kd), coeficiente de reflexão especular (ks), expoente especular (phongN), coeficiente de reflexão especular transparente (kr), coeficiente de transmissão transparente (kt), índice de refração (refN), operador de transformação (rot/scale/translate), valor 1, valor 2, valor 3, valor 4, valor 5, valor 6.
decima segunda linha: Define a cor de fundo da cena (RGB).
decima terceira linha: Numero de luzes na cenas.
decima quarta linha: especificam a posição e cor Cada linha tem 6 valores: o primeiro é a intensidade vermelha da luz, o segundo é a intensidade verde, o terceiro é a intensidade azul, o quarto é a posição da luz no eixo x, o quinto é a posição da luz no eixo y e o sexto é a posição da luz no eixo z.
decima quinta e sexta: mesma sintaxe.

# Para rodar
Utilize o arquivo main.py e escolha uma entrada ou faça a sua e coloque no arquivo input, divirta-se!!

# Para aplicara textura
para texturas diferentes precisamos de nossa variavel texture_scale e para cada imagem é um valor diferente

piso de madeira / self.texture_scale = 0.01
terra (o planeta) / self.texture_scale = 1
metal / self.texture_scale = 0.05

