# Oxford College Vacancies Monitor

This repository serves as a **GitHub template** for monitoring the [Oxford College Vacancies](https://collegevacancies.web.ox.ac.uk/) website. It checks for new job postings containing specific keywords and sends notifications via Slack when matches are found.

## Features

- 🔍 Searches for configurable keywords in vacancy titles and descriptions
- ⏱️ Configurable schedule via CI variables
- 🔔 Sends notifications via Slack only for new matches
- 📝 Keeps track of previously notified vacancies to avoid duplicates

## Setup Instructions

1. **Create your repository from this template:**
   - Click the green "Use this template" button at the top of this repository
   - Select "Create a new repository"
   - Name your repository and click "Create repository from template"

2. **Create a Slack Incoming Webhook:**
   - Go to your Slack workspace → Administration → Manage apps
   - Search for "Incoming Webhooks" and add to your workspace
   - Create a new webhook for a specific channel
   - Copy the webhook URL

3. **Add the Slack webhook URL as a secret in your GitHub repository:**
   - Go to your repository → Settings → Secrets → Actions
   - Click "New repository secret"
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Paste the Slack webhook URL
   - Click "Add secret"

4. **Configure keywords and schedule using CI variables:**
   - Go to your repository → Settings → Variables → Actions
   - Add the following variables:
     - `VACANCY_KEYWORDS`: Comma-separated list of keywords - these could be college names or role titles (e.g., "Balliol")
     - `CRON_SCHEDULE`: Cron expression for the schedule (e.g., "0 8 * * *" for daily at 8 AM UTC)

5. **Enable GitHub Actions:**
   - Go to your repository → Actions
   - Click "I understand my workflows, go ahead and enable them"

## Manual Trigger

You can manually trigger the workflow:
1. Go to the "Actions" tab in your repository
2. Select "Monitor Oxford College Vacancies" workflow
3. Click "Run workflow"

## Default Values

If CI variables are not configured:
- **Default keywords**: "Tutor"
- **Default schedule**: Daily at 8:00 AM UTC (cron: '0 8 * * *')

## Troubleshooting

- **No notifications received:** Check if your Slack webhook URL is correctly configured in the repository secrets.
- **Workflow not running:** Make sure GitHub Actions is enabled for your repository.
- **Keywords not working:** Verify the `VACANCY_KEYWORDS` CI variable is set correctly with comma-separated values.

## Customization

- **Changing notification time:** Update the `CRON_SCHEDULE` CI variable
- **Modifying search keywords:** Update the `VACANCY_KEYWORDS` CI variable
- **Additional notification channels:** Modify the `send_slack_notification` function in the Python script

## License
