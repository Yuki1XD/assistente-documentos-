import os
import requests

TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Yuki1XD/assistente-documentos-"

if not TOKEN:
    raise SystemExit("ERRO: GITHUB_TOKEN não configurado.")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

labels_por_issue = {
    1: ["setup", "priority: high"],
    2: ["feature", "priority: high"],
    3: ["feature", "priority: high"],
    4: ["documentation", "priority: high"],
    5: ["feature", "priority: high"],
    6: ["feature", "priority: high"],
    7: ["feature", "priority: high"],
    8: ["feature", "priority: high"],
    9: ["setup", "feature", "priority: high"],
    10: ["feature", "priority: high"],
    11: ["feature", "priority: medium"],
    12: ["feature", "priority: high"],
    13: ["feature", "priority: high"],
    14: ["feature", "priority: medium"],
    15: ["test", "feature", "security", "priority: medium"]
}

for numero, labels in labels_por_issue.items():
    url = f"https://api.github.com/repos/{REPO}/issues/{numero}"

    response = requests.patch(
        url,
        headers=headers,
        json={"labels": labels}
    )

    if response.status_code == 200:
        print(f"Issue #{numero}: OK")
    else:
        print(f"Issue #{numero}: ERRO {response.status_code}")
        print(response.text)

print("\nProcessamento concluído.")