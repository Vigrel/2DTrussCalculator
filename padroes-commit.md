# Padrões de commits

Formato: 

`<tipo> (<escopo>) : <assunto> `

pular linha

`<corpo>`

## Tipos de commits:

- docs : Alterações apenas na documentação
- feat : Um novo recurso
- fix : uma correção de bug
- refactor : uma alteração de código que não corrige um bug ou adiciona um recurso
- reverter : Revertendo coisas
- style : marcação, espaço em branco, formatação, ponto e vírgula faltando ...

## Regras da mensagem / corpo:

- Separe o assunto do corpo com uma linha em branco
- Limite a linha de assunto a 50 caracteres
- Resumo no tempo presente. Sem letras maiúsculas.
- Não termine a linha de assunto com um ponto
- Use o humor imperativo na linha de assunto
- Envolva o corpo em 72 caracteres
- Use o corpo para explicar o que e por quê vs. como



## Exemplo

```
feat (file): add hat wobble
^--^         ^------------^
|            |
|            +-> Sempre no infinitivo.
|
+-------> Type: docs, feat, fix, refactor, reverter, style.
```
