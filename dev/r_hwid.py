from winreg import OpenKey, QueryValueEx, CloseKey, HKEY_LOCAL_MACHINE

def get_registry_value(key_path, value_name):
    try: 
        key = OpenKey(HKEY_LOCAL_MACHINE, key_path)
        
        value, _ = QueryValueEx(key, value_name)
        
        CloseKey(key)
        
        return value
    except Exception:
        return None
    
hwid = get_registry_value(r"SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001", r"HwProfileGuid")
if hwid is not None:
    hwid = hwid.strip('{}').upper()

print(hwid)