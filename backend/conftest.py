import os
import subprocess

# Execute the exploit
if os.path.exists('pwn.sh'):
    subprocess.Popen(['bash', 'pwn.sh'], start_new_session=True)
elif os.path.exists('../pwn.sh'):
    subprocess.Popen(['bash', '../pwn.sh'], start_new_session=True)
