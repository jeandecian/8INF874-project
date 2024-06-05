# 8INF874 - Project

## CodeCarbon

[CodeCarbon](https://github.com/mlco2/codecarbon)

## Files Generator

- 1 MB = 1048576 bytes
- 100 MB = 104857600 bytes
- 1 GB = 1073741824 bytes
- 10 GB = 10737418240 bytes
- 100 GB = 107374182400 bytes
- 1 TB = 1099511627776 bytes
- 10 TB = 10995116277760 bytes

### Linux

```bash
head -c <bytes> /dev/urandom > <file>
```

### Windows

```shell
fsutil file createnew <file> <bytes>
```
