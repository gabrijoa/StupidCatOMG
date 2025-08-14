# StupidCatOMG
😻😻😻

Projeto Gato Idiota - Bot Serverless no Telegram
E aí, tudo bem? Este é o repositório com o código-fonte completo do artigo "Criando um ChatBot Serverless na nuvem: Um guia Rápido sobre AWS, Python e Telegram".

O artigo principal foca no "porquê" e no passo a passo da arquitetura na nuvem. Este README foca na parte prática: como rodar e empacotar este projeto na sua máquina local.

Por que Poetry?
Você deve ter notado que eu uso o Poetry para este projeto. O motivo é simples: organização e isolamento.

O Poetry cria um ambiente virtual exclusivo para o nosso bot. Isso garante que as versões das bibliotecas que usamos (como a requests) não entrem em conflito com nenhum outro projeto Python que você tenha na sua máquina. É uma forma limpa e profissional de gerenciar dependências, garantindo que o projeto funcione hoje e sempre.

Configurando o Ambiente Local
Para rodar e modificar o projeto, siga estes passos:

Clone o Repositório:

Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd nome-do-repositorio
Instale as Dependências:
Com o Poetry já instalado na sua máquina, rode o comando abaixo. Ele vai ler o arquivo pyproject.toml e instalar tudo o que o projeto precisa.

Bash

poetry install
Empacotando para o Lambda (O Pulo do Gato)
O AWS Lambda precisa de um arquivo .zip com uma estrutura específica (sem pastas-pai desnecessárias). O processo para criar esse pacote é um pouco diferente dependendo do seu sistema operacional.

Para Linux e macOS
No terminal, siga esta sequência de comandos a partir da raiz do projeto:

Bash

# 1. Cria uma pasta temporária para o pacote
mkdir package

# 2. Exporta a lista de dependências para um arquivo requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes

# 3. Instala as dependências DENTRO da pasta 'package'
pip install -r requirements.txt --target ./package

# 4. Copia o seu código-fonte para dentro da pasta 'package'
cp -r src/* ./package/

# 5. Navega para dentro da pasta 'package' e cria o .zip
cd package
zip -r ../deployment_package.zip .
cd ..
Ao final, você terá o arquivo deployment_package.zip pronto para o upload!

Para Windows
O racional é o mesmo, mas os comandos e ações são um pouco diferentes.

Instale as Dependências na Pasta package:
Abra o seu terminal (CMD ou PowerShell) na raiz do projeto e execute os mesmos comandos de instalação:

PowerShell

# Crie a pasta 'package' pela interface gráfica ou com o comando 'mkdir package'
mkdir package

# Exporte os requerimentos
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Instale os pacotes no diretório 'package'
pip install -r requirements.txt --target ./package
Copie o seu Código:
Pela interface gráfica (Windows Explorer), copie o conteúdo da sua pasta src (o arquivo lambda_function.py) e cole dentro da pasta package.

Crie o Arquivo .zip:
Como conversamos, a forma mais segura é pela interface gráfica para não errar a estrutura:

Abra a pasta package.

Selecione todos os arquivos e pastas lá dentro (Ctrl + A).

Clique com o botão direito sobre a seleção, vá em "Enviar para" e escolha "Pasta compactada (.zip)".

Renomeie o arquivo gerado para deployment_package.zip.

Agora é com você! Com o código na sua máquina e o pacote .zip gerado, você pode fazer as alterações que quiser e subir para o Lambda.

Explore, modifique e, o mais importante: SE DIVIRTA >)