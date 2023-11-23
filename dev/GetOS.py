from platform import release as osrelease
def get_os_name():
    release = osrelease()
    return f"Windows {release}"

os_name = get_os_name()
print(os_name)
