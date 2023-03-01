# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hajowieland/ubuntu-jammy-arm"
  config.vm.box_version = "1.0.0"
  config.vm.provider "vmware_desktop" do |v|
      v.ssh_info_public = true
      v.gui = true 
      v.linked_clone = false
      v.vmx["ethernet0.virtualdev"] = "vmxnet3"
  end

  ## Basic setup
  config.vm.provision "shell", inline: <<-SHELL
    echo "sudo su -" >> .bashrc
  SHELL

  ## Install terminfo
  config.vm.provision "shell", inline: <<-SHELL
    apt-get -yqq update && apt-get install -yqq kitty-terminfo
  SHELL

  ## Install bash utils
  config.vm.provision "shell", inline: <<-SHELL
    apt-get -yqq update && apt-get install -yqq binutils pv
  SHELL

  ## Install golang
  config.vm.provision "shell", inline: <<-SHELL
    curl -sLO https://dl.google.com/go/go1.19.4.linux-arm64.tar.gz
    tar -C /usr/local -xzf go1.19.4.linux-arm64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' > /etc/profile.d/golang.sh
  SHELL

  ## Install ebpf related
  config.vm.provision "shell", inline: <<-SHELL
    apt-get -yqq update && apt-get install -yqq bpftrace
  SHELL

  ## Install reptyr
  config.vm.provision "shell", inline: <<-SHELL
    apt-get -yqq update && apt-get install -yqq linux-headers-$(uname -r) bison build-essential cmake flex g++ git libelf-dev zlib1g-dev libfl-dev systemtap-sdt-dev binutils-dev arping netperf iperf3 python3-distutils make
    git clone --depth=1 https://github.com/nelhage/reptyr.git
    cd reptyr
    make install 
    echo 0 > /proc/sys/kernel/yama/ptrace_scope
  SHELL
end
