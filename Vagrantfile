# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "discourse2fedmsg" do |discourse2fedmsg|
    discourse2fedmsg.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/34/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-34-1.2.x86_64.vagrant-libvirt.box"
    discourse2fedmsg.vm.box = "f34-cloud-libvirt"
    discourse2fedmsg.vm.hostname = "discourse2fedmsg.test"

    discourse2fedmsg.vm.synced_folder '.', '/vagrant', disabled: true
    discourse2fedmsg.vm.synced_folder ".", "/home/vagrant/discourse2fedmsg", type: "sshfs"


    discourse2fedmsg.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048 
    end

    discourse2fedmsg.vm.provision "ansible" do |ansible|
      ansible.playbook = "devel/ansible/playbook.yml"
      ansible.config_file = "devel/ansible/ansible.cfg"
      ansible.verbose = true
    end
  end

end
