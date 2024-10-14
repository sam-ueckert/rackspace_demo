# vsys-dashboard
VSYS capacity management dashboard

## Notes on build
To inject a Github PAT for authentication to the repo, first create a Docker secret:
docker secret create github_token github_token.txt
Then this line leverage that secret mount:
RUN --mount=type=secret,id=github_token \
    export GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    git clone https://$GITHUB_TOKEN@github.com/rax-nsi-cdw/vsys-dashboard.git .