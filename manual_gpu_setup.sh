# SSH into server
ssh root@<server-ip>

# 1. Update packages
sudo apt update && sudo apt upgrade -y

# 2. Install build tools
sudo apt install -y build-essential curl git

# 3. Install NVIDIA driver (for RTX 4090)
sudo apt install -y nvidia-driver-535
sudo reboot

# 4. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 5. Add NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install -y nvidia-docker2
sudo systemctl restart docker

# 6. Test GPU access in Docker
sudo docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi