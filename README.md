# Usage

<code>
when monero
</code>

# Installation
<code>bin/when</code> is a symlink to <code>src/when.py</code>. Adding <code>/bin</code> to PATH environment variable will "install" the script.

<code>git clone git@github.com:MrMebelMan/when.git</code>

<code>pip3 install -r requirements.txt</code>

<code>cd bin</code>

### sh
<code>
echo "export PATH=\$PATH:$(pwd)" >> ~/.profile
</code>

### bash
<code>
echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
</code>

### zsh
<code>
echo "export PATH=\$PATH:$(pwd)" >> ~/.zshrc
</code>

### fish
<code>
set -gx PATH $PATH (pwd)
</code>
