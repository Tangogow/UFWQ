# UFW queue

### Todo

- [ ] systemctl start stop restart
- [ ] packet size
- [ ] enable/disable
- [ ] reset
- [ ] default
- [ ] profiles
- [x] protocol mapping
- [ ] /etc/ conf file
- [ ] view log live
- [ ] ip table

### Install

### Usage

```bash
pip install pipenv
```
apt install python-pip git libnfnetlink-dev libnetfilter-queue-dev
build-essential libnetfilter-queue-dev python-dev ?
##### Local

```bash
pipenv install --python 2.7 --system --deploy --ignore-pipfile # or --dev
pipenv shell ufwq start

# testing
echo text | netcat localhost 12
```

##### Docker

```bash
docker run -tid ufwq
docker build -t ufwq .

# testing
echo text | netcat 172.17.0.2 12
```

### Blocking priority

1. Blocked port
2. Blocked rules
3. Allowed rules
4. Database Blacklist

### Logs

/var/log/ufwq

### Config

/etc/ufwq
