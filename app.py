
# Importação dos módulos e bibliotecas.
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import resources.database_connection as database_connection
from werkzeug.security import generate_password_hash, check_password_hash


# Configuração do aplicativo da web.
app = Flask(__name__)

# Definição de uma chave de renderização.
app.config['SECRET_KEY'] = 'PEO'

# Definição da rota para a página inicial. rota = url
#se o usuário colocar uma barra vazia ele renderiza a página inicial
@app.route('/')
def inicio():

    return render_template('index.html')

# Rota para o LOGIN do website.
@app.route('/login', methods=['POST', 'GET'])
def login():

    # Recupera as informações do formulário de login.
    email = request.form.get('email')
    senha = request.form.get('senha')

    # Faz a conexão com o banco de dados
    connection = database_connection.open_connection()
    cursor = connection.cursor()

    # Seleciona no banco de dados o usuário com as informações inseridas.
    query = "SELECT * FROM funcionarios WHERE email = %s AND senha = %s;"
    values = (email, senha)

    # Executa a consulta e gravar o retorno em um vetor.
    cursor.execute(query, values)
    user = cursor.fetchone()

    # Encerra a conexão com o banco de dados.
    cursor.close()
    connection.close()

    # Verifica se o vetor retornado do banco de dados existe.
    # Caso ele exista, significa que as informações de login estavam corretas.
    # Caso não existe, significa que as informações de login estavam incorretas.
    if user:

        # Redireciona o usuário para a tela privada principal.
        return render_template('tela-inicial.html')
    else:
        
        # Redireciona o usuário para a tela de login, de volta.
        return render_template('index.html')
    
# rota que cadastra os funcionarios
@app.route('/cadastrar-funcionarios', methods=['GET', 'POST'])
def cadastrar_funcionarios ():

    # Verifica se o método da requisição é o POST.
    if (request.method == 'POST'):

        # Recebe os dados do formulário via POST.
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        data_nascimento = request.form['data_nascimento']
        endereco = request.form['endereco']
        numero = request.form['numero']
        cargo = request.form['cargo']
        senha = request.form['senha']
        pergunta1 = request.form['pergunta1']
        pergunta2 = request.form['pergunta2']
        pergunta3 = request.form['pergunta3']

        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Monta a instrução SQL e insere os dados no banco de dados.
        SQL = "INSERT INTO funcionarios (nome, email, cpf, data_nascimento, endereco, numero, cargo, senha, pergunta1, pergunta2, pergunta3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        values = (nome, email, cpf, data_nascimento, endereco, numero, cargo, senha, pergunta1, pergunta2, pergunta3)
        cursor.execute(SQL, values)
        connection.commit()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a página de login
        return render_template('index.html')
    else:

        # Redireciona para a página de cadastro de funcionarios.
        return render_template('cadastro-funcionario.html')
    
# Rota de cadastro dos dados dos pacientes
@app.route('/cadastrar-pacientes', methods=['GET', 'POST'])
def cadastrar_pacientes ():

    # Verifica se o método da requisição é o POST.
    if (request.method == 'POST'):

        # Recebe os dados do formulário via POST.
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento']
        contato_emergencia = request.form['contato_emergencia']
        cpf = request.form['cpf']
        carteirinha_sus = request.form['carteirinha_sus']

        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Monta a instrução SQL e insere os dados no banco de dados.
        SQL = "INSERT INTO pacientes (nome, endereco, telefone, data_nascimento, contato_emergencia, cpf, carteirinha_sus) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        values = (nome, endereco, telefone, data_nascimento, contato_emergencia, cpf, carteirinha_sus)
        cursor.execute(SQL, values)
        connection.commit()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a tela inicial
        return render_template('tela-inicial.html')
    else:

        # Redireciona para a tela de cadastro de pacientes.
        return render_template('cadastrar-pacientes.html')
    
