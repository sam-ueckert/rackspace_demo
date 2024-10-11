# vsys-dashboard
VSYS capacity management dashboard

## Notes on build
Deploy keys for Github repo are in /app/.ssh. On Docker image build, this .ssh directory is copied to /root. The config file specifies the app name used
in the 'git clone' command.
The Dockerfile specifies the path to the git repo to clone.
The deploy key for this project is granted read access to the Github repo. #TODO Change from dev repo to prod repo



