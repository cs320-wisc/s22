# Connecting with SSH from the Terminal

In a terminal Window, run something like `ssh USER@IP`. You should
replace `USER` with the user name you got in the last step of the
directions for creating the SSH Key ([here](ssh.md)).  You should
replace "IP" with the "External IP" you saw in the table of VM
instances after you launched your virtual machine.

You might see something like "The authenticity of host
'104.154.180.165 (104.154.180.165)' can't be established.  ECDSA key
fingerprint is SHA256:....  Are you sure you want to continue
connecting (yes/no/[fingerprint])?"  You can type "yes".

If the ssh connection works, run `lsb_release -a`.  If all is well, it
should show you what version of Ubuntu you're running (hopefully
20.04).  It should look something like this:

<img src="img/25.png" width=600>

Congrats, you've created your first virtual machine with Linux
installed!  This is no small feat, and being able to do so in the
future in an invaluable career skill.

Note: you can type "exit" or `CTRL-D` to exit the SSH connection and
run commands on your own computer again.
