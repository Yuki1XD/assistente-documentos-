# Histórias de Usuário

## US01 — Verificar API
**Como** usuário ou sistema integrado, **quero** verificar se a API está funcionando **para que** eu saiba se posso utilizá-la.

**Critérios de aceitação**
```gherkin
Cenário: API disponível
  Dado que a API está iniciada
  Quando eu consultar GET /health
  Então devo receber uma resposta de sucesso
  E o estado deve indicar que a API está funcionando
```
**Rastreabilidade:** RF01, UC01.

## US02 — Enviar arquivo
**Como** usuário, **quero** enviar um arquivo PDF ou TXT **para que** o sistema possa analisar seu conteúdo.

```gherkin
Cenário: Envio de arquivo permitido
  Dado que selecionei um arquivo PDF ou TXT válido
  Quando eu enviar o arquivo
  Então o sistema deve aceitar o envio
  E retornar um identificador do documento

Cenário: Formato não permitido
  Dado que selecionei um arquivo de formato não aceito
  Quando eu enviar o arquivo
  Então o sistema deve rejeitar o envio
  E informar os formatos aceitos
```
**Rastreabilidade:** RF02, RF03, RF04, UC02.

## US03 — Extrair texto
**Como** usuário, **quero** que o sistema extraia o texto do arquivo **para que** eu possa consultar seu conteúdo.

```gherkin
Cenário: Extração realizada
  Dado que enviei um PDF ou TXT legível
  Quando o sistema processar o documento
  Então deve extrair o texto disponível
  E disponibilizá-lo para armazenamento
```
**Rastreabilidade:** RF05, UC03.

## US04 — Salvar documento
**Como** usuário, **quero** que meus documentos sejam armazenados **para que** eu possa consultá-los depois.

```gherkin
Cenário: Documento salvo
  Dado que o texto do documento foi extraído
  Quando o sistema salvar os dados
  Então deve registrar os dados básicos e o texto
  E retornar o identificador do documento
```
**Rastreabilidade:** RF06, UC04.

## US05 — Consultar documentos
**Como** usuário, **quero** listar e consultar meus documentos **para que** eu encontre um arquivo enviado anteriormente.

```gherkin
Cenário: Consultar documento existente
  Dado que existe um documento cadastrado
  Quando eu solicitar sua consulta pelo identificador
  Então o sistema deve retornar seus dados

Cenário: Documento inexistente
  Dado que não existe documento com o identificador informado
  Quando eu solicitar a consulta
  Então o sistema deve informar que o documento não foi encontrado
```
**Rastreabilidade:** RF07, RF08, UC05.

## US06 — Gerar resumo
**Como** usuário, **quero** gerar um resumo do documento **para que** eu entenda seus pontos principais com mais rapidez.

```gherkin
Cenário: Resumo gerado
  Dado que existe um documento com texto extraído
  Quando eu solicitar um resumo
  Então o sistema deve retornar um resumo do conteúdo

Cenário: Documento sem texto disponível
  Dado que o documento não possui texto extraído
  Quando eu solicitar um resumo
  Então o sistema deve informar que não há conteúdo disponível para resumir
```
**Rastreabilidade:** RF09, UC06.

## US07 — Perguntar sobre documento
**Como** usuário, **quero** fazer perguntas sobre o documento **para que** eu encontre informações específicas sem ler todo o arquivo.

```gherkin
Cenário: Pergunta respondida com base no documento
  Dado que existe um documento processado
  Quando eu enviar uma pergunta sobre seu conteúdo
  Então o sistema deve responder com base nos trechos encontrados
  E apresentar referências quando disponíveis

Cenário: Informação não encontrada
  Dado que o documento não contém informação suficiente para responder
  Quando eu enviar uma pergunta
  Então o sistema deve informar que não encontrou dados suficientes
```
**Rastreabilidade:** RF10, RF11, UC07.

## US08 — Excluir documento
**Como** usuário, **quero** excluir um documento **para que** eu possa remover arquivos que não desejo mais manter.

```gherkin
Cenário: Exclusão concluída
  Dado que existe um documento que posso excluir
  Quando eu solicitar sua exclusão
  Então o sistema deve remover o documento e seus dados associados
  E confirmar a operação
```
**Rastreabilidade:** RF12, UC08.
