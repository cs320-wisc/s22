# Linux Skills

In this section, you'll learn a few Linux commands and get more familiar with your VM.

## 1. Updates and Rebooting

**IMPORTANT:** save all your code in Jupyter before continuing.  You
  might also consider downloading your most important work to your
  laptop too.

SSH into your VM.  There will be some messages when you connect, perhaps similar to the following:

```
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.11.0-1028-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sat Mar  5 18:46:20 UTC 2022

  System load:  0.0                Processes:             133
  Usage of /:   41.7% of 14.37GB   Users logged in:       0
  Memory usage: 34%                IPv4 address for ens4: 10.128.0.3
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

21 updates can be applied immediately.
To see these additional updates run: apt list --upgradable


*** System restart required ***
Last login: Fri Mar  4 17:48:33 2022 from 72.33.0.72
```

If you also get a message that updates are available, install them now
with this (you might be prompted to type a `Y`):

`sudo apt upgrade`

If you saw a message about rebooting too (`*** System restart required ***`), you can do this now:

`sudo reboot`

**REMEMBER:** always save any unsaved work before rebooting.

This will end your SSH session, but you can try reconnecting: `ssh
USER@IP_ADRESS`.  It will probably fail initially because your VM is
in the process of rebooting.  Keep trying, and you should be able to
reconnect within a few minutes.

During a reboot, all processes stop, including Jupyter.  You'll need
to restart it (don't `cd` into a sub directory first, or you won't be
able to access files outside that sub directory):

```
nohup python3 -m notebook --no-browser --ip=0.0.0.0 --port=2020
```

## 2. Networking

### Website to VM

The `curl` command can be used to send web requests to servers.  Open
https://tyler.caraza-harter.com/hello.txt in a web browser.  Now let's
try fetching it with `curl` from within an SSH session:

```
curl https://tyler.caraza-harter.com/hello.txt
```

The file contents should be printed directly to the screen.  We can
use `-o` to download to a file instead:

```
curl https://tyler.caraza-harter.com/hello.txt -o mycopy.txt
```

Use `ls` and `cat` to see the downloaded file and it's contents.

### VM to VM

The *network cat* program (`nc` for short) is like `cat`, but for
outputing data received over the network (instead of from a file).

While in SSH, choose a port number (for example, `54321`).  Start the
`nc` program, listening on that port:

```
nc -lk 54321
```

Tell a group member (a) your virtual machine's external IP address and
(b) the port number you chose.

From their own virtual machine, ask them to run the following command:
`nc <YOUR IP ADDRESS> <PORT NUMBER>`.  For example, it might look
like this:

```
nc 104.154.131.51 54321
```

Once these two `nc` commands are run correctly on the two different
VMs, it should be possible for the owners of those VMs to type
messages back and forth.

**Requirement**: everybody in the group should get a turn to do both of the following:
1. send a message from their VM
2. receive a message on their VM from someone else's VM

### VM to Laptop

You may want to bulk download files from your VM to your laptop.

The `cp ORIGINAL_FILE NEW_COPY` command creates copies of a file.  The
`ssh USER@IP` connects to a remote computer. The `scp` command is a
combination of these that can upload/download files to/from a VM.

On your **laptop**, run the following (don't SSH first; replace `USER` and `VM_IP`):

```
scp USER@VM_IP:~/s22/p3/scrape.py scrape.py
ls
```

You should see `scrape.py` downloaded to your own computer.  You could
use `scp USER@VM_IP:~/s22/p3/scrape.py some_other_name.py` if you
wanted your download of `scrape.py` to be named something else on your
computer.

What if we want to download all of `p3` to the current directory (remember `.` is a shorthand for the current directory)?  Try this:

```
scp USER@VM_IP:~/s22/p3 .
```

You should get an error like this:

```
scp: /home/USER/s22/p3: not a regular file
```

If you want `scp` to work on directories (which contain other directories, which contain other directories, which ...), you need to use recursive mode: `-r`.

```
scp -r USER@VM_IP:~/s22/p3 .
```

There should now be a `p3` directory on your laptop with all your
work.  Not sure where?  Run `pwd`.

## 3. Processes

SSH to your VM, then run the `find` command.  It will find every file
and directory (including sub files and directories) at your current
location, in this case your user's home directory.

What if you want to find all the Jupyter notebooks in the `s22`
directory?  First, `cd` there.

On Linux, you can combine commands like this: `PROGRAM1 | PROGRAM2`.
This runs `PROGRAM1`, captures its output, and feeds the results as
input to `PROGRAM2`.  The character in the middle is called a *pipe*
and this technique is called *piping*.

Let's pipe the output of `find` into the `grep` program.  The `grep`
program filters lines based on some search criteria.  We'll filter to only see lines containing `.ipynb`:

```
find . | grep .ipynb
```

We can combine `grep` with other commands to search for specific
processes, which we may need to terminate.

For example, a common situation is that we want to find and kill the
process using a specific port (because we can't start a new process
with that port while the prior one is running).  In this case, we'll
use the `lsof` program together with `grep`.  The name stands for
**l**i**s**t **o**pen **f**iles (it also lists open ports, not just
files).

Run `lsof | grep 2020` -- this will show the processes running Jupyter
on port 2020.

Open up a second terminal window and SSH again, so that you have two
SSH sessions active at once.

1. in one SSH session, `cd` to `s22/labs/linux-skills`, then run `python3 port_user.py`.  The program uses port `55555`, so no other process can start using that port until `port_user.py` stops.
2. in the SSH session, run `lsof | grep 55555`

You should see something somewhat like this (details will vary):

```
trh@instance-2:~$ lsof | grep 55555
python3   1986                            trh    3u     IPv4              40497       0t0        TCP *:55555 (LISTEN)
```

Identify the process ID in your case (for the above output, the process ID was `1986`).  You can use the `kill` command to terminate that process from any SSH session.  Run the following (substituting in whatever process ID you saw):

```
kill 1986
```

Verify in the other window that `port_user.py` was terminated.

In the window where you were running `port_user.py`, now run this:

```
python3 forever.py
```

This is a nasty program.  It tries to use up all your CPU with an
infinite loop, and it refuses to die when asked politely.  Try
"CONTROL-C" to see what we mean.

In the other window, run `htop`.  In addition to the summary of CPU
and memory usage at the top, you'll see a list of processes below,
sorted by CPU usage.  The `forever.py` program should one of the top
ones.  Note down its process ID (in the `PID` column).  Close `htop`
(you can type `q` for "quit").

Try killing `forever.py` using the `kill PROCESS_ID` command like we
did to kill `port_user.py` before.  Did it work?

There are different kill signals that can be used to stop a process,
and each has a number.  For example, a few are 2 (interrupt), 6
(abort), 9 (kill), 15 (terminate).

Kill signal 9 is the most aggressive and cannot be ignored by an
uncooperative process.  This is a good time to use it:

```
kill -9 PROCESS_ID
```

Verify that it worked this time.

We won't go into details here, but there are other variants on killing
processes.  For example, `pkill -f` (mentioned in the project
directions) kills processes based on their name (rather than process
ID).
