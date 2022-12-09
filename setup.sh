wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
$HOME/miniconda/bin/conda init
$HOME/miniconda/bin/conda create -n web python pip flask tqdm -y
echo 'conda activate web && cd ~/src' >> ~/.bashrc
