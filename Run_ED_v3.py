import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import requests
from os.path import isfile
import tkinter as tk
from tkinter import filedialog

os.system('cls')

def fetch_list_from_txt(url:str) -> list:
    """fetch the data from a remote txt and convert to list"""
    txt = requests.get(url).text
    return list(set(txt.split("\n")))

def check_file(check:str = "database.csv"): #requer from os.path import exists
    """check if a file with the name 'file_path' exists in the working dir"""
    return(isfile(check))

file = "database.csv"
FILE_FIRST_NAMES = "https://raw.githubusercontent.com/Tremocex/ALL_NAMES_PORTUGAL/main/names_final.txt"
FILE_SURNAMES = "https://raw.githubusercontent.com/Tremocex/ALL_NAMES_PORTUGAL/main/surnames_final.txt"

nomes = fetch_list_from_txt(FILE_FIRST_NAMES)
sobrenomes = fetch_list_from_txt(FILE_SURNAMES)

empregados = pd.read_csv(file, index_col=None) #será o nosso dataframe temporario, no fim decido se quero exportar para o .csv
empregados["first_name"] = empregados["first_name"].apply( str.capitalize)
empregados["surname"] = empregados["surname"].apply( str.capitalize)
empregados["job_title"] = empregados["job_title"].apply( str.lower)

def name_check(nome, lista_nomes):
    return nome in lista_nomes

def validar_data(input_data):
    try:
        # Tenta converter a string para um objeto datetime
        data = datetime.strptime(input_data, '%d/%m/%Y')
        return True, data
    except ValueError:
        # Se ocorrer um erro, informa que a data não está no formato correto
        return False, None

def create_new_employee(df, nomes, sobrenomes):
    os.system('cls')
    print('1 - CREATE NEW EMPLOYEE\n')    
    nome = input("Nome: ").upper()
    if name_check(nome,nomes) == True:
        nome = nome.capitalize()
        sobrenome = input("Sobrenome: ").upper()
        if name_check(sobrenome,sobrenomes) == True:
            sobrenome = sobrenome.capitalize()
            print(f'Para o novo registo de, {nome} {sobrenome}, inserir os seguintes dados.') 
                              
            while True:
                birth = input("Data de nascimento no formato dd/mm/yyyy: ")
                valido, data = validar_data(birth)
                if valido:
                    break
                else:
                    print("Formato de data inválido. Tente novamente.")
            while True:
                start = input("Data de inicio de funções na empresa, no formato dd/mm/yyyy: ")
                valido, data = validar_data(start)
                if valido:
                    break
                else:
                    print("Formato de data inválido. Tente novamente.")
                    
            job = input("Titulo: ")
            
            while True:
                try:
                    salary = int(input("Por favor, insira um número inteiro: "))
                    if salary > 0:
                        break
                    else:
                        print("O valor para o salário não pode ser zero. Tente novamente.")
                except ValueError:
                    print("O valor para o salário não é um número inteiro. Tente novamente.")
  
                        #registo = {"first_name": nome, "surname": sobrenome, "birthday": birth, "starting_date": start, "job_title": job,"salary":salary}
            df.loc[len(df.index)] = [nome, sobrenome, birth, start, job, salary]
            print(f"\n\n --- EMPREGADO {nome} {sobrenome} CRIADO COM SUCESSO ---\n\n")
            return df
            #fc.run(menu)
        else:
            print("Sobrenome não consta na lista de possibilidades.")
            #fc.run(menu)
    else:
        print("Nome não consta na lista de possibilidades.")
        #fc.run(menu)

def abrir_explorador():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Abre o Explorador de Ficheiros para selecionar um ficheiro CSV
    ficheiro = filedialog.askopenfilename(
        title="Selecionar ficheiro CSV",
        filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
    )
    return ficheiro
             
def load_batch_employees(df, nomes, sobrenomes):
    os.system('cls')
    print('2. Load batch employees (csv file)\n')    
    batch =  pd.read_csv(abrir_explorador(), index_col=None)
    try:
        num_row = int(batch.shape[0]) #vai-me dar o primeiro valor do tuplo, que é o numero de linhas
        #Testar se o ficheiro não está vazio, ou seja nº linhas == 0
        if num_row == 0:
            print("\n\n--- Ficheiro vazio ---\n\n")
            print("\n")
        else:
            #Testar se temos o mesmo numero de colunas em ambos os DF's
            df_num_col = int(df.shape[1])
            batch_num_col = int(batch.shape[1])
            if batch_num_col != df_num_col: #Testar o numnero de colunas é o mesmo em ambos os DF's
                print(f'O numero de colunas do ficheiro -- {batch} -- não corresponde ao numero de colunas do ficheiro original.')
            else:
                df_colo_names = df.columns.to_list()
                batch_col_names = batch.columns.to_list()
                if df_colo_names != batch_col_names:
                    print(f'\n\n O nome das colunas do ficheiro -- {batch} -- não correspondem ao nome das colunas do ficheiro original.\n\n')
                else:
                    for i in range(num_row):
                        print("--------")
                        nome = batch.at[i, "first_name"].upper() #aceder a cada linha index i, ao valor da coluna "fiest_name"
                        nome_cap = nome.capitalize() # Coloco já em Capitalize para depois adicionar ao DF original
                        if name_check(nome,nomes) == False:
                            print(f'\n\n ERRO: O nome {nome_cap} não é valido\n\n')
                        else:
                            sur = batch.at[i, "surname"].upper()
                            sur_cap = sur.capitalize()
                            if name_check(sur,sobrenomes) == False:
                                print(f'\n\nE RRO: O nome {sur_cap} não é valido\n\n')
                            else:
                                birth = batch.at[i, "birthday"]
                                if validar_data(birth) == (False, None):
                                    print(f'\n\n ERRO: O utilizador {nome_cap} {sur_cap}, não tem a birthday em formato correto. \n\n') 
                                else:    
                                    start = batch.at[i, "starting_date"]
                                    if validar_data(start) == (False, None):
                                        print(f'\n\n ERRO: O utilizador {nome_cap} {sur_cap}, não tem a starting_date em formato correto. \n\n')
                                    else:    
                                         df.loc[len(df.index)] = batch.loc[i]
                                         print(f'\n\n O utilizador {nome_cap} {sur_cap}, foi inserido com SUCESSO \n\n')
        return df
    except FileNotFoundError:
        print("\n\nNome do ficheiro errado, ou ficheiro não existente.\n\n")
        pass        
    
def change_record(df):
    os.system('cls')
    print('4. Change some record\n')
    while True:
        pesquisa = input("\n - [Escrever 'indice' - se sabe o indice do colaborador a editar] OU\n - [Escrever 'Nome do utilizador' - que pretende pesquisar?] OU\n - [Escrever '-1' - para voltar ao MENU PRINCIPAL]\n:  ").lower()
        if pesquisa == "-1":
            break
        elif pesquisa == "indice": #definir o INDEX que quero editar mas o valor do index tem de existir (TRY)
            index = int(input("Indicar o index do colaborador a editar: "))
            try: 
                col = input(" - Nome da coluna a editar, ou\n - Se pretende eliminar escreva 'eliminar'\n: ")
                if col == "eliminar":
                    df = df.drop(index, inplace=True)
                    return df
                elif col in df.columns.to_list():
                    valor_col = input("Novo valor: ")
                    if col == "first_name":
                        df.loc[index, col] = valor_col 
                        return df 
                    elif col == "surname":
                        df.loc[index, col] = valor_col 
                        return df
                    elif col == "birthday" or col == "starting_date":
                        while True:
                            valido, data = validar_data(valor_col)
                            if valido:
                                df.loc[index, col] = valor_col
                                break
                            else:
                                print("Formato de data inválido. Tente novamente com o formato dd/mm/yyyy.")
                                valor_col = input("Novo valor: ") 
                        return df  
                    elif col == "job-title" or col == "salary":
                        df.loc[index, col] = valor_col 
                        return df
                    else:
                        print("Novo valor, não é válido\n\n")
                        pass
                else:
                    print("Nome na coluna não existe.\n\n")                     
            except IndexError:
                print("O indice indicado não existe.\n\n")
                continue
        else: #pesquisa de nome para obter o index
            lista_pesquisa = pesquisa.split(" ")
            os.system('cls')
            try:
                nome_pesquisa_index = lista_pesquisa[0].lower().capitalize()
                sur_pesquisa_index = lista_pesquisa[1].lower().capitalize()
                df_filtrado = df[(df['first_name'] == nome_pesquisa_index) & (df['surname'] == sur_pesquisa_index)] 
                if len(df_filtrado) != 0:
                    print(f'\n Lista de empregados com o nome igual a {nome_pesquisa_index} {sur_pesquisa_index}:\n')
                    print(df_filtrado)
                else:
                    print("\nNome não existe nos registos\n")
                    continue
            except IndexError:
                df_filtrado = df[df['first_name'] == nome_pesquisa_index]
                if len(df_filtrado) != 0:
                    print(f'\n Lista de empregados com o nome igual a {nome_pesquisa_index}\n')
                    print(df_filtrado)
                else:
                    print(f'\nNenhum colaborador com o nome {nome_pesquisa_index}\n')
                    continue
     
