wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
git clone https://github.com/johan456789/md5-cracker/ && cd src
conda create -n web python pip -y
conda init && exec bash
echo 'conda activate web && cd ~/src' >> ~/.bashrc
conda activate web
pip install -r requirements.txt
