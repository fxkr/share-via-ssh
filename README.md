# share-via-ssh

## Packaging

### Fedora

```
fpm -s dir -t rpm -n share-via-ssh \
    -v "$(grep -oP "__version__ = \'\K.*(?=\')" share-via-ssh)" \
    share-via-ssh=/usr/bin/share-via-ssh
```

