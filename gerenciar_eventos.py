import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

# Configuração do banco de dados SQLite
def conectar_bd():
    conn = sqlite3.connect('eventos.db')
    cursor = conn.cursor()
    return conn, cursor

# Função para criar tabelas no banco de dados
def criar_tabelas():
    conn, cursor = conectar_bd()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            data_evento TEXT,
            data_encerramento TEXT,
            vagas INTEGER,
            vagas_preenchidas INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Ativo'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT,
            id_evento INTEGER,
            data_inscricao TEXT,
            FOREIGN KEY (id_evento) REFERENCES eventos (id)
        )
    ''')
    conn.commit()
    conn.close()

# Função para simular eventos iniciais
def simular_eventos_iniciais():
    eventos_simulados = [
        ("Workshop de Python", "Um workshop para iniciantes em Python.", "2024-11-15", "2024-11-10", 30),
        ("Palestra sobre Inteligência Artificial", "Palestra sobre o futuro da IA.", "2024-12-05", "2024-11-30", 50),
        ("Hackathon de Data Science", "Maratona de desenvolvimento de soluções em Data Science.", "2024-12-20", "2024-12-15", 25),
        ("Seminário de Tecnologia", "Discussão sobre novas tecnologias e inovações.", "2024-11-25", "2024-11-20", 40),
        ("Treinamento de SQL", "Treinamento intensivo de SQL para análise de dados.", "2024-11-30", "2024-11-25", 35)
    ]

    conn, cursor = conectar_bd()
    for nome, descricao, data_evento, data_encerramento, vagas in eventos_simulados:
        cursor.execute('SELECT * FROM eventos WHERE nome = ? AND data_evento = ?', (nome, data_evento))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO eventos (nome, descricao, data_evento, data_encerramento, vagas, vagas_preenchidas)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (nome, descricao, data_evento, data_encerramento, vagas))
    conn.commit()
    conn.close()

# Função para simular inscrições iniciais
def simular_inscricoes_iniciais():
    inscricoes_simuladas = [
        ("Ana Clara", "Workshop de Python"),
        ("Pedro Silva", "Palestra sobre Inteligência Artificial"),
        ("Mariana Santos", "Hackathon de Data Science"),
        ("João Almeida", "Seminário de Tecnologia"),
        ("Laura Ferreira", "Treinamento de SQL"),
        ("Carlos Pereira", "Workshop de Python"),
        ("Julia Souza", "Palestra sobre Inteligência Artificial"),
        ("Mateus Silva", "Hackathon de Data Science"),
        ("Luana Lima", "Seminário de Tecnologia"),
        ("André Santos", "Treinamento de SQL")
    ]

    conn, cursor = conectar_bd()
    for nome_aluno, nome_evento in inscricoes_simuladas:
        cursor.execute('SELECT id, vagas, vagas_preenchidas FROM eventos WHERE nome = ?', (nome_evento,))
        evento = cursor.fetchone()

        if evento:
            id_evento, vagas, vagas_preenchidas = evento
            if vagas_preenchidas < vagas:
                data_inscricao = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('''
                    INSERT INTO inscricoes (nome_aluno, id_evento, data_inscricao)
                    VALUES (?, ?, ?)
                ''', (nome_aluno, id_evento, data_inscricao))
                cursor.execute('UPDATE eventos SET vagas_preenchidas = vagas_preenchidas + 1 WHERE id = ?', (id_evento,))
    conn.commit()
    conn.close()

# Função para visualizar eventos
def visualizar_eventos():
    conn, cursor = conectar_bd()
    cursor.execute('SELECT id, nome, descricao, data_evento, data_encerramento, vagas, vagas_preenchidas, status FROM eventos')
    eventos = cursor.fetchall()
    conn.close()
    return eventos

# Função para inscrever aluno em evento
def inscrever_aluno(nome_aluno, nome_evento):
    conn, cursor = conectar_bd()
    cursor.execute('SELECT id, vagas, vagas_preenchidas, data_encerramento, status FROM eventos WHERE nome = ?', (nome_evento,))
    resultado = cursor.fetchone()

    if resultado:
        id_evento, vagas, vagas_preenchidas, data_encerramento, status = resultado
        data_encerramento = datetime.strptime(data_encerramento, '%Y-%m-%d')
        hoje = datetime.now()

        if status == "Cancelado":
            st.error("Este evento foi cancelado.")
        elif vagas_preenchidas < vagas and hoje <= data_encerramento:
            cursor.execute('INSERT INTO inscricoes (nome_aluno, id_evento, data_inscricao) VALUES (?, ?, ?)', 
                           (nome_aluno, id_evento, hoje.strftime('%Y-%m-%d')))
            cursor.execute('UPDATE eventos SET vagas_preenchidas = vagas_preenchidas + 1 WHERE id = ?', (id_evento,))
            conn.commit()
            st.success(f"Inscrição de {nome_aluno} realizada com sucesso!")
        elif hoje > data_encerramento:
            st.error("As inscrições para este evento estão encerradas.")
        else:
            st.error("Evento sem vagas disponíveis.")
    else:
        st.error("Evento não encontrado.")
    conn.close()

# Função para visualizar alunos por evento
def visualizar_alunos_por_evento(nome_evento):
    conn, cursor = conectar_bd()
    cursor.execute('''
        SELECT i.nome_aluno 
        FROM inscricoes i
        JOIN eventos e ON i.id_evento = e.id
        WHERE e.nome = ?
    ''', (nome_evento,))
    alunos = cursor.fetchall()
    conn.close()
    return alunos

# Função para editar evento
def editar_evento(nome_evento, novo_nome, nova_descricao, nova_data_evento, nova_data_encerramento, cancelar=False):
    conn, cursor = conectar_bd()
    if cancelar:
        cursor.execute('UPDATE eventos SET status = "Cancelado" WHERE nome = ?', (nome_evento,))
    else:
        cursor.execute('''
            UPDATE eventos 
            SET nome = ?, descricao = ?, data_evento = ?, data_encerramento = ?
            WHERE nome = ?
        ''', (novo_nome, nova_descricao, nova_data_evento, nova_data_encerramento, nome_evento))
    conn.commit()
    conn.close()

# Configuração da interface com Streamlit
st.set_page_config(page_title="Gerenciamento de Eventos", layout="wide")
st.title("Sistema de Gerenciamento de Eventos")

# Criar tabelas no banco de dados
criar_tabelas()

# Simular eventos e inscrições iniciais
simular_eventos_iniciais()
simular_inscricoes_iniciais()

# Menu de navegação
opcao = st.sidebar.selectbox("Selecione uma opção", ["Cadastrar Evento", "Visualizar Eventos", "Inscrição em Evento", "Alunos por Evento", "Editar Evento"])

# Implementação das funcionalidades baseadas na opção selecionada
if opcao == "Cadastrar Evento":
    st.header("Cadastrar Novo Evento")
    nome = st.text_input("Nome do Evento")
    descricao = st.text_area("Descrição do Evento")
    data_evento = st.date_input("Data do Evento")
    data_encerramento = st.date_input("Data de Encerramento das Inscrições")
    vagas = st.number_input("Número de Vagas", min_value=1, step=1)

    if st.button("Cadastrar Evento"):
        if nome and descricao and data_encerramento <= data_evento:
            conn, cursor = conectar_bd()
            cursor.execute('''
                INSERT INTO eventos (nome, descricao, data_evento, data_encerramento, vagas, vagas_preenchidas)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (nome, descricao, data_evento.strftime('%Y-%m-%d'), data_encerramento.strftime('%Y-%m-%d'), vagas))
            conn.commit()
            conn.close()
            st.success("Evento cadastrado com sucesso!")
        else:
            st.error("Preencha todos os campos e verifique se a data de encerramento é antes da data do evento.")

