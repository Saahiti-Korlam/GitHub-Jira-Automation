# GitHub to Jira Auto Issue Creator 🚀

Automatically create Jira issues when a developer comments `/createissue` on a GitHub repository — no manual Jira dashboard interaction needed.

---

## 📌 Problem Statement

Every time a developer spots a bug or problem in newly added code or a GitHub repo, they had to manually navigate to the Jira dashboard to create an issue. This project eliminates that friction by automating Jira issue creation directly from a GitHub comment.

---

## 🏗️ Architecture Overview

```
GitHub (Webhooks)  -->  Python Flask API  -->  Jira (REST API)
```

- **GitHub Webhooks** — Listens for comment events on the repository
- **Python Flask API** — Acts as the middleware deployed on an EC2 server
- **Jira REST API** — Receives the request and creates the issue on the board

---

## 🛠️ Tech Stack

| Component | Purpose |
|-----------|---------|
| **GitHub Webhooks** | Triggers on issue comment events |
| **Python + Flask** | Builds and hosts the API endpoint |
| **AWS EC2** | Hosts and runs the Flask server |
| **Jira REST API v3** | Creates issues on the Jira board |

---

## ⚙️ Prerequisites & Installations

### 1. Python & pip
Ensure Python 3 and pip are installed on your EC2 instance:
```bash
sudo dnf install python3-pip -y
```

### 2. Flask
Flask is a lightweight Python web framework used to build and serve the API endpoint.
```bash
pip install flask
```
Verify the installation:
```bash
python -m flask --version
```

### 3. Requests Library
Used to make HTTP calls to the Jira REST API:
```bash
pip install requests
```

---

## 🔑 Setting Up Jira API Token

1. Log in to your Atlassian account
2. Click on your **Profile → Account Settings → Security**
3. Scroll to the **API Tokens** section
4. Click **"Create and Manage API Tokens"**
5. Click **"Create API Token"**, give it a label (e.g., `python`), and save it
6. Copy and store the generated token securely — you will need it in the Flask script

---

## 🧩 Jira Issue Type IDs

When creating an issue via API, you need to pass the correct Issue Type ID. You can find these from your Jira board URL under **Configure Board → Issue Types**:

| Issue Type | ID |
|------------|----|
| Task | `10006` |
| Epic | `10009` |
| Bug | `10007` |
| Story | `10008` |

---

## 🐍 Flask API — Key Concepts

Flask is used to convert the Python script into a deployable REST API. Here are the mandatory building blocks:

```python
from flask import Flask

app = Flask(__name__)
```

- `from flask import Flask` — Imports only the `Flask` class from the flask package
- `app = Flask(__name__)` — Creates the Flask application instance; **this line is mandatory in every Flask program**

### Decorator (`@app.route`)
```python
@app.route('/issue', methods=['POST'])
def createJira():
    ...
```
- A **decorator** performs an action *before* the function executes
- It checks whether the incoming HTTP request is hitting the correct path (e.g., `/issue`)
- Example: a payment endpoint would be accessible at `http://<ip>/pay` — Flask validates the path before running the function

### Flask Default Port
- Flask runs on **port 5000** by default
- Access the server at: `http://<your-ip>:5000`
- To allow external access, bind to all interfaces: `app.run(host='0.0.0.0', port=5000)`

### HTTP Methods Used
| Method | Purpose |
|--------|---------|
| `POST` | Send data / create a resource |
| `GET`  | Retrieve information |
| `PUT`  | Modify / update a resource |
| `DELETE` | Remove a resource |

> The Jira issue creation uses **POST**, as we are sending data to create a new resource.

---

## 🚀 Step-by-Step Implementation

### Step 1 — Write the Flask API
Create a Python file (e.g., `github-issue.py`) with:
- A `/createissue` route accepting `POST` requests
- Authentication using your Jira email and API token
- A JSON payload defining the issue fields (summary, description, project key, issue type)
- The response returned from Jira API
### Step 2 — Deploy to AWS EC2

Launch an EC2 instance and SSH into it, then:

```bash
# Update package manager and install pip
sudo dnf install python3-pip -y

# Install Flask and Requests
pip install flask
pip install requests

# Transfer your script to EC2 (from local machine)
scp -i your-key.pem github-issue.py ec2-user@<ec2-public-ip>:~

# Run the Flask server
python3 github-issue.py
```

Make sure **port 5000** is open in your EC2 Security Group inbound rules.
<img width="947" height="409" alt="server-runnig" src="https://github.com/user-attachments/assets/9b9dee63-d72e-432b-8d19-6861e5e15fdf" />

### Step 3 — Create a GitHub Webhook

1. Go to your GitHub repository
2. Navigate to **Settings → Webhooks → Add Webhook**
3. Fill in the details:

| Field | Value |
|-------|-------|
| Payload URL | `http://<ec2-public-dns-or-ip>:5000/issue` |
| Content Type | `application/json` |
| Events | Select **"Let me select individual events"** → check **Issue comments** |
<img width="955" height="463" alt="webhook" src="https://github.com/user-attachments/assets/b839a4ed-b22c-4a97-a0f4-337b512200cb" />

4. Click **Add Webhook**

### Step 4 — Trigger & Verify

1. Go to your GitHub repository's **Issues** section
2. Open any issue and add a comment: `/createissue`
3. The webhook fires, hits your Flask API, and the API calls Jira
4. Navigate to your **Jira Dashboard** and confirm the new issue appears on the board
<img width="957" height="509" alt="createissue-1" src="https://github.com/user-attachments/assets/8d9f0392-ee5f-4684-9bea-e398cd485782" />

---

## 🔁 Flow Summary

```
Developer comments "/createissue" on GitHub
        |
        ▼
GitHub Webhook fires a POST request
        |
        ▼
Flask API running on EC2 receives the request
        |
        ▼
Flask sends a POST to Jira REST API with issue details
        |
        ▼
Jira creates the issue on the project board ✅
```
<img width="938" height="446" alt="jira-issues" src="https://github.com/user-attachments/assets/5874629c-b48c-4a51-bfdb-a13b294f00ea" />

<img width="938" height="446" alt="jira-issues" src="https://github.com/user-attachments/assets/820da40f-44f9-4b45-b984-4567b2f7a073" />

<img width="959" height="458" alt="jira-issue-2" src="https://github.com/user-attachments/assets/635c74d8-4ee6-4897-ae35-33170862a795" />

---

## ✅ Conclusion

This project bridges **GitHub** and **Jira** using a lightweight **Flask API** deployed on **AWS EC2**, enabling developers to trigger Jira issue creation directly from a GitHub comment. By combining GitHub Webhooks, Python Flask, and the Jira REST API, the entire workflow is automated — saving time, reducing context switching, and keeping development and project tracking in sync.

---
### sample other issues 
<img width="956" height="450" alt="issues-jira" src="https://github.com/user-attachments/assets/8e1001cc-1817-4129-87d7-69aaa23f7e20" />

<img width="938" height="446" alt="jira-issues" src="https://github.com/user-attachments/assets/5363f999-0d7b-4133-bcbe-ab225be3ef7c" />

## 📚 References

- [Jira REST API v3 Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Get Project List API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-get)
- [Create Jira Issue API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post)
- [Flask Documentation](https://flask.palletsprojects.com/)


