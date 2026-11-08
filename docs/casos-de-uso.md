# Casos de Uso

## Atores
- **Usuário:** envia documentos e consulta seu conteúdo.
- **Serviço de IA:** serviço externo utilizado para gerar resumos e respostas.
- **Administrador do sistema:** acompanha a operação técnica da aplicação (papel futuro).

## UC01 — Verificar funcionamento da API
**Ator principal:** Usuário ou sistema externo.  
**Pré-condição:** API iniciada.

**Fluxo principal**
1. O ator solicita `GET /health`.
2. O sistema verifica sua disponibilidade.
3. O sistema retorna estado de funcionamento.

**Fluxo alternativo:** se algum componente essencial estiver indisponível, o sistema pode retornar estado de serviço degradado.  
**Exceção:** falha inesperada gera resposta de erro adequada.

## UC02 — Enviar documento
**Ator principal:** Usuário.  
**Pré-condição:** API disponível.

**Fluxo principal**
1. O usuário seleciona um arquivo PDF ou TXT.
2. O usuário envia o arquivo.
3. O sistema verifica extensão, tipo e tamanho.
4. O sistema aceita o arquivo e inicia o processamento.
5. O sistema informa o identificador do documento.

**Fluxo alternativo:** se o arquivo exceder o limite, o sistema informa que o tamanho não é permitido.  
**Exceção:** arquivo corrompido ou impossível de ler é recusado com mensagem clara.

## UC03 — Extrair texto
**Ator principal:** Sistema.  
**Pré-condição:** documento enviado.

**Fluxo principal**
1. O sistema identifica o formato do arquivo.
2. O sistema utiliza o extrator correspondente.
3. O sistema obtém o texto.
4. O sistema verifica se existe conteúdo textual.
5. O sistema disponibiliza o texto para armazenamento.

**Fluxo alternativo:** se o PDF não possuir texto selecionável, o sistema informa que não conseguiu extrair texto e que OCR não está incluído na primeira versão.  
**Exceção:** falha na leitura é registrada sem interromper a API.

## UC04 — Armazenar documento
**Ator principal:** Sistema.  
**Pré-condição:** texto extraído.

**Fluxo principal**
1. O sistema registra nome, formato, data e texto extraído.
2. O banco de dados confirma a gravação.
3. O sistema retorna o identificador do documento.

**Fluxo alternativo:** se o banco estiver indisponível, o sistema informa que não foi possível concluir o cadastro.  
**Exceção:** erro de gravação é registrado para análise.

## UC05 — Consultar documentos
**Ator principal:** Usuário.  
**Pré-condição:** existir ao menos um documento cadastrado.

**Fluxo principal**
1. O usuário solicita a lista ou os detalhes de um documento.
2. O sistema consulta os registros.
3. O sistema retorna os dados encontrados.

**Fluxo alternativo:** se não houver documentos, o sistema retorna uma lista vazia.  
**Exceção:** identificador inexistente retorna não encontrado.

## UC06 — Gerar resumo
**Ator principal:** Usuário.  
**Ator secundário:** Serviço de IA.  
**Pré-condição:** documento com texto extraído.

**Fluxo principal**
1. O usuário solicita o resumo.
2. O sistema recupera o texto do documento.
3. O sistema envia o conteúdo necessário ao serviço de IA.
4. O serviço retorna um resumo.
5. O sistema apresenta o resumo ao usuário.

**Fluxo alternativo:** para documentos muito extensos, o sistema poderá dividir o texto em partes antes de resumir.  
**Exceção:** se o serviço de IA estiver indisponível, o sistema informa que não conseguiu gerar o resumo.

## UC07 — Fazer pergunta sobre documento
**Ator principal:** Usuário.  
**Ator secundário:** Serviço de IA.  
**Pré-condição:** documento com texto extraído.

**Fluxo principal**
1. O usuário informa uma pergunta.
2. O sistema localiza trechos relevantes do documento.
3. O sistema envia a pergunta e os trechos ao serviço de IA.
4. O serviço retorna uma resposta.
5. O sistema apresenta a resposta e as referências disponíveis.

**Fluxo alternativo:** se não houver trecho relevante, o sistema informa que não encontrou informação suficiente.  
**Exceção:** falha no serviço externo gera mensagem de indisponibilidade.

## UC08 — Excluir documento
**Ator principal:** Usuário.  
**Pré-condição:** documento cadastrado.

**Fluxo principal**
1. O usuário solicita a exclusão pelo identificador.
2. O sistema verifica se o documento existe e se o usuário tem permissão.
3. O sistema remove o documento e os dados associados.
4. O sistema confirma a exclusão.

**Fluxo alternativo:** documento inexistente retorna mensagem de não encontrado.  
**Exceção:** falha no banco impede a exclusão e gera mensagem de erro.
