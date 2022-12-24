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

  ## Install golang
  config.vm.provision "shell", inline: <<-SHELL
    snap install go --classic
  SHELL

  ## Install ebpf related
  config.vm.provision "shell", inline: <<-SHELL
    apt-get -yqq update && apt-get install -yqq bpftrace
  SHELL
end
