# Requisitos do Sistema

## 1. Requisitos funcionais (RF)

| ID | Requisito | Prioridade | Rastreabilidade |
|---|---|---|---|
| RF01 | O sistema deve disponibilizar um endpoint para verificar se a API está funcionando. | Alta | UC01, US01 |
| RF02 | O sistema deve permitir o envio de arquivos PDF e TXT. | Alta | UC02, US02 |
| RF03 | O sistema deve rejeitar arquivos com formatos não permitidos. | Alta | UC02, US02 |
| RF04 | O sistema deve validar o tamanho do arquivo enviado. | Alta | UC02, US02 |
| RF05 | O sistema deve extrair o texto de arquivos PDF e TXT válidos. | Alta | UC03, US03 |
| RF06 | O sistema deve armazenar os dados básicos e o texto extraído do documento. | Alta | UC04, US04 |
| RF07 | O sistema deve listar os documentos cadastrados. | Média | UC05, US05 |
| RF08 | O sistema deve apresentar os detalhes de um documento pelo seu identificador. | Média | UC05, US05 |
| RF09 | O sistema deve gerar um resumo do conteúdo de um documento. | Alta | UC06, US06 |
| RF10 | O sistema deve permitir que o usuário faça perguntas sobre um documento. | Alta | UC07, US07 |
| RF11 | O sistema deve apresentar referências às partes do documento usadas na resposta, quando disponíveis. | Alta | UC07, US07 |
| RF12 | O sistema deve permitir excluir um documento cadastrado. | Média | UC08, US08 |

## 2. Requisitos não funcionais (RNF)

| ID | Requisito | Prioridade |
|---|---|---|
| RNF01 | A API deve ser desenvolvida em Python utilizando FastAPI. | Alta |
| RNF02 | A API deve disponibilizar documentação interativa por OpenAPI/Swagger. | Alta |
| RNF03 | O sistema deve retornar mensagens de erro claras para entradas inválidas. | Alta |
| RNF04 | O sistema deve limitar o tamanho dos arquivos enviados. O limite exato será definido na implementação. | Alta |
| RNF05 | Chaves de serviços externos não devem ser armazenadas diretamente no código-fonte. | Alta |
| RNF06 | O sistema deve proteger documentos para que um usuário não acesse arquivos de outro usuário quando a autenticação for implementada. | Alta |
| RNF07 | O código deve ser organizado em módulos para facilitar manutenção. | Média |
| RNF08 | O sistema deve registrar erros técnicos sem expor o conteúdo privado dos documentos nos logs. | Alta |
| RNF09 | O projeto deve possuir instruções para instalação e execução local. | Alta |
| RNF10 | O processamento de documentos deve tratar arquivos corrompidos sem encerrar toda a API. | Alta |

## 3. Regras de negócio
- RN01: somente arquivos PDF e TXT serão aceitos na primeira versão.
- RN02: um documento precisa ser enviado e processado antes de permitir resumo ou perguntas.
- RN03: respostas devem se basear no conteúdo disponível do documento; quando não houver informação suficiente, o sistema deve informar essa limitação.
- RN04: a exclusão de um documento também deverá remover os dados associados a ele.

## 4. Rastreabilidade
Os requisitos funcionais estão relacionados aos casos de uso (UC) e às histórias de usuário (US) indicados na tabela. As issues propostas em `docs/issues/` também indicam os requisitos e histórias relacionados.
