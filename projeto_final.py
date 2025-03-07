import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def conectar():
    return sqlite3.connect('clinica.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def inserir_paciente():
    nome = entry_nome.get()
    idade = entry_idade.get()
    peso = entry_peso.get()
    altura = entry_altura.get()

    if nome and idade and peso and altura:
        try:
            idade = int(idade)
            peso = float(peso)
            altura = float(altura)

            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO pacientes(nome, idade, peso, altura) VALUES(?, ?, ?, ?)', (nome, idade, peso, altura))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Paciente cadastrado com sucesso!')
            mostrar_pacientes()
        except ValueError:
            messagebox.showerror('Erro', 'Certifique de que todos os campos estão preenchidos corretamente!')
    else:
        messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos!')

def mostrar_pacientes():
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM pacientes')
    pacientes = c.fetchall()

    for paciente in pacientes:
        imc = calcular_imc(paciente[3], paciente[4])
        tree.insert("", "end", values=(paciente[0], paciente[1], paciente[2], paciente[3], paciente[4], f"{imc:.2f}"))
    conn.close()

def delete_paciente():
    dado_del = tree.selection()
    if dado_del:
        paciente_id = tree.item(dado_del)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Paciente deletado com sucesso!')
        mostrar_pacientes()
    else:
        messagebox.showerror('Erro', 'Selecione um paciente para deletar!')

def editar_paciente():
    selecao = tree.selection()
    if selecao:
        paciente_id = tree.item(selecao)['values'][0]
        novo_nome = entry_nome.get()
        nova_idade = entry_idade.get()
        novo_peso = entry_peso.get()
        nova_altura = entry_altura.get()

        if novo_nome and nova_idade and novo_peso and nova_altura:
            try:
                nova_idade = int(nova_idade)
                novo_peso = float(novo_peso)
                nova_altura = float(nova_altura)

                conn = conectar()
                c = conn.cursor()
                c.execute('UPDATE pacientes SET nome = ?, idade = ?, peso = ?, altura = ? WHERE id = ?',
                          (novo_nome, nova_idade, novo_peso, nova_altura, paciente_id))
                conn.commit()
                conn.close()

                messagebox.showinfo('Sucesso', 'Dados do paciente atualizados com sucesso!')
                mostrar_pacientes()
            except ValueError:
                messagebox.showerror('Erro', 'Certifique-se de que todos os campos estão preenchidos corretamente!')
        else:
            messagebox.showwarning('Aviso', 'Preencha todos os campos!')
    else:
        messagebox.showerror('Erro', 'Selecione um paciente para editar!')

janela = tk.Tk()
janela.title('Sistema de Cadastro de Pacientes - Clínica Saúde & Bem-Estar')

label_nome = tk.Label(janela, text='Nome:')
label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_idade = tk.Label(janela, text='Idade:')
label_idade.grid(row=1, column=0, padx=10, pady=10)
entry_idade = tk.Entry(janela)
entry_idade.grid(row=1, column=1, padx=10, pady=10)

label_peso = tk.Label(janela, text='Peso (kg):')
label_peso.grid(row=2, column=0, padx=10, pady=10)
entry_peso = tk.Entry(janela)
entry_peso.grid(row=2, column=1, padx=10, pady=10)

label_altura = tk.Label(janela, text='Altura (m):')
label_altura.grid(row=3, column=0, padx=10, pady=10)
entry_altura = tk.Entry(janela)
entry_altura.grid(row=3, column=1, padx=10, pady=10)

btn_salvar = tk.Button(janela, text='Salvar', command=inserir_paciente)
btn_salvar.grid(row=4, column=0, padx=10, pady=10)

btn_deletar = tk.Button(janela, text='Deletar', command=delete_paciente)
btn_deletar.grid(row=5, column=0, padx=10, pady=10)

btn_atualizar = tk.Button(janela, text='Atualizar', command=editar_paciente)
btn_atualizar.grid(row=6, column=0, padx=10, pady=10)

columns = ('ID', 'Nome', 'Idade', 'Peso', 'Altura', 'IMC')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_pacientes()

janela.mainloop()