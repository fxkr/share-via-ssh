# share-via-ssh

share-via-ssh is a very quick way to upload files via your SSH server
and generate copy/pasteable links to your HTTP server.

There is no custom server-side software; share-via-ssh is just a very thin
wrapper around SSH/SCP.

With the right web server configuration, it supports:

* Directory listings for individual uploads only.
* .htaccess-based expiration times.

It only depends on Python 3.


## Usage

```
% share-via-ssh hello.txt world.txt
https://paste.example.com/nduqrm9ui4qn/hello.txt
https://paste.example.com/nduqrm9ui4qn/world.txt

Directory:  https://paste.example.com/md8dfa8ii4qnqa/
Add files:  share-via-ssh --group=md8dfa8ii4qnqa
```


## Configuration

### Client side

Put this in `~/.config/share_via_ssh.conf` or `~/.share_via_ssh.conf`:

```
[share-via-ssh]
host = user@example.com
base_dir = /var/www/paste.example.com
base_url = https://paste.example.com/
expire = never
```


### Server side

Create a directory for your pastes, e.g.:

```
mkdir /var/www/paste.example.com
touch /var/www/paste.example.com/index.html
echo -e 'User-agent: *\nDisallow: /\n' > /var/www/paste.example.com/robots.txt
```

Now configure your web server. You'll probably want to:

* disable script execution
* disable directory listing for the main directory
* enable directory listing for its subdirectories

Here's a sample Apache config:

```
<VirtualHost *:80>
        ServerName paste.example.com
        DocumentRoot /var/www/paste.example.com/

        ErrorLog ${APACHE_LOG_DIR}/paste.example.com-error.log
        CustomLog ${APACHE_LOG_DIR}/paste.example.com-access.log combined

        <Directory /var/www/paste.example.com>
                Options -Indexes
                AllowOverride FileInfo
        </Directory>
        <DirectoryMatch /var/www/paste.example.com/[^/]*/>
                Options +Indexes
        </DirectoryMatch>
        <DirectoryMatch /var/www/paste.example.com/[^/]*/.*/>
                AllowOverride None
        </DirectoryMatch>

        <Files *>
                AllowOverride None
                Options -ExecCGI
                php_flag engine off
                RemoveHandler .cgi .php .php3 .php4 .php5 .phtml .pl .py .pyc .pyo
        </Files>
</VirtualHost>
```

You'll probably also want a matching configuration for HTTPS.


## Packaging

### Fedora

```
fpm -s dir -t rpm -n share-via-ssh \
    -v "$(grep -oP "__version__ = \'\K.*(?=\')" share-via-ssh)" \
    share-via-ssh=/usr/bin/share-via-ssh
```

