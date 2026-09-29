import subprocess


def get_missing_updates():
    powershell_command = r'''
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$result = $searcher.Search("IsInstalled=0")

foreach ($update in $result.Updates) {
    $update.Title
}
'''

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", powershell_command],
        capture_output=True,
        text=True,
        check=False
    )


    updates = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return updates


if __name__ == "__main__":
    updates = get_missing_updates()

    print(f"Missing updates: {len(updates)}")

    for update in updates:
        print(f"- {update}")
