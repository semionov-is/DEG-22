- name: "Homework Playbook"
  hosts: all
  become: true
  tasks:
	- name: "Check connectivity (ping)"
  	ping:

	- name: "Install required packages"
  	package:
    	name: "{{ item }}"
    	state: present
  	with_items:
    	- net-tools
    	- git
    	- tree
    	- htop
    	- mc
    	- vim

	- name: "Update packages"
  	ansible.builtin.apk:
    	update_cache: yes
    	upgrade: yes

	- name: "Copy the text file"
  	copy:
    	src: /home/debuser/mlops/hw03/test.txt
    	dest: /home/ansible/test.txt

	- name: "Create user groups and home directories"
  	group:
    	name: "{{ item }}"
    	state: present
  	with_items:
    	- devops_1
    	- test_1
  	loop_control:
    	label: "{{ item }}_loop"

	- name: "Create home users"
  	user:
    	name: "{{ item }}"
    	group: "{{ item }}"
    	home: "/home/{{ item }}"
    	state: present
  	with_items:
    	- devops_1
    	- test_1