elif opcao == "Visualizar Eventos":
    st.header("Eventos Disponíveis")
    eventos = visualizar_eventos()
    if eventos:
        df_eventos = pd.DataFrame(eventos, columns=["ID", "Nome", "Descrição", "Data do Evento", "Data de Encerramento", "Vagas Totais", "Vagas Preenchidas", "Status"])
        st.dataframe(df_eventos, use_container_width=True)

elif opcao == "Inscrição em Evento":
    st.header("Inscrição em Evento")
    eventos = visualizar_eventos()
    if eventos:
        nomes_eventos = [evento[1] for evento in eventos if evento[-1] == "Ativo"]
        nome_evento = st.selectbox("Selecione o Evento", options=nomes_eventos)

        nome_aluno = st.text_input("Nome do Aluno")

        if st.button("Inscrever"):
            if nome_aluno and nome_evento:
                inscrever_aluno(nome_aluno, nome_evento)
            else:
                st.error("Insira o nome do aluno.")

elif opcao == "Alunos por Evento":
    st.header("Lista de Alunos Cadastrados por Evento")
    eventos = visualizar_eventos()
    if eventos:
        nomes_eventos = [evento[1] for evento in eventos]
        nome_evento = st.selectbox("Selecione o Evento para Visualizar Alunos", options=nomes_eventos)

        if nome_evento:
            alunos = visualizar_alunos_por_evento(nome_evento)
            if alunos:
                df_alunos = pd.DataFrame(alunos, columns=["Nome do Aluno"])
                st.dataframe(df_alunos, use_container_width=True)
            else:
                st.info("Nenhum aluno cadastrado neste evento.")
    else:
        st.info("Nenhum evento disponível para visualização.")

elif opcao == "Editar Evento":
    st.header("Editar Evento")
    eventos = visualizar_eventos()
    if eventos:
        nomes_eventos = [evento[1] for evento in eventos if evento[-1] == "Ativo"]
        nome_evento = st.selectbox("Selecione o Evento para Editar", options=nomes_eventos)

        if nome_evento:
            evento_selecionado = [evento for evento in eventos if evento[1] == nome_evento][0]
            novo_nome = st.text_input("Novo Nome do Evento", value=evento_selecionado[1])
            nova_descricao = st.text_area("Nova Descrição do Evento", value=evento_selecionado[2])
            nova_data_evento = st.date_input("Nova Data do Evento", value=datetime.strptime(evento_selecionado[3], '%Y-%m-%d'))
            nova_data_encerramento = st.date_input("Nova Data de Encerramento", value=datetime.strptime(evento_selecionado[4], '%Y-%m-%d'))

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Atualizar Evento"):
                    editar_evento(nome_evento, novo_nome, nova_descricao, nova_data_evento.strftime('%Y-%m-%d'), nova_data_encerramento.strftime('%Y-%m-%d'))
                    st.success(f"Evento '{nome_evento}' atualizado com sucesso!")
            with col2:
                if st.button("Cancelar Evento"):
                    editar_evento(nome_evento, novo_nome, nova_descricao, nova_data_evento.strftime('%Y-%m-%d'), nova_data_encerramento.strftime('%Y-%m-%d'), cancelar=True)
                    st.success(f"Evento '{nome_evento}' foi cancelado.")

# Fechar conexão com o banco de dados ao finalizar
if st.sidebar.button("Sair"):
    st.write("Obrigado por utilizar o sistema de gerenciamento de eventos!")
