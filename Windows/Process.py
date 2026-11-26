
import win32api
import win32con
import win32process


def extract_processes(limit=10):
    """Extract information about running Windows processes."""

    processes = []

    # Get all running process IDs
    process_ids = win32process.EnumProcesses()

    for pid in process_ids:
        if pid == 0:
            continue

        try:
            # Open the process
            handle = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION |
                win32con.PROCESS_VM_READ,
                False,
                pid
            )

            try:
                # Get executable path
                exe_path = win32process.GetModuleFileNameEx(
                    handle, 0
                )

                process_name = exe_path.split("\\")[-1]

                processes.append({
                    "pid": pid,
                    "name": process_name,
                    "exe": exe_path
                })

            finally:
                win32api.CloseHandle(handle)

        except Exception:
            # Some Windows processes restrict access
            continue

        if len(processes) >= limit:
            break

    return processes


if __name__ == "__main__":

    running_processes = extract_processes(10)

    print("\n===== TOP 10 WINDOWS PROCESSES =====\n")

    for process in running_processes:
        print("PID:", process["pid"])
        print("Name:", process["name"])
        print("Path:", process["exe"])
        print("-" * 40)

    print("Total processes extracted:", len(running_processes))
