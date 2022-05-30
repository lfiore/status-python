# status-python
A simple variation of my server status script written in Python

# Installation
To run the script just run the following command

`wget -O status https://raw.githubusercontent.com/lfiore/status-python/master/status.py && chmod +x status`

# Usage

`./status`

# Example output

``` ==== Server Info =============================================================

 Hostname       dev (example)
 IP Address     1.1.1.1 (example)
 Uptime         2 days, 23 hours, 36 minutes and 18 seconds

 ==== Software Info ===========================================================

 Distro         Debian GNU/Linux 10 (buster)
 Kernel         4.19.0
 System Type    64-bit (x64)

 ==== CPU Info ================================================================

 Model          Intel(R) Xeon(R) CPU E3-1241 v3 @ 3.50GHz
 Load           0.00, 0.01, 0.05

 ==== Memory Usage ============================================================

 RAM            [######################-------------] (125.75 / 192.0 MB)

 ==== Disk Usage ==============================================================

 Disk           [###--------------------------------] (1.19 / 11.68 GB)
 ```
