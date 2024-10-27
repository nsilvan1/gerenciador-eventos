
# Sistema de Gerenciamento de Eventos

Este projeto é um sistema de gerenciamento de eventos, desenvolvido em Python, utilizando Streamlit para a interface gráfica e SQLite para o banco de dados.

## Funcionalidades

- **Cadastrar Evento:** Permite criar novos eventos com nome, descrição, data de realização, data de encerramento das inscrições e número de vagas.
- **Visualizar Eventos:** Exibe uma lista de todos os eventos cadastrados, incluindo detalhes como vagas preenchidas e status do evento.
- **Inscrição em Evento:** Permite a inscrição de alunos em eventos, verificando a disponibilidade de vagas e o prazo de inscrição.
- **Alunos por Evento:** Exibe os alunos inscritos em um evento específico.
- **Editar Evento:** Permite atualizar ou cancelar um evento existente.

## Como Executar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale as dependências do projeto com o comando:
    ```
    pip install -r requirements.txt
    ```
3. Execute o projeto com o seguinte comando:
    ```
    streamlit run gerenciar_eventos.py
    ```

## Requisitos do Sistema

- Python 3.7 ou superior
- Streamlit
- SQLite3
- Pandas

## Estrutura do Banco de Dados

O banco de dados é um arquivo SQLite (`eventos.db`) que contém duas tabelas principais:
1. **eventos:** Armazena os detalhes dos eventos.
2. **inscricoes:** Armazena as inscrições realizadas para os eventos.

## Contribuição

Sinta-se à vontade para contribuir com melhorias no projeto através de pull requests ou sugestões.

## Licença

Este projeto é de código aberto e está licenciado sob a MIT License.
