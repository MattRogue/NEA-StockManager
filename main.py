#!C:/Users/mahth/Documents/RogueCodes/stock_manager/venv/Scripts/python.exe
from website import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
    #set host = 0.0.0.0 (public), 127.0.0.1:5000 (this pc)
    #you will need to open firewall for public host to work