from flask import Flask,render_template,request,redirect,g,session,flash
import sqlite3

app = Flask(__name__)
app.secret_key="Senai"

def ligar_banco():
    banco = g._database = sqlite3.connect('Escola.db')
    cursor=banco.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return banco

@app.teardown_appcontext
def fechar_banco(exception):
    banco = ligar_banco()
    banco.close()

@app.route('/')
def home():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('Home.html',Titulo = "Gestão Escolar")

@app.route('/estudante')
def estudante():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('SELECT * FROM Estudantes;')
        Estudantes = cursor.fetchall()
        cursor.execute("SELECT id_turma, nome_turma FROM turma;")
        turmas = cursor.fetchall()
        return render_template('Estudante.html', ListaEstudantes =Estudantes,listaturmas=turmas, Titulo = "Cadastro de Estudantes" )

@app.route('/cadastro')
def cadastro():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("SELECT id_turma, nome_turma FROM turma;")
        turmas = cursor.fetchall()
        return render_template('Cadastro.html',Titulo='Cadastro de Estudante', listaturmas=turmas)

@app.route('/criar', methods=['POST','GET'])
def criar():
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        rm = request.form['RM']
        nome = request.form['nome']
        dataNascimento = request.form['datanas']
        genero = request.form['genero']
        endereco = request.form['endereco']
        email = request.form['email']
        telefone = request.form['telefone']
        curso = request.form['curso']
        turma = request.form['turma']
        cursor.execute('INSERT INTO Estudantes'
                   '(RM,Nome,DataNascimento,Genero,Endereço,Email,Telefone,Curso,id_turma) '
                   'VALUES (?,?,?,?,?,?,?,?,?);',
                   (rm,nome, dataNascimento, genero,endereco, email, telefone, curso,turma))
        banco.commit()
    except:
        banco.rollback()
    return redirect('/')

@app.route('/excluir/<rm>', methods=['GET', 'DELETE'])
def deletar(rm):
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        try:
            cursor.execute('DELETE FROM Estudantes WHERE RM=?;', (rm,))
            banco.commit()
        except:
            banco.rollback()
        return redirect('/estudante')

@app.route('/editar/<rm>', methods =['GET'])
def editar(rm):
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        banco = ligar_banco()
        cursor = banco.cursor()
        try:
            cursor.execute('SELECT * FROM Estudantes WHERE RM=?;', (rm,))
            encontrado = cursor.fetchone()
            cursor.execute("SELECT id_turma, nome_turma FROM turma;")
            turmas = cursor.fetchall()
            return render_template('Editar.html', Estudante=encontrado, listaturmas = turmas, Titulo = "Editar Estudante")
        except:
            banco.rollback()
            return redirect('/estudante')

@app.route('/alterar', methods=["PUT", "POST"])
def alterar():
        rm = request.form['RM']
        nome = request.form['nome']
        data = request.form['datanas']
        genero = request.form['genero']
        endereco = request.form['endereco']
        email= request.form['email']
        telefone = request.form['telefone']
        curso = request.form['curso']
        banco = ligar_banco()
        turma = request.form['turma']
        cursor = banco.cursor()
        try:
            cursor.execute('UPDATE Estudantes SET Nome=?,DataNascimento=?,'
                           'Genero=?,Endereço=?,Email=?,Telefone=?,Curso=?, id_turma=? WHERE RM=?;',
                           (nome,data,genero,endereco,email,telefone,curso,turma,rm))
            banco.commit()
            return redirect('/estudante')
        except:
            banco.rollback()
            return redirect('/estudante')

@app.route('/login')
def login():
    return render_template('Login.html', Titulo = "Faça seu Login")

@app.route('/autenticar', methods =["POST"])
def autenticar():
    if request.form['usuario']=='Bruno' and request.form['senha']=='123':
        session['Usuario_Logado']=request.form['usuario']
        flash('Usuario Logado')
        return redirect('/')
    else:
        flash('Usuario não encontrado')
        return redirect('/login')

@app.route('/deslogar')
def deslogar():
    session.clear()
    return redirect('/login')

@app.route('/cadastro-turma')
def cadturma():
    if 'Usuario_Logado' not in session:
        return redirect('/login')
    else:
        return render_template('CadastroTurma.html', Titulo="Casdastro de Turma")

@app.route('/criarturma', methods=['POST','GET'])
def criarturma():
    banco = ligar_banco()
    cursor = banco.cursor()
    nome_turma = request.form['nome_turma']
    ano_letivo = request.form['ano_letivo']
    quantidade_alunos = request.form['quantidade_alunos']
    sala = request.form['sala']
    periodo = request.form['periodo']
    try:
        cursor.execute('INSERT INTO Turma'
                       '(nome_turma,ano_letivo,quantidade_alunos,sala,periodo) '
                       'VALUES (?,?,?,?,?);',
                       (nome_turma,ano_letivo,quantidade_alunos,sala,periodo))
        banco.commit()
    except:
        banco.rollback()
    return redirect('/')


if __name__ == '__main__':
    app.run()
