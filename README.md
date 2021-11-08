# discourse2fedmsg

discourse2fedmsg is a small flask web application that takes webhook POST requests from Discourse instances, and relays those messages to Fedora Messaging

## development environment

discourse2fedora has a full development environment that is managed by Vagrant.  Vagrant allows contributors to get quickly up and running with a discourse2fedmsg development environment by automatically configuring a virtual machine. To get started, first install the Vagrant and Virtualization packages needed, and start the libvirt service:

```
$ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager
$ sudo systemctl enable libvirtd
$ sudo systemctl start libvirtd
```

Check out the code and run vagrant up:

```
$ git clone https://github.com/fedora-infra/discourse2fedmsg
$ cd discourse2fedmsg
$ vagrant up
```

### final setup

After the machine is fully provisioned, there are two extra steps that you need to manually do:

1. Go to mailcatcher at http://discourse2fedmsg.test:1080 . Mailcatcher is set up to capture and show you all the outgoing email from the discourse instance. In there there is an email about an admin account. Follow that link (changing the port from 3000 to 4200 in the link) to set the admin password for the discourse instance

2. you will need to set up the webhook in the discourse settings UI -- first log in with the admin account, and set the webhook URL to http://discourse2fedmsg:5000/webhook and set the secret to `CHANGEMECHANGEME`


### available tools and services

* http://discourse2fedmsg.test:1080 -- **mail catcher** -- all outgoing mail from the discourse instance is captured here
* http://discourse2fedmsg.test:4200 -- **discourse** -- the discourse instance
* http://discourse2fedmsg.test:5000 -- **discourse2fedmsg** -- the discourse2fedmsg flask application itself
