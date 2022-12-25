# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "starboard/ubuntu-arm64-20.04.5"
  config.vm.box_version = "20221120.20.40.0"
  config.vm.box_download_insecure = true
  config.vm.provider "vmware_desktop" do |v|
      v.ssh_info_public = true
      v.gui = true 
      v.linked_clone = false
      v.vmx["ethernet0.virtualdev"] = "vmxnet3"
  end

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
end
