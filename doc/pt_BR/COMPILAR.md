# Compilar no Linux em um clique

1. Instale as dependências do Luanti/AstraLua usando o gerenciador de pacotes da sua distribuição. No Ubuntu/Debian, instale pelo menos `cmake`, `g++`, `ninja-build`, `libirrlicht-dev`, `libsqlite3-dev`, `libjsoncpp-dev`, `libluajit-5.1-dev`, `libcurl4-gnutls-dev`, `libopenal-dev`, `libfreetype6-dev`, `libpng-dev`, `libjpeg-dev`, `libxxf86vm-dev`, `libgl1-mesa-dev`, `libgles2-mesa-dev`, `zlib1g-dev` e `gettext`.
2. Na pasta raiz do projeto, dê duplo clique em `compilar-astralua.sh` e escolha **Executar**. Pelo terminal, use `./compilar-astralua.sh`.
3. O script cria somente `build-linux/`, compila em modo Release e executa os testes unitários. O executável final aparece em `bin/`.

A compilação é local e não inicia nenhum workflow ou serviço externo. A pasta de dados segue o comportamento padrão do Luanti; `ASTRALUA_USER_PATH` pode ser usado apenas quando for necessário isolar um teste.
