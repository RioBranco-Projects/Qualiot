# run.py

from app import create_app

app = create_app()

if __name__ == '__main__':
    """
    Ponto de entrada da aplicação.
    Executa o servidor Flask em modo de depuração.
    """
    app.run(debug=True)
