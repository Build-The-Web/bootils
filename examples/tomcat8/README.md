# Tomcat8 Web Server

This shows how to launch a *Tomcat8* servlet container with the help of *runit* and *Bootils*.
It should run unmodified on any recent Debian-like Linux,
and on any other system with a few modifications.
It expects that the
[opt-tomcat8](https://github.com/jhermann/priscilla/tree/master/tomcat8)
package is available (or already installed).


## Basic Installation

On *Trusty* and *Wheezy*, use this to install necessary requirements:

```sh
apt-get install ansible sshpass
```

Other versions and platforms should have the same or similar packages.


## Running the Playbook

To execute the playbook, call the following command
which will set up a sample configuration on localhost.

```sh
/usr/bin/ansible-playbook --ask-sudo-pass -i hosts-example site.yml
```


## Testing the Service

**TODO**
