create database GerenciadorOS;
use GerenciadorOS;
create table funcionario(id int unsigned not null auto_increment,
	nome varchar(30) not null,
	login varchar(20) not null,
	senha varchar(15) not null,
	documento varchar(25) not null,
	tipo_documento varchar(20),
	telefone varchar(12),
	ddd varchar(5),
	email varchar(30),
	cep varchar(12),
	nascimento date,
	cargo varchar(30),
	endereco varchar(150),
	foto blob,
	administrador int,
	primary key (id));

create table servico(id int unsigned not null auto_increment,
	nome varchar(40),
	descricao varchar(1500),
	primary key (id));

create table os(id int unsigned not null auto_increment,
	obs varchar(1000),
	cliente_id int,
	funcionario_id int,
	scaner varchar(200),
	pasta varchar(30),
	alterada int,
	foreign key(cliente_id) references cliente(id),
	foreign key(funcionario_id) references funcionario(id),
	primary key (id));

create table os_servico(servico_id int,
	foreign key(servico_id) references servico(id),
	os_id int,
	foreign key(os_id) references os(id));

create table cliente( id int unsigned not null auto_increment,
	nome varchar(50),
	documento varchar(20),
	tipo_documento varchar(10),
	email varchar(30),
	telefone1 varchar(12),
	ddd varchar(5),
	endereco varchar(150),
	foto blob,
	primary key (id));
