from web_base.colored_print import print_colored
def is_online():
    print_colored("------[is_online]-------", "cyan")
    return {"status": True}