# Rota que cadastra as informações da pré-consulta
@app.route('/pre-consulta', methods=['GET', 'POST'])
def pre_consulta():
    if request.method == 'POST':

        # Recebe os dados do formulário via POST.
        id_paciente = request.form.get('paciente')
        data_triagem = request.form.get('data_triagem')

        # Recebe os sintomas selecionados como uma lista e os transforma em uma string separada por vírgulas
        sintomas = request.form.getlist('sintomas')
        sintomas = ', '.join(sintomas)

        intensidade_sintomas = request.form.get('intensidade_sintomas')
        fatores_sintomas = request.form.get('fatores_sintomas')
        informacoes_sintomas = request.form.get('informacoes_sintomas')
        doencas_preexistentes = request.form.get('doencas_preexistentes')
        condicoes_cronicas = request.form.get('condicoes_cronicas')
        historico_cirurgico = request.form.get('historico_cirurgico')
        alergias = request.form.get('alergias')
        uso_medicamentos = request.form.get('uso_medicamento')
        doencas_hereditarias = request.form.get('doencas_hereditarias')
        condicoes_saude = request.form.get('condicoes_saude')

        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Monta a instrução SQL e insere os dados no banco de dados.
        SQL = """INSERT INTO pre_consulta (id_paciente, data_triagem, sintomas, intensidade_sintomas, 
                  fatores_sintomas, informacoes_sintomas, doencas_preexistentes, condicoes_cronicas, 
                  historico_cirurgico, alergias, uso_medicamentos, doencas_hereditarias, condicoes_saude) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        values = (id_paciente, data_triagem, sintomas, intensidade_sintomas, fatores_sintomas, 
                  informacoes_sintomas, doencas_preexistentes, condicoes_cronicas, historico_cirurgico, 
                  alergias, uso_medicamentos, doencas_hereditarias, condicoes_saude)
        cursor.execute(SQL, values)
        connection.commit()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a tela inicial.
        return render_template('tela-inicial.html')
    else:

        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Consulta SQL para pegar os pacientes ativas no banco de dados.
        query = "SELECT id_paciente, nome FROM pacientes WHERE ativo = 1;"
        cursor.execute(query)

        # Grava os resultados do SQL em uma tupla (vetor).
        pacientes = cursor.fetchall()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Rendereiza o template em HTML junto com os dados das categorias.
        return render_template('pre-consulta.html', pacientes=pacientes)    

# rota para a tela de recuperação de senha
@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha ():

    # Verifica se o método da requisição é o POST.
    if (request.method == 'POST'):

        # Recebe os dados do formulário via POST.
        pergunta1 = request.form['pergunta1']
        pergunta2 = request.form['pergunta2']
        pergunta3 = request.form['pergunta3']


        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()
        
        # Recupera as respostas das três perguntas do funcionario.

        # Compara se as três perguntas estão corretas.

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a tela de login
        return render_template('index.html')
    else:

        # Redireciona para a tela de recuperar senha
        return render_template('recuperar-senha.html')
    
#@app.route('/abrir-ficha', methods=['POST'])
@app.route('/abrir-ficha/<string:cpf>', methods=['GET','POST'])
def abrir_ficha(cpf=None):
    try:
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Se for uma requisição POST, obtém o CPF do formulário
        if request.method == 'POST':
            cpf = request.form.get('cpf')
        
        # Validação do CPF
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            return jsonify({"error": "CPF inválido"}), 400

        # Monta a instrução SQL
        SQL = "SELECT * FROM pacientes WHERE cpf = %s"
        values = (cpf,)
        cursor.execute(SQL, values)

        # Obtém os resultados
        paciente = cursor.fetchone()

        if paciente:
            paciente_dict = {
                "cpf": paciente[0],
                "nome": paciente[1],
                "data_nascimento": paciente[2],
                "endereco": paciente[3],
                # Adicione os outros campos conforme o necessário
            }
            return jsonify(paciente_dict), 200
        else:
            return jsonify({"error": "Paciente não encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/redefinir-senha', methods=['POST', 'GET'])
def redefinir_senha():

    # Verificar se o método de requisição é POST ou GET.
    if (request.method == 'POST'):

        # Recebe os dados do formulário via POST.
        cpf = request.form['cpf']
        pergunta1 = request.form['pergunta1']
        pergunta2 = request.form['pergunta2']
        pergunta3 = request.form['pergunta3']
        senha = request.form['senha']
        confirmarsenha = request.form['confirmarsenha']

        # Faz a conexão com o banco de dados.
        connection = database_connection.open_connection()
        cursor = connection.cursor()

        # Monta a instrução SQL para atualização dos dados do livro.
        SQL = "UPDATE funcionarios SET senha = %s WHERE cpf = %s AND pergunta1 = %s AND pergunta2 = %s AND pergunta3 = %s;"
        values = (senha, cpf, pergunta1, pergunta2, pergunta3)
        cursor.execute(SQL, values)
        connection.commit()

        print(SQL)

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a página de leitores novamente.
        return redirect(url_for('login'))
    
    else: 

        # Redireciona para a tela de edição da senha.   
        return render_template('redefinir-senha.html')
    


@app.route('/sobre')
def sobre():

    # Retorna a página HTML com os dados dos livros.
    return render_template('sobre.html')

@app.route('/tela-inicial')
def tela_inicial():

    return render_template('tela-inicial.html')




#não trazer para cima, tem que ficar por ultimo veyrrrr
# Executa o aplicativo da web.
if __name__ == '__main__':
    app.run(debug=True)