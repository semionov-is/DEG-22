---
- name: "Homework Playbook"
  hosts: 
    - netology-ml
  become: true
  tasks:
    - name: "Check SSH connectivity"
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

    - name: "Update all packages"
      package:
        name: "*"
        state: latest

    - name: "Copy the text file"
      copy:
        src: /app/test.txt
        dest: /test.txt
      delegate_to: netology-ml

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