def show_current_employees(df):
    os.system('cls')
    print("\n\n LISTA DE EMPREGADOS ATUAIS\n\n")
    print(f'{df}\n\n')
    pass

#Analise de IDADES
def idades(df):
    df2 = df.copy()
    df2['birthday'] = pd.to_datetime(df2['birthday'], format='%d/%m/%Y')
    hoje = datetime.now()
    df2['idade'] = (hoje - df2['birthday'])
    df2['idade'] = (df2['idade'] / np.timedelta64(1, 'D'))/365
    df2['idade'] = df2['idade'].astype(int)

    mais_idoso = df2['idade'].max()
    print(f'O empregado mais idoso tem: {mais_idoso} anos')

    mais_novo = df2['idade'].min()
    print(f'O empregado mais novo tem: {mais_novo} anos')

    media_idades =  df2['idade'].mean()
    print(f'A média de idades é de : {media_idades} anos')

#Analise de TEMPO de empresa
def tempo(df):
    df1 = df.copy()
    df1['starting_date'] = pd.to_datetime(df1['starting_date'], format='%d/%m/%Y')
    
    hoje = datetime.now()
    
    df1['tempo'] = (hoje - df1['starting_date'])
    df1['tempo'] = (df1['tempo'] / np.timedelta64(1, 'D'))/365
    df1['tempo'] = df1['tempo'].astype(int)

    mais_antigo = df1['tempo'].max()
    print(f'O empregado mais antigo da empresa tem {mais_antigo} anos de casa')

    mais_novo = df1['tempo'].min()
    print(f'O empregado mais antigo da empresa tem {mais_novo} anos de casa')

    media_tempo =  df1['tempo'].mean()
    print(f'A média de tempo de casa é: {media_tempo} anos')

    df1 = df1.sort_values(by='starting_date', ascending=True)

    df1['total_salarios'] = df1['salary'].cumsum()

    df_dataset = df1[['starting_date','total_salarios']]

    df_dataset.plot(x='starting_date', y='total_salarios')
    
    plt.show()
    
    plt.close('all')

def show_stats():
    os.system('cls')
    #Alterar o df onde inserimos a bd
    global empregados
    print('\nInformações gerais\n')
    #calcular o nº de funcionários
    print(f'\nO numero total de funcionários é de: {empregados.shape[0]}') 
    
    #calcular a média
    empregados['salary'] = empregados["salary"].astype(int)
    media_salary = empregados['salary'].mean()
    print(f'\nA média de salários é de: {media_salary}$')
    
    #calcular a soma
    soma_salary = empregados['salary'].sum()
    print(f'\nO total de salários é de: {soma_salary}$')      

    #Calcular ordenado minimo
    minimo_salary = empregados['salary'].min()
    print(f'\nO salário minimo é de: {minimo_salary}$')
    #Calcular ordenado máximo
    máximo_salary = empregados['salary'].max()
    print(f'\nO salário máximo é de: {máximo_salary}$')
    
    def menu_estatistica():
        print("\nPretende visualizar estatisticas especificas de:")
        print("1. IDADES")
        print("2. EVOLUÇÃO SALARIAL EMPRESA")
        print("3. Sair")
    
    while True:
        menu_estatistica()
        opcao = input("Escolha uma opção (1/2/3): ")
        if opcao == '1':
            idades(empregados)
        elif opcao == '2':
            tempo(empregados)
        elif opcao == '3':
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")  

def export_data():
    nome_excel = input("Qual o nome do ficheiro xls que quer guardar? ")
    empregados.to_excel(nome_excel+'.xlsx')
    pass

def exit_program():
    save = input("Quer guardar as alterações antes de sair? (S)im/(N)ão: ")
    if save == "S":
        empregados.to_csv("database_save.csv", index=False)
    print("Good Bye!")
    plt.close('all')
        
def mostrar_menu():
    print("---- MENU PRINCIPAL ----\n")
    print("1. Create new employee")
    print("2. Load batch employees (csv file)")
    print("3. Show current employees")
    print("4. Change some record")
    print("5. Show stats about current staff")
    print("6. Download data")
    print("-1. Exit")

def escolher_opcao():
    opcao = input("Escolha uma opção: ")
    return opcao

while True:
    mostrar_menu()
    opcao = escolher_opcao()
    if opcao == "1":
        create_new_employee(empregados, nomes, sobrenomes)
    elif opcao == "2":
        load_batch_employees(empregados, nomes, sobrenomes)
    elif opcao == "3":
        show_current_employees(empregados)
    elif opcao == "4":   
        change_record(empregados)
    elif opcao == "5":   
        show_stats()
    elif opcao == "6":   
        export_data()
    elif opcao == "-1":
        exit_program()
        break
    else:
        print("Opção inválida. Tente novamente.")

