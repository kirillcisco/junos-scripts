# junos-scripts
## What IS?
A collecion of python scripts for Juniper OS that help work

## requirements
If this on-box operational script:
1) script.py --> ./var/db/script/op
2) user@device# set system scripts language python3
3) user@device# set system scripts op file [script.py] \
You can set the alias: \
a) set system scripts op file [script.py] command [script-alias]
4) user@device> op [script.py] / [script-alias]



## OP script
### bgp_sum.py
Default show bgp summary, information about routes in second line, and u cant just use _**| match 192.168.1.1**_\

`192.168.1.1          ASnum   N    N       0       0 23w5d 0:41:47 Establ ` \
 `inet.0: N/N/N/N` 
 
Output of @> op bgp_sum | match 192.168.1.1 \
routes Active/Recieved/Accepted | Advertised \
peer_group + peer_description + flaps_count 

`192.168.1.1    ASnum   Established     N/N/N | N       23w5d 0:41:47    CORE-IBGP-IPV6  IBGP peers IPV6  flaps: 1 `
