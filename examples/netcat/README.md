# ‘netcat’ Demo

This example uses [Ansible](http://docs.ansible.com/)
to set up a very simple service based on ``netcat``.
It demonstrates the basic mechanics of setting up a runtime environment using *Bootils*,
without any complexity whatsoever introduced by the service that is launched.


## Basic Installation

On *Trusty* and *Wheezy*, use this to install necessary requirements:

```sh
apt-get install ansible sshpass
```

Other platforms should have similar packages.


## Running the Playbook

To execute the playbook, call the following command
which will set up a sample configuration on localhost in ``/etc/bootils/netcat-demo``.

```sh
/usr/bin/ansible-playbook --ask-sudo-pass -i hosts-example site.yml
```


## Testing the Service

**TODO**
