Esse tutorial é exclusivo para instalação em linux. Caso deseje instalar no windows procure tutoriais ensinando a instalar o mysql, o python, o glade e o pygtk.

1- Instale o mysql digitando no terminal:
sudo apt-get install mysql-server

2- Durante a instalação vai ser solicitado uma senha de root. Digite qualquer uma. Ela vai ser necessário depois, não esqueça dela!

3- Instale o glade digitando no terminal:
sudo apt-get install glade

4- Baixe os arquivos.

5- Na pasta img troque a imagem logoEmpresa pelo logo de sua empresa e deixe com esse nome. A imagem tem que ser em png!

6- Abra o arquivo bd em qualuer editor de texto e altere self.senha colocando a senha de root que foi cadastrado quando instalou o mysql.

7- Abra o terminal vá até a pasta banco que foi baixada junto com o código.

8- Ainda no terminal digite:
mysql -u root -p < sqlOS.sql

9- Digite a senha de root do mysql

Seu computador agora está configurado para rodar o sistema.

Pelo terminal vá até a pasta src baixada junto com o programa e digite:
python Gerenciador\_de\_OS.py

Pronto o programa deverá rodar.