🛠️ 1. Instale dependências no WSL (Ubuntu, por exemplo)
Abra o terminal do WSL e rode:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev git
```

🧬 2. Instale o pyenv
Execute:

```bash
curl https://pyenv.run | bash
```

⚙️ 3. Configure o ambiente
Adicione estas linhas ao final do seu `~/.bashrc` (ou ~/.zshrc se usar Zsh):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Depois, recarregue o terminal:

```bash
exec "$SHELL"
```


🐍 4. Instale versões do Python
Veja as disponíveis:

```bash
pyenv install --list
```

Instale uma versão específica (exemplo: 3.11.4):

```bash
pyenv install 3.11.4
```

Defina como padrão global ou local:

```bash
bash
pyenv global 3.11.4
# ou
pyenv local 3.11.4
```

✅ 5. Verifique
```bash
python --version
```
Se aparecer Python 3.11.4, tá tudo certo!


# Terminal Pular linha

✅ 1. Fazer o terminal pular linha quando o nome for muito grande
```bash
nano ~/.bashrc
```

✅ 2. Encurtar o nome exibido no prompt
```bash
PS1='\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\n\[\e[0m\]\$ '
```

✅ 3. Usar um prompt customizado com cores e quebra de linha
```bash
source ~/.bashrc
```