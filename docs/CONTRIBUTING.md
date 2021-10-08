# Contributing

> You can contribute at will, you will always be welcome. But we have some rules to be followed so that everyone is well received by everyone and that everyone can contribute in a happy way.

## Add/Update Features

You looked the application and thought of some feature that should be added to the project ?

**_So you have two steps to follow:_**

- [Open an issue detailing your idea](#creating-an-issue)
- [You implement the functionality yourself](#contribute-to-implementation)

## Creating an issue

On the [project](https://github.com/richecr/duck-orm) page, you can click on the `Issues` button and a `new issue` button will appear on the page, then just select and follow the following steps:

- Select the type of your issue: `Bug, Feature or Discussion`.
- Give your issue a good name.
- Detail very well about the purpose of the issue.
- Images if possible.
- Finaly, click on `Submit new issue`.

## Clone the repository

On the home page of the [repository](https://github.com/richecr/duck-orm) there is a `Fork` button. When you click, just wait to complete the fork. And then it will create the repository in your account. And now just clone in your machine, this:

```sh
git clone https://github.com/<nome_de_usuario>/duck-orm
```

When finished, you will have the repository on your computer and then just open in your preferred editor and make your changes.

Before you should create your branch for your development.

You must create your branch from the `develop` branch:

```sh
git checkout -b <nome_branch>
```

For the name of the branch use the number of the issue to facilitate, ex: `issue_17`.

And now can begin the development.

When you have finished make your changes, you should commit your changes, but first:

```sh
git add .
```

The above command will prepare all modified files to be committed, going through all the changes that were made by you where you will decide if the change will be added(you must be inside the project folder to use the command). Now just commit the changes:


```sh
git commit -m "<Sua_Mensagem>"
```

Remember to use message clear. If what you're solving already has an issue open, reference issue in commit.
Ex: `git commit -m "#17 - Add contributing.md"`

And finally, you will submit the changes to the remote repository:

```sh
git push --set-upstream origin <nome_branch>
```

This is only the first time that submit a new branch to the remote repository, next times, just:


```sh
git push
```

But that will only in your fork, the official repository will not have its changes now what ?

Calm down, now that the `Pull Request` or `PR` to branch `develop`.

## Contribute to implementation:

After having forked and clone the project, chosen your favorite text editor. Now it's time to code.

But calm there, first of all, you should **choose an issue** you want to work with. If the issue is about functionality does not exist, you should create and say you're working on it, case it exists, you must say that you intend to work on the issue. And after done that, now yes are you ready to **code**.

### Understanding folders:

The project code can be found in the folder `duck_orm`, we are accepting library name hints as well..

- In the folder `duck_orm/utils`: Possui os arquivos que possuem funções que podem ser usadas por todo o projeto.

- In the folder `docs`: Possui os arquivos de documentação da biblioteca.

- In the folder `duck_orm/sql`: Possui todos os arquivos sobre as funcionalidades relacionadas com SQL, seja do Postgres e/ou SQLite.

    - In the folder `./postgres`: Possui a classe QueryPostgres que herda de QueryExecutor, onde é responsável por gerar todos os códigos SQL que irão funcionar no Postgres. Se algum SQL for diferente para o banco, então basta sobrescrever a função e então retornar o SQL suportado.
    - In the folder `./sqlite`:  Possui a classe QuerySQLite que herda de QueryExecutor, onde é responsável por gerar todos os códigos SQL que irão funcionar no SQLite. Se algum SQL for diferente para o banco, então basta sobrescrever a função e então retornar o SQL suportado.
    - In the file `./condition.py`: Possui a classe que é usada para adicionar filtros nas consultas do DuckORM.
    - In the file `./fields.py`: Possui todas as classes que representam os tipos que são suportados pelo DuckORM e que fazem o tratamento para os tipos SQL.
    - In the file `./operator.py`: Possui a classe que é usada para adicionar validar os operatores condicionais, usados pela classe `Condition`.
    - In the file `./relationship.py`: Possui todas as classes que representam os tipos de relacionamentos que são suportados pelo DuckORM e que fazem o tratamento para os relacionamentos para SQL. 
    - In the file `./sql.py`: Possui a classe QueryExecutor, na qual todos as classes Query{nome_banco} herdam. É aqui onde é montado todos os comandos SQL e caso um SQL seja diferentes entre os bancos suportados, basta sobrescrever o método na classe Query{nome_banco}. 

- In the file `./exceptions.py`: Possui todas as exceções usadas no DuckORM.

- In the file `./model.py`: Principal arquivo, é aqui onde toda a mágica acontece. Todos os métodos que podem ser usados por um modelo estão nesse aquivo.

### How to run the application:

We use [poetry](https://python-poetry.org/docs/) for easier dependency management.
So you need to install it:

- Install poetry: To install you can follow the steps of their own documentation [here](https://python-poetry.org/docs/#installation)

Now you should create virtualenv:

```bash
poetry shell
```

This will create a virtualenv for this project.

Now you need to install the dependencies:

```bash
poetry install
```

- You are now ready to implement your functionality/fix.

### Run the tests:

```bash
pytest .
```

### Entering the standards:

We chose to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard. To do this, install the [Python extension for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python). Another solution is to use pycodestyle.

#### Pycodestyle:

You can install pycodestyle with the command:

```bash
poetry add pycodestyle
```

- To run pycodestyle:

```bash
pycodestyle .
```

## Performing a Pull Request - PR

On your fork page a yellow message will appear asking you to make a Pull Request to the original repository. Clicking will open a page for you to fill in your PR information.

- Reference the issue you are working on using `#<numero_da_issue>`.

- Open your PR for the `develop` branch.

- Describe your modifications.

- Wait for your PR evaluation, and it may happen that we ask for some changes to be made.