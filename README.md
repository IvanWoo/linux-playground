## setup

register a free personal use license for VMware Fusion Player 13 at [here](https://customerconnect.vmware.com/evalcenter?p=fusion-player-personal-13)

install required binaries via brew

```sh
brew install --cask vmware-fusion
brew install vagrant
brew install --cask vagrant-vmware-utility
```

install the provider for vagrant

```sh
vagrant plugin install vagrant-vmware-desktop
```

access the machine

```sh
vagrant up
vagrant ssh
```

halt the machine

```sh
vagrant halt
```

reset the machine

```sh
vagrant destroy
```

## ref

- [Vagrant and VMWare Fusion 13 Player on Apple M1 Pro](https://gist.github.com/sbailliez/2305d831ebcf56094fd432a8717bed93)
