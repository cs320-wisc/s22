# Google Option for Virtual Machine

## Step 1: Create Account and Redeem Credits

See details about how to get the $50 credit: https://canvas.wisc.edu/courses/272598/discussion_topics/1079256.

Then follow [these instructions](gcp.md) to create an account and redeem the credit.

## Step 2: Configuring the Firewall

Follow [these instructions](firewall.md) to configure the firewall to unblock all
ports.

## Step 3 [Recommended]: Creating an SSH Key

You already have an idea of what a shell is: you've been either using
PowerShell (Windows) or bash (default on Mac) in CS 220/301.  *ssh*
stands for "secure shell", and it's a special shell that lets you
remotely connect to other computers over the network and run commands
there.  An *ssh key* is like a randomly generated password that ssh
automatically uses to access other machines (you won't generally type
it).

Macs and recent Windows computers (Windows 10 with recent updates)
should have a program OpenSSH installed, which will be the most
convenient way to access your virtual machine.

Try [these directions](ssh.md) to create an SSH key and connect it
with your cloud account.  If it doesn't work (e.g., because you don't
have OpenSSH), don't worry too much -- there are workarounds later.

## Step 4: Launching your Virtual Machine

Now it's time to actually create your virtual machine!  Follow [these steps](launch.md).

## Step 5a: Connecting with SSH from your terminal

If you were able to configure the SSH key properly in Step 3, follow
[these directions](connect.md).

## Step 5b [Alternative]: Connecting without SSH

If you couldn't configure the SSH key, follow [these
directions](connect-alt.md) instead.

## Step 6: Setting up Jupyter

Now lets get Jupyter and some other software installed.  Follow [these
directions](jupyter.md).

