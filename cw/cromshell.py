import os, subprocess, sys

def config_dn():
    return os.path.join("apps", "cromshell", ".cromshell")
#--

def server_fn():
    return os.path.join(config_dn(), "cromwell_server.config")
#--

def update_server(url):
    dn = config_dn()
    if not os.path.exists(dn):
        return None, f"No cromshell directory at <{dn}> detected, not updating url\n"
    fn = server_fn()
    with open(fn, "w") as f:
        f.write(f"{url}\n")
    return True, f"Updated cromshell url <{url}> in <{fn}>\n"
#--